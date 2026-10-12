<!--
  - SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
  - SPDX-License-Identifier: AGPL-3.0-or-later
-->
# Changelog

## 0.1.1 – 2026-10-12

- LightCraft 0.7.1 (commit 701f78e): the latest LightCraft, with the embedding bridge rebased onto it

## 0.1.0 – 2026-10-11

First release.

- App ID `integration_lightcraft`: "Edit in LightCraft" in the Files action menu for photo or camera raw files (Nextcloud 33–35)
- Editor page with LightCraft 0.6.0 (commit 0ba118d) in an iframe
- Save writes back over WebDAV with conflict detection; new formats and exports ask for a name and folder
- Read-only files save as a copy
- Optional "open photos in LightCraft when clicked", per user, with an admin default
