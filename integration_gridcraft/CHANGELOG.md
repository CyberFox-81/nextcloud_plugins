<!--
  - SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
  - SPDX-License-Identifier: AGPL-3.0-or-later
-->
# Changelog

## 0.1.6 – 2026-10-27

- GridCraft 0.12.1 (commit 89ac453), which includes the embedding bridge this app uses (storytold/gridcraft#237): the official GridCraft build is used as is, without a patch

## 0.1.5 – 2026-10-21

- GridCraft 0.10.0 (commit 8ae67c5), which includes the embedding bridge this app uses (storytold/gridcraft#237): the official GridCraft build is used as is, without a patch

## 0.1.4 – 2026-10-16

- GridCraft 0.7.0 (commit f1894c6), which includes the embedding bridge this app uses (storytold/gridcraft#237): the official GridCraft build is used as is, without a patch

## 0.1.3 – 2026-10-14

- GridCraft 0.7.0 (commit d9d09f0), which includes the embedding bridge this app uses (storytold/gridcraft#237): the official GridCraft build is used as is, without a patch

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
