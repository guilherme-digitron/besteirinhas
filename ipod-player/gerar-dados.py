#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lê a pasta playlists/ e escreve data.js ao lado do index.html.
Rode sempre que adicionar ou remover músicas:

    python gerar-dados.py
"""

import json
import os
import re
import sys

AUDIO = (".mp3", ".m4a", ".ogg", ".wav", ".flac", ".aac", ".opus", ".webm")
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "playlists")


def natural(name):
    """Ordena Section 2 antes de Section 10."""
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", name)]


def title_of(filename):
    name = os.path.splitext(filename)[0]
    return re.sub(r"\s+", " ", name.replace("_", ":")).strip()


def main():
    if not os.path.isdir(ROOT):
        sys.exit("Não achei a pasta 'playlists' ao lado deste script.")

    playlists = []
    for folder in sorted(os.listdir(ROOT), key=natural):
        path = os.path.join(ROOT, folder)
        if not os.path.isdir(path):
            continue
        files = sorted(
            (f for f in os.listdir(path) if f.lower().endswith(AUDIO)), key=natural
        )
        if not files:
            continue
        playlists.append(
            {
                "name": folder,
                "tracks": [
                    {"title": title_of(f), "src": "playlists/%s/%s" % (folder, f)}
                    for f in files
                ],
            }
        )

    # Áudios soltos direto em playlists/
    loose = sorted(
        (f for f in os.listdir(ROOT) if f.lower().endswith(AUDIO)), key=natural
    )
    if loose:
        playlists.insert(
            0,
            {
                "name": "Músicas soltas",
                "tracks": [
                    {"title": title_of(f), "src": "playlists/%s" % f} for f in loose
                ],
            },
        )

    if not playlists:
        sys.exit("Nenhum áudio encontrado dentro de 'playlists'.")

    out = "window.PLAYLISTS = %s;\n" % json.dumps(
        playlists, ensure_ascii=False, indent=2
    )
    with open(os.path.join(BASE, "data.js"), "w", encoding="utf-8") as fh:
        fh.write(out)

    total = sum(len(p["tracks"]) for p in playlists)
    print("data.js criado: %d playlist(s), %d faixa(s)." % (len(playlists), total))
    for p in playlists:
        print("  - %s (%d)" % (p["name"], len(p["tracks"])))


if __name__ == "__main__":
    main()
