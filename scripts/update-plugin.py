#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Put a new version of a Nextcloud app into this repository, replacing the old one.

Usage: scripts/update-plugin.py PATH/TO/<app_id>-<version>.tar.gz [...]

For each archive (as built by the app's `make dist`):
  - checks it holds exactly one app folder with appinfo/info.xml
  - stores it as <app_id>/<app_id>.tar.gz, replacing the previous version
  - copies the app's CHANGELOG.md next to it
  - rewrites SHA256SUMS and the app table in README.md

Then review `git diff --stat` and commit, e.g. "integration_pdfcraft 0.1.1".
"""

import hashlib
import shutil
import sys
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SUMS = ROOT / "SHA256SUMS"
RAW = "https://github.com/CyberFox-81/nextcloud_plugins/raw/main"
START, END = "<!-- plugins:start -->", "<!-- plugins:end -->"


def fail(message: str) -> None:
    sys.exit(f"error: {message}")


def read_app(archive: Path) -> dict:
    """The app's id, folder and info.xml fields, after checking the archive's layout."""
    try:
        with tarfile.open(archive, "r:gz") as tar:
            names = tar.getnames()
            tops = {n.split("/", 1)[0] for n in names if n and not n.startswith("./")}
            if len(tops) != 1 or any(n.startswith("/") or ".." in n.split("/") for n in names):
                fail(f"{archive}: expected one app folder at the top, found {sorted(tops)}")
            folder = tops.pop()
            info = tar.extractfile(f"{folder}/appinfo/info.xml")
            changelog_member = f"{folder}/CHANGELOG.md"
            changelog = tar.extractfile(changelog_member).read() if changelog_member in names else None
            root = ET.fromstring(info.read()) if info else fail(f"{archive}: no {folder}/appinfo/info.xml")
    except (tarfile.TarError, OSError, KeyError, ET.ParseError) as error:
        fail(f"{archive}: {error}")
    app_id = (root.findtext("id") or "").strip()
    if app_id != folder:
        fail(f"{archive}: the folder is {folder!r} but info.xml says the app id is {app_id!r}")
    nc = root.find("dependencies/nextcloud")
    return {
        "id": app_id,
        "name": (root.findtext("name") or app_id).strip(),
        "summary": " ".join((root.findtext("summary") or "").split()),
        "version": (root.findtext("version") or "").strip(),
        "nextcloud": f"{nc.get('min-version')}–{nc.get('max-version')}" if nc is not None else "",
        "changelog": changelog,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def stored_archives() -> list[Path]:
    return sorted(p for p in ROOT.glob("*/*.tar.gz") if p.name == f"{p.parent.name}.tar.gz")


def refresh_index() -> None:
    rows, sums = [], []
    for archive in stored_archives():
        app = read_app(archive)
        link = f"[{archive.name}]({RAW}/{app['id']}/{archive.name})"
        rows.append(
            f"| **{app['name']}** (`{app['id']}`) | {app['version']} | {app['nextcloud']} | "
            f"{app['summary']} | {link} · [changes]({app['id']}/CHANGELOG.md) |"
        )
        sums.append(f"{sha256(archive)}  {archive.name}")
    table = "\n".join(
        ["| App | Version | Nextcloud | What it does | Download |", "|---|---|---|---|---|", *rows]
    )
    SUMS.write_text("\n".join(sums) + "\n")
    text = README.read_text()
    if START not in text or END not in text:
        fail(f"README.md needs the {START} and {END} markers")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    README.write_text(f"{before}{START}\n{table}\n{END}{after}")


def main() -> None:
    archives = [Path(a) for a in sys.argv[1:]]
    if not archives:
        sys.exit(__doc__)
    for archive in archives:
        app = read_app(archive)
        folder = ROOT / app["id"]
        folder.mkdir(exist_ok=True)
        target = folder / f"{app['id']}.tar.gz"
        old = read_app(target)["version"] if target.exists() else None
        shutil.copyfile(archive, target)
        if app["changelog"] is not None:
            (folder / "CHANGELOG.md").write_bytes(app["changelog"])
        print(f"{app['id']}: {old or '(new)'} → {app['version']}")
    refresh_index()
    print("Updated README.md and SHA256SUMS. Review with `git status`, then commit.")


if __name__ == "__main__":
    main()
