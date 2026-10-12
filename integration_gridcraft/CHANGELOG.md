<!--
  - SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
  - SPDX-License-Identifier: AGPL-3.0-or-later
-->
# Changelog

## 0.1.2 – 2026-10-12

- GridCraft 0.6.1 (commit fc45b7f): the latest GridCraft, with the embedding bridge rebased onto it

## 0.1.1 – 2026-10-11

- GridCraft 0.5.0 (commit 3926d21): the latest GridCraft, with the embedding bridge rebased onto it
- Opens legacy Excel workbooks (.xls) too; like the other formats, they're saved as a new .xlsx file

## 0.1.0 – 2026-10-10

First release.

- App ID `integration_gridcraft`: "Edit in GridCraft" in the Files action menu for Excel, OpenDocument or CSV files (Nextcloud 33–35)
- Editor page with GridCraft 0.5.0 (commit 9f896c1) in an iframe
- Save writes back over WebDAV with conflict detection; new formats and exports ask for a name and folder
- Read-only files save as a copy
- Optional "open workbooks in GridCraft when clicked", per user, with an admin default
