<!--
  - SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
  - SPDX-License-Identifier: AGPL-3.0-or-later
-->
# {{NAME}} integration for Nextcloud

Open and edit the files in your Nextcloud with [{{NAME}}](https://github.com/storytold/{{ID}}), the open-source, Rust-native {{KIND}}, without leaving the browser.

{{README_FEATURES}}
- If someone else changes the file while you have it open, saving asks whether to replace their version or save a copy.
- Read-only files (for example a share without edit rights) open normally; saving offers a copy.
- Optionally, clicking a {{NOUN}} in Files opens it in {{NAME}}: tick **Open {{NOUNS}} here from Files** in the editor's top bar.

{{NAME}} runs entirely in your browser as WebAssembly. Files go only between your browser and your Nextcloud; there is no extra server to run.

## Requirements

- Nextcloud 33, 34 or 35
- A browser with WebGPU or WebGL2 (any current Chrome, Edge, Firefox or Safari)
- The web server must serve `.wasm` files as `application/wasm`. Nextcloud's own `.htaccess` does this on Apache; the [recommended nginx configuration](https://docs.nextcloud.com/server/latest/admin_manual/installation/nginx.html) does too.
- Recommended: gzip or Brotli for `application/wasm`. {{NAME}} is fetched once and then cached.

## Install

Until the app is in the Nextcloud App Store, the latest version is in [CyberFox-81/nextcloud_plugins](https://github.com/CyberFox-81/nextcloud_plugins), whose README has step-by-step commands for Docker, Nextcloud AIO and regular servers. In short:

1. Download [`{{APP_ID}}.tar.gz`](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/{{APP_ID}}/{{APP_ID}}.tar.gz) and extract it into your Nextcloud's `custom_apps/` (or `apps/`) folder, so you have `custom_apps/{{APP_ID}}/appinfo/info.xml`.
2. Make it readable by the web server user, e.g. `chown -R www-data:www-data custom_apps/{{APP_ID}}`.
3. Enable it: `sudo -u www-data php occ app:enable {{APP_ID}}`. In Docker: `docker exec -u www-data nextcloud php occ app:enable {{APP_ID}}`.

To make {{NAME}} the click-to-open default for every user who hasn't chosen otherwise:

```sh
sudo -u www-data php occ config:app:set {{APP_ID}} open_by_default --value=true --type=boolean
```

## How it works

```
Files ── "Edit in {{NAME}}" ──▶ /apps/{{APP_ID}}/edit/{fileId}   (src/editor.ts)
                                  │  WebDAV GET/PUT with the user's session
                                  ▼
                                <iframe> /apps/{{APP_ID}}/frame?host=parent   (templates/frame.php)
                                  │  {{NAME}} (web/*.wasm) — postMessage bridge
```

The editor page downloads the file over WebDAV and passes it to {{NAME}} with `postMessage`. When you save, {{NAME}} passes the bytes back and the page uploads them with `If-Match`, so a newer version on the server is never overwritten without asking. A save in a format the opened file isn't in, and an export, ask for a name and folder with Nextcloud's own folder picker the first time; later saves under the same name go to the same file. The frame page is the only one whose Content Security Policy allows compiling WebAssembly.

{{NAME}}'s browser build saves by downloading a file. `patches/{{ID}}-nextcloud.patch` adds an opt-in embedding bridge (`?host=parent`) to its web shell{{PATCH_EXTRA}}; the protocol is in [web/README.md](web/README.md). It is meant to be proposed upstream, so a future official {{NAME}} build can be used as is.

## Build from source

```sh
make js      # npm ci && vite build → js/
make wasm    # clone {{NAME}}, apply the patch, build → web/   (needs Rust, see below)
make dist    # → build/dist/{{APP_ID}}-<version>.tar.gz
```

`make wasm` runs `scripts/build-{{ID}}-web.sh`, which needs the `wasm32-unknown-unknown` Rust target, `wasm-bindgen-cli` at the version in {{NAME}}'s `Cargo.lock` ({{BINDGEN_VERSION}} at the pinned commit), and optionally `wasm-opt` from binaryen. Set `{{ID_UPPER}}_REF` to build another {{NAME}} commit, `FAST=1` for quicker development builds, and `CRAFT_FONTS_DIR` to a clone of [storytold/craft-fonts](https://github.com/storytold/craft-fonts) to embed the shared Japanese fonts.

For development, `npm run watch` rebuilds the scripts as you edit; symlink or copy the repository into `custom_apps/{{APP_ID}}` of a test server.

## Releasing to the App Store

One-time setup (see the [App Store developer guide](https://nextcloudappstore.readthedocs.io/en/latest/developer.html)):

1. Create the app's key and certificate request, and keep the key private and backed up:
   ```sh
   mkdir -p ~/.nextcloud/certificates && cd ~/.nextcloud/certificates
   openssl req -nodes -newkey rsa:4096 -keyout {{APP_ID}}.key -out {{APP_ID}}.csr -subj "/CN={{APP_ID}}"
   ```
2. Submit `{{APP_ID}}.csr` as `{{APP_ID}}/{{APP_ID}}.csr` in a pull request to [nextcloud/app-certificate-requests](https://github.com/nextcloud/app-certificate-requests). Save the signed certificate they reply with as `~/.nextcloud/certificates/{{APP_ID}}.crt`.
3. Register the app at [apps.nextcloud.com/developer/apps/new](https://apps.nextcloud.com/developer/apps/new) with the certificate and this signature:
   ```sh
   echo -n "{{APP_ID}}" | openssl dgst -sha512 -sign ~/.nextcloud/certificates/{{APP_ID}}.key | openssl base64
   ```

Each release:

```sh
make js && make wasm
scripts/sign-release.sh --key ~/.nextcloud/certificates/{{APP_ID}}.key \
  --cert ~/.nextcloud/certificates/{{APP_ID}}.crt --docker nextcloud
```

The script code-signs the app with `occ integrity:sign-app` (borrowed from a running Nextcloud container, or `--occ` for a local install; `--archive` signs a prebuilt archive), packs `{{APP_ID}}-<version>.tar.gz` and prints the App Store signature. Attach the archive to a GitHub release, then submit its download URL and the signature at [apps.nextcloud.com/developer/apps/releases/new](https://apps.nextcloud.com/developer/apps/releases/new).

Every new version also goes to [nextcloud_plugins](https://github.com/CyberFox-81/nextcloud_plugins), replacing the previous one, with that repository's script (from a clone next to this one):

```sh
../nextcloud_plugins/scripts/update-plugin.py build/dist/{{APP_ID}}-<version>.tar.gz
```

## Limitations

- {{NAME}} is young; see its [roadmap](https://github.com/storytold/{{ID}}/blob/main/ROADMAP.md) for what's still missing.
- One person edits at a time. There is no live co-editing; concurrent saves are caught and you choose what happens.
{{README_LIMITATIONS}}
## License

This app is licensed under the AGPL-3.0-or-later. {{NAME}}, bundled in `web/`, is licensed under MIT OR Apache-2.0; its bundled fonts and assets carry their own open licenses (see `web/{{ID_UPPER}}-ATTRIBUTION.md` or `web/{{ID_UPPER}}-NOTICE`). This is a community integration based on {{NAME}} by the ArtCraft team, not made or endorsed by them.
