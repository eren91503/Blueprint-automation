#!/usr/bin/env python3
"""Prüft die Logik von bridge.py mit künstlichen Composio-Funktionen (kein Netz, kein Konto, keine Kosten).

usage: python3 tools/test_bridge_mock.py

Das ersetzt keinen Live-Test: Es zeigt nur, dass die Aufrufe in der richtigen Reihenfolge und mit den richtigen
Daten gemacht werden. Ob Composio die Aufrufe so annimmt, zeigt erst ein Lauf in der echten Umgebung.
"""
import base64, hashlib, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
import requests  # noqa: E402

repo_store = {}      # (repo, pfad, branch) -> bytes
blobs = {}           # sha -> bytes
s3 = {}              # s3key -> bytes
drive = []           # {"id","name","parents","bytes"}
protokoll = []
fehler_put = {"anzahl": 0}


class Antwort:
    def __init__(self, daten, status=200):
        self.content, self.status_code = daten, status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def fake_get(url, timeout=0):
    protokoll.append(("GET", url))
    return Antwort(b"AUDIO-" + url.encode()) if "nichts" not in url else Antwort(b"", 200)


def proxy_execute(methode, endpoint, toolkit, query_params=None, body=None):
    protokoll.append((methode, endpoint))
    m = re.match(r"/repos/([^/]+/[^/]+)/contents/(.+)", endpoint)
    if m:
        repo, pfad = m.groups()
        branch = (query_params or {}).get("ref") or (body or {}).get("branch") or "main"
        if methode == "GET":
            daten = repo_store.get((repo, pfad, branch))
            if daten is None:
                return None, "404 Not Found"
            return {"sha": hashlib.sha1(daten).hexdigest()}, None
        if methode == "PUT":
            if fehler_put["anzahl"] > 0:
                fehler_put["anzahl"] -= 1
                return None, "500 Server Error"
            daten = base64.b64decode(body["content"])
            repo_store[(repo, pfad, branch)] = daten
            blobs[hashlib.sha1(daten).hexdigest()] = daten
            return {"ok": True}, None
    b = re.match(r"/repos/[^/]+/[^/]+/git/blobs/(.+)", endpoint)
    if b:
        return {"content": base64.b64encode(blobs[b.group(1)]).decode()}, None
    return None, "unbekannter Aufruf"


def upload_local_file(pfad):
    key = "s3key-" + hashlib.md5(pfad.encode()).hexdigest()
    s3[key] = open(pfad, "rb").read()
    return {"s3key": key}, None


def run_composio_tool(name, args):
    protokoll.append((name, str(args)[:80]))
    if name == "GOOGLEDRIVE_UPLOAD_FILE":
        fid = f"drive{len(drive) + 1}"
        drive.append({"id": fid, "name": args["file_to_upload"]["name"], "parents": [args["folder_to_upload_to"]],
                      "bytes": s3[args["file_to_upload"]["s3key"]]})
        return {"data": {"id": fid}}, None
    if name == "GOOGLEDRIVE_FIND_FILE":
        q = args["q"]
        nm = re.search(r"name = '([^']+)'", q).group(1)
        par = re.search(r"'([^']+)' in parents", q).group(1)
        return {"data": {"files": [{"id": d["id"], "name": d["name"], "parents": d["parents"]}
                                   for d in drive if d["name"] == nm and par in d["parents"]]}}, None
    return None, "unbekanntes Werkzeug"


def pruefe(bedingung, text):
    print(("OK     " if bedingung else "FEHLER ") + text)
    if not bedingung:
        pruefe.fehler += 1


pruefe.fehler = 0


def main():
    requests.get = fake_get
    ns = {"proxy_execute": proxy_execute, "run_composio_tool": run_composio_tool, "upload_local_file": upload_local_file}
    quelle = open(os.path.join(HIER, "bridge.py"), encoding="utf-8").read()
    exec(compile(quelle, "bridge.py", "exec"), ns)
    ns["_PAUSE"] = 0

    # 1. Audio ins Repo
    erg = ns["audio_to_repo"]("o/r", "projekte/k/videos/V1", {"hook": "http://x/h", "haupt": "http://x/m"})
    pruefe(erg == {"hook": "ok", "haupt": "ok"}, "audio_to_repo meldet ok für beide Blöcke")
    pruefe(repo_store[("o/r", "projekte/k/videos/V1/blocks/hook.mp3", "main")] == b"AUDIO-http://x/h",
           "Inhalt von hook.mp3 im Repo stimmt")
    # 2. Überschreiben (bekannte sha wird mitgeschickt)
    ns["audio_to_repo"]("o/r", "projekte/k/videos/V1", {"hook": "http://x/neu"})
    pruefe(repo_store[("o/r", "projekte/k/videos/V1/blocks/hook.mp3", "main")] == b"AUDIO-http://x/neu",
           "Zweiter Lauf überschreibt die Datei")
    # 3. Einmaliger Fehler wird wiederholt
    fehler_put["anzahl"] = 1
    erg = ns["audio_to_repo"]("o/r", "V2", {"hook": "http://x/h"})
    pruefe(erg["hook"] == "ok", "Ein Fehler beim Ablegen wird einmal wiederholt")
    # 4. Dauerhafter Fehler endet mit RuntimeError
    fehler_put["anzahl"] = 5
    try:
        ns["audio_to_repo"]("o/r", "V3", {"hook": "http://x/h"})
        pruefe(False, "Dauerhafter Fehler löst RuntimeError aus")
    except RuntimeError as ex:
        pruefe("2 Versuchen" in str(ex), "Dauerhafter Fehler löst RuntimeError aus (nach 2 Versuchen)")
    fehler_put["anzahl"] = 0
    # 5. Leere Audiodatei
    try:
        ns["audio_to_repo"]("o/r", "V4", {"hook": "http://x/nichts"})
        pruefe(False, "Leere Audiodatei wird abgelehnt")
    except RuntimeError:
        pruefe(True, "Leere Audiodatei wird abgelehnt")
    # 6. Video nach Drive aus Zweig videos
    video = b"VIDEO" * 1000
    ns["put_repo"]("o/r", "out_videos/test.mp4", video, "Video", "videos")
    erg = ns["video_to_drive"]("o/r", "out_videos/test.mp4", "test.mp4", "ORDNER_ERSTELLT", "videos")
    pruefe(erg["bytes"] == len(video), "video_to_drive: Größe stimmt")
    pruefe(erg["in_ordner"] is True, "video_to_drive: Datei liegt im angegebenen Drive-Ordner")
    pruefe(drive[-1]["bytes"] == video and drive[-1]["parents"] == ["ORDNER_ERSTELLT"], "Drive-Inhalt und Ordner stimmen")
    # 7. Fehlende Datei
    try:
        ns["video_to_drive"]("o/r", "out_videos/gibtsnicht.mp4", "x.mp4", "ORDNER", "videos")
        pruefe(False, "Fehlende Repo-Datei löst RuntimeError aus")
    except RuntimeError:
        pruefe(True, "Fehlende Repo-Datei löst RuntimeError aus")
    # 8. Keine festen Werte im Code
    pruefe(not re.search(r"eren91503|faktum", quelle, re.I), "bridge.py enthält keine festen Faktum-Werte")
    print("MOCK-TEST", "FEHLGESCHLAGEN" if pruefe.fehler else "OK", f"({pruefe.fehler} Fehler)")
    sys.exit(1 if pruefe.fehler else 0)


if __name__ == "__main__":
    main()
