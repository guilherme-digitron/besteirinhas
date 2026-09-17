#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lê a pasta playlists/ e escreve data.js ao lado do index.html.
Cada subpasta que contenha áudio vira uma playlist (inclusive subpastas de subpastas).

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
        print("Aviso: não achei a pasta 'playlists'. Nada a fazer.")
        return

    playlists = []
    for folder, dirs, files in os.walk(ROOT):
        dirs.sort(key=natural)
        audio = sorted((f for f in files if f.lower().endswith(AUDIO)), key=natural)
        if not audio:
            continue
        rel = os.path.relpath(folder, ROOT).replace(os.sep, "/")
        name = "Músicas soltas" if rel == "." else rel.replace("/", " / ")
        prefix = "playlists/" if rel == "." else "playlists/%s/" % rel
        playlists.append(
            {
                "name": name,
                "tracks": [
                    {"title": title_of(f), "src": prefix + f} for f in audio
                ],
            }
        )

    if not playlists:
        print("Aviso: nenhum áudio encontrado dentro de 'playlists'.")
        return

    playlists.sort(key=lambda p: natural(p["name"]))

    out = "window.PLAYLISTS = %s;\n" % json.dumps(playlists, ensure_ascii=False, indent=2)
    with open(os.path.join(BASE, "data.js"), "w", encoding="utf-8") as fh:
        fh.write(out)

    total = sum(len(p["tracks"]) for p in playlists)
    print("data.js criado: %d playlist(s), %d faixa(s)." % (len(playlists), total))
    for p in playlists:
        print("  - %s (%d)" % (p["name"], len(p["tracks"])))


if __name__ == "__main__":
    main()
