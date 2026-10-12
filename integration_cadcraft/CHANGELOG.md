<!--
  - SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
  - SPDX-License-Identifier: AGPL-3.0-or-later
-->
# Changelog

## 0.1.3 – 2026-10-12

- CADCraft 0.6.2 (commit 00c7613), which includes the embedding bridge this app uses (storytold/cadcraft#509): the official CADCraft build is used as is, without a patch

## 0.1.2 – 2026-10-11

- CADCraft 0.5.0 (commit c57879a), which includes the embedding bridge this app uses (storytold/cadcraft#509): the official CADCraft build is used as is, without a patch

## 0.1.1 – 2026-10-11

- CADCraft 0.5.0 (commit 699dd1a): the latest CADCraft, with the embedding bridge rebased onto it

## 0.1.0 – 2026-10-10

First release.

- App ID `integration_cadcraft`: "Edit in CADCraft" in the Files action menu for DXF or DWG files (Nextcloud 33–35)
- Editor page with CADCraft 0.5.0 (commit fc4220e) in an iframe
- Save writes back over WebDAV with conflict detection; new formats and exports ask for a name and folder
- Read-only files save as a copy
- Optional "open drawings in CADCraft when clicked", per user, with an admin default
