#!/usr/bin/env bash
# Prüft und installiert, was die Pipeline braucht, und führt dann den Trockenlauf ohne Credits aus.
set -u
fehlt=0
for b in python3 ffmpeg ffprobe; do
  command -v "$b" >/dev/null 2>&1 || { echo "FEHLT: $b"; fehlt=1; }
done
if [ "$fehlt" = 1 ]; then
  if command -v apt-get >/dev/null 2>&1; then
    (apt-get install -y ffmpeg python3 >/dev/null 2>&1 || sudo apt-get install -y ffmpeg python3 >/dev/null 2>&1) || true
  fi
  for b in python3 ffmpeg ffprobe; do
    command -v "$b" >/dev/null 2>&1 || { echo "FEHLER: $b nicht verfügbar, bitte installieren"; exit 1; }
  done
fi
python3 -c "import PIL, requests" 2>/dev/null || pip install --quiet --break-system-packages pillow requests || { echo "FEHLER: pip install pillow requests"; exit 1; }
fc-list 2>/dev/null | grep -qi "dejavu\|liberation\|noto" || echo "HINWEIS: keine Standardschrift gefunden, im look.json eine Schrift angeben"
cd "$(dirname "$0")"
python3 tools/trockenlauf.py projekte/_beispiel projekte/_beispiel/videos/B001 | tail -n 3
