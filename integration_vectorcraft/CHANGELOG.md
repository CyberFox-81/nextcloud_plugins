<!--
  - SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
  - SPDX-License-Identifier: AGPL-3.0-or-later
-->
# Changelog

## 0.1.1 – 2026-10-11

- VectorCraft 0.9.0 (commit 1637165): the latest VectorCraft, with the embedding bridge rebased onto it

## 0.1.0 – 2026-10-10

First release.

- App ID `integration_vectorcraft`: "Edit in VectorCraft" in the Files action menu for SVG, Illustrator, EPS or VectorCraft files (Nextcloud 33–35)
- Editor page with VectorCraft 0.9.0 (commit c9236ed) in an iframe
- Save writes back over WebDAV with conflict detection; new formats and exports ask for a name and folder
- Read-only files save as a copy
- Optional "open drawings in VectorCraft when clicked", per user, with an admin default
