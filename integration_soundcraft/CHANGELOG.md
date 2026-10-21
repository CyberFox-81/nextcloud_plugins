<!--
  - SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
  - SPDX-License-Identifier: AGPL-3.0-or-later
-->
# Changelog

## 0.1.4 – 2026-10-21

- SoundCraft 0.11.0 (commit 30ef830): the latest SoundCraft, with the embedding bridge rebased onto it

## 0.1.3 – 2026-10-14

- SoundCraft 0.7.0 (commit 3a28a65): the latest SoundCraft, with the embedding bridge rebased onto it

## 0.1.2 – 2026-10-12

- SoundCraft 0.6.1 (commit 6cf896e): the latest SoundCraft, with the embedding bridge rebased onto it

## 0.1.1 – 2026-10-11

- SoundCraft 0.5.0 (commit acb08ff), which saves sessions in the browser as one bundle file (.scraftz). Save now stores the session and its audio in a bundle instead of a .scraft file with an Audio Files folder; sessions saved that way (by 0.1.0, or by SoundCraft on a computer and synced to Nextcloud) still open with their audio, and save as a bundle next to them.
- The embedding bridge only touches SoundCraft's web shell now: it builds on SoundCraft's own browser file handling, so the engine changes of 0.1.0 are gone.
- File › Import reads audio and MIDI from your computer.

## 0.1.0 – 2026-10-10

First release.

- App ID `integration_soundcraft`: "Edit in SoundCraft" in the Files action menu for audio or SoundCraft files (Nextcloud 33–35)
- Editor page with SoundCraft 0.5.0 (commit 7414719) in an iframe
- Save writes back over WebDAV with conflict detection; new formats and exports ask for a name and folder
- Read-only files save as a copy
- Optional "open sessions in SoundCraft when clicked", per user, with an admin default
