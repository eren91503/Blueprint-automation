"""Dateibrücke für die Composio-Umgebung (Workbench). Ohne feste Repo- oder Ordnerwerte.

Wofür: Die Claude-Sitzung erreicht die ElevenLabs-Links nicht (403) und lädt große Dateien nicht selbst nach Drive.
Darum läuft das hier in der Composio-Umgebung, wo `proxy_execute`, `run_composio_tool` und `upload_local_file`
vorhanden sind (GitHub- und Google-Drive-Verbindung in Composio nötig).

Laden (in der Composio-Umgebung, ein Mal je Lauf):
    import base64
    r, e = proxy_execute("GET", "/repos/<owner>/<repo>/contents/tools/bridge.py", "github")
    exec(base64.b64decode(r["content"]).decode())

Funktionen:
    audio_to_repo(repo, ordner, urls, branch="main")
        urls = {"hook": "<ElevenLabs-Link>", ...}; legt <ordner>/blocks/<szene>.mp3 im Repo ab.
    video_to_drive(repo, repo_pfad, name, folder_id, branch="main")
        holt die Datei aus dem Repo (Zweig `branch`), lädt sie in den Drive-Ordner `folder_id`, prüft danach,
        dass sie wirklich in diesem Ordner liegt.
    drive_ordner(kanalname)
        legt in Drive den Ordner <kanalname> mit den Unterordnern `erstellt` und `gepostet` an (oder findet sie, wenn
        es sie schon gibt) und gibt die IDs zurück: {"kanal": id, "erstellt": id, "gepostet": id}.
    in_ordner(name, folder_id)
        listet Dateien dieses Namens im Drive-Ordner (id, name, parents).

`repo` hat die Form "<owner>/<repo>". Bei dauerhaftem Fehler (2 Versuche) wird RuntimeError ausgelöst: dann stoppen
und den Nutzer benachrichtigen, nicht weiter wiederholen (siehe LERNEN.md).
"""
import base64
import contextlib
import io
import os
import tempfile
import time

import requests

_VERSUCHE = 2
_PAUSE = 5


def _ruhig(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*a, **k)


def _mit_versuchen(was, f):
    letzter = None
    for i in range(_VERSUCHE):
        try:
            return f()
        except Exception as ex:  # noqa: BLE001
            letzter = ex
            if i < _VERSUCHE - 1:
                time.sleep(_PAUSE)
    raise RuntimeError(f"{was} nach {_VERSUCHE} Versuchen fehlgeschlagen: {str(letzter)[:300]}")


def _sha(repo, pfad, branch):
    r, e = _ruhig(proxy_execute, "GET", f"/repos/{repo}/contents/{pfad}", "github", query_params={"ref": branch})  # noqa: F821
    try:
        return r["sha"]
    except Exception:  # noqa: BLE001
        return None


def put_repo(repo, pfad, daten, nachricht, branch="main"):
    body = {"message": nachricht, "content": base64.b64encode(daten).decode(), "branch": branch}

    def tun():
        s = _sha(repo, pfad, branch)
        if s:
            body["sha"] = s
        r, e = _ruhig(proxy_execute, "PUT", f"/repos/{repo}/contents/{pfad}", "github", body=body)  # noqa: F821
        if e:
            raise RuntimeError(str(e))
        return "ok"

    return _mit_versuchen(f"Ablegen von {pfad}", tun)


def audio_to_repo(repo, ordner, urls, branch="main"):
    ergebnis = {}
    for szene, url in urls.items():
        antwort = requests.get(url, timeout=60)
        antwort.raise_for_status()
        daten = antwort.content
        if not daten:
            raise RuntimeError(f"Leere Audiodatei für Block {szene}")
        ergebnis[szene] = put_repo(repo, f"{ordner}/blocks/{szene}.mp3", daten, f"Audio {ordner} {szene}", branch)
    return ergebnis


def in_ordner(name, folder_id):
    r, e = _ruhig(run_composio_tool, "GOOGLEDRIVE_FIND_FILE",  # noqa: F821
                  {"q": f"name = '{name}' and '{folder_id}' in parents and trashed = false"})
    if e:
        raise RuntimeError(str(e))
    return (r or {}).get("data", {}).get("files", [])


def _arbeitsordner():
    return "/home/user" if os.path.isdir("/home/user") else tempfile.gettempdir()


def video_to_drive(repo, repo_pfad, name, folder_id, branch="main"):
    meta, e = _ruhig(proxy_execute, "GET", f"/repos/{repo}/contents/{repo_pfad}", "github",  # noqa: F821
                     query_params={"ref": branch})
    if e or not meta or "sha" not in meta:
        raise RuntimeError(f"Datei {repo_pfad} im Zweig {branch} nicht gefunden: {str(e)[:200]}")
    blob, e2 = _ruhig(proxy_execute, "GET", f"/repos/{repo}/git/blobs/{meta['sha']}", "github")  # noqa: F821
    if e2 or not blob:
        raise RuntimeError(f"Blob von {repo_pfad} nicht lesbar: {str(e2)[:200]}")
    daten = base64.b64decode(blob["content"])
    lokal = os.path.join(_arbeitsordner(), name)
    with open(lokal, "wb") as f:
        f.write(daten)

    def hochladen():
        up, ue = _ruhig(upload_local_file, lokal)  # noqa: F821
        if ue:
            raise RuntimeError(str(ue))
        rr, e3 = _ruhig(run_composio_tool, "GOOGLEDRIVE_UPLOAD_FILE",  # noqa: F821
                        {"file_to_upload": {"name": name, "mimetype": "video/mp4", "s3key": up["s3key"]},
                         "folder_to_upload_to": folder_id})
        if e3:
            raise RuntimeError(str(e3))
        return (rr or {}).get("data", {}).get("id")

    drive_id = _mit_versuchen(f"Upload von {name}", hochladen)
    liegt = any(f.get("id") == drive_id for f in in_ordner(name, folder_id))
    return {"bytes": len(daten), "drive_id": drive_id, "in_ordner": liegt}


def _finde_ordner(name, parent_id=None):
    args = {"name_exact": name}
    if parent_id:
        args["parent_folder_id"] = parent_id
    r, e = _ruhig(run_composio_tool, "GOOGLEDRIVE_FIND_FOLDER", args)  # noqa: F821
    if e:
        raise RuntimeError(str(e))
    daten = (r or {}).get("data", {})
    treffer = daten.get("files") or daten.get("folders") or []
    return [t["id"] for t in treffer if t.get("id") and not t.get("trashed")]


def _ordner(name, parent_id=None):
    def tun():
        ids = _finde_ordner(name, parent_id)
        if ids:
            return ids[0]
        args = {"name": name}
        if parent_id:
            args["parent_id"] = parent_id
        r, e = _ruhig(run_composio_tool, "GOOGLEDRIVE_CREATE_FOLDER", args)  # noqa: F821
        if e:
            raise RuntimeError(str(e))
        return r["data"]["id"]

    return _mit_versuchen(f"Drive-Ordner {name}", tun)


def drive_ordner(kanalname):
    """<kanalname>/erstellt und <kanalname>/gepostet anlegen oder wiederfinden (kein Doppelanlegen)."""
    if not kanalname or not kanalname.strip():
        raise RuntimeError("Kein Kanalname angegeben")
    kanal = _ordner(kanalname.strip())
    return {"kanal": kanal, "erstellt": _ordner("erstellt", kanal), "gepostet": _ordner("gepostet", kanal)}
