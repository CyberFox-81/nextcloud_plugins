# Nextcloud plugins

Ready-to-install Nextcloud apps by [CyberFox-81](https://github.com/CyberFox-81) that aren't in the Nextcloud App Store yet. Each app has its own folder with the **latest version only**; a new version replaces the old one. Until an app is in the App Store, install it by hand as described below.

<!-- plugins:start -->
| App | Version | Nextcloud | What it does | Download |
|---|---|---|---|---|
| **CADCraft integration** (`integration_cadcraft`) | 0.1.3 | 33–35 | Open and edit DXF and DWG drawings in Nextcloud with CADCraft | [integration_cadcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_cadcraft/integration_cadcraft.tar.gz) · [changes](integration_cadcraft/CHANGELOG.md) |
| **DeckCraft integration** (`integration_deckcraft`) | 0.1.2 | 33–35 | Edit PowerPoint presentations in Nextcloud with DeckCraft | [integration_deckcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_deckcraft/integration_deckcraft.tar.gz) · [changes](integration_deckcraft/CHANGELOG.md) |
| **DesignCraft integration** (`integration_designcraft`) | 0.1.2 | 33–35 | Edit page layouts in Nextcloud with DesignCraft | [integration_designcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_designcraft/integration_designcraft.tar.gz) · [changes](integration_designcraft/CHANGELOG.md) |
| **EffectCraft integration** (`integration_effectcraft`) | 0.1.3 | 33–35 | Make motion graphics and effects in Nextcloud with EffectCraft | [integration_effectcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_effectcraft/integration_effectcraft.tar.gz) · [changes](integration_effectcraft/CHANGELOG.md) |
| **FilmCraft integration** (`integration_filmcraft`) | 0.1.3 | 33–35 | Edit videos in Nextcloud with the FilmCraft video editor | [integration_filmcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_filmcraft/integration_filmcraft.tar.gz) · [changes](integration_filmcraft/CHANGELOG.md) |
| **GridCraft integration** (`integration_gridcraft`) | 0.1.3 | 33–35 | Edit Excel spreadsheets in Nextcloud with GridCraft | [integration_gridcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_gridcraft/integration_gridcraft.tar.gz) · [changes](integration_gridcraft/CHANGELOG.md) |
| **LightCraft integration** (`integration_lightcraft`) | 0.1.1 | 33–35 | Develop photos and camera raws from Nextcloud with LightCraft | [integration_lightcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_lightcraft/integration_lightcraft.tar.gz) · [changes](integration_lightcraft/CHANGELOG.md) |
| **PdfCraft integration** (`integration_pdfcraft`) | 0.1.7 | 33–35 | Edit PDFs in your Nextcloud with the PdfCraft PDF workbench | [integration_pdfcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_pdfcraft/integration_pdfcraft.tar.gz) · [changes](integration_pdfcraft/CHANGELOG.md) |
| **PhotoCraft integration** (`integration_photocraft`) | 0.1.5 | 33–35 | Edit photos and Photoshop files in Nextcloud with PhotoCraft | [integration_photocraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_photocraft/integration_photocraft.tar.gz) · [changes](integration_photocraft/CHANGELOG.md) |
| **SoundCraft integration** (`integration_soundcraft`) | 0.1.2 | 33–35 | Edit audio and SoundCraft sessions in Nextcloud with SoundCraft | [integration_soundcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_soundcraft/integration_soundcraft.tar.gz) · [changes](integration_soundcraft/CHANGELOG.md) |
| **VectorCraft integration** (`integration_vectorcraft`) | 0.1.3 | 33–35 | Edit SVG and Illustrator files in Nextcloud with VectorCraft | [integration_vectorcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_vectorcraft/integration_vectorcraft.tar.gz) · [changes](integration_vectorcraft/CHANGELOG.md) |
| **WordCraft integration** (`integration_wordcraft`) | 0.1.3 | 33–35 | Write and edit Word and OpenDocument files in Nextcloud with the WordCraft word processor | [integration_wordcraft.tar.gz](https://github.com/CyberFox-81/nextcloud_plugins/raw/main/integration_wordcraft/integration_wordcraft.tar.gz) · [changes](integration_wordcraft/CHANGELOG.md) |
<!-- plugins:end -->

Source code: [integration_pdfcraft](https://github.com/CyberFox-81/integration_pdfcraft), [integration_wordcraft](https://github.com/CyberFox-81/integration_wordcraft), [integration_deckcraft](https://github.com/CyberFox-81/integration_deckcraft), [integration_cadcraft](https://github.com/CyberFox-81/integration_cadcraft), [integration_photocraft](https://github.com/CyberFox-81/integration_photocraft), [integration_vectorcraft](https://github.com/CyberFox-81/integration_vectorcraft), [integration_filmcraft](https://github.com/CyberFox-81/integration_filmcraft), [integration_effectcraft](https://github.com/CyberFox-81/integration_effectcraft), [integration_gridcraft](https://github.com/CyberFox-81/integration_gridcraft), [integration_soundcraft](https://github.com/CyberFox-81/integration_soundcraft), [integration_designcraft](https://github.com/CyberFox-81/integration_designcraft); integration_lightcraft's repository is coming soon. Checksums: [SHA256SUMS](SHA256SUMS).

## Before you start

- **Nextcloud 33, 34 or 35**, and admin access to the server (a shell, or `docker exec` for Docker).
- **Browsers** need WebGPU or WebGL2: any current Chrome, Edge, Firefox or Safari.
- **The web server must serve `.wasm` files as `application/wasm`.** Nextcloud's own Apache `.htaccess`, the official Docker images and Nextcloud AIO already do. On nginx, use the [recommended Nextcloud configuration](https://docs.nextcloud.com/server/latest/admin_manual/installation/nginx.html), which adds the type.
- Install into **`custom_apps`**, not `apps`. `apps` belongs to Nextcloud and is replaced by updates (in Docker, by a new image), while `custom_apps` is kept.

In the commands below, set `APP` to the app you want, for example `APP=integration_pdfcraft` or `APP=integration_wordcraft`. Repeat the steps for each app.

## Install

### Docker (official `nextcloud` image)

Run on the Docker host. `docker ps` shows your container's name; it's often `nextcloud`.

```sh
APP=integration_pdfcraft
CONTAINER=nextcloud

curl -fLO "https://github.com/CyberFox-81/nextcloud_plugins/raw/main/$APP/$APP.tar.gz"
docker cp "$APP.tar.gz" "$CONTAINER":/tmp/
docker exec "$CONTAINER" sh -c "cd /var/www/html/custom_apps && rm -rf $APP && tar -xzf /tmp/$APP.tar.gz && rm /tmp/$APP.tar.gz && chown -R www-data:www-data $APP"
docker exec -u www-data "$CONTAINER" php occ app:enable "$APP"
rm "$APP.tar.gz"
```

Don't mount a separate volume over `/var/www/html/apps`: it hides the apps Nextcloud ships with, and `occ` then fails with errors such as `QueryNotFoundException`. The `/var/www/html` volume already keeps `custom_apps`.

### Nextcloud All-in-One (AIO)

The same as Docker, with the AIO container:

```sh
APP=integration_pdfcraft
CONTAINER=nextcloud-aio-nextcloud

curl -fLO "https://github.com/CyberFox-81/nextcloud_plugins/raw/main/$APP/$APP.tar.gz"
sudo docker cp "$APP.tar.gz" "$CONTAINER":/tmp/
sudo docker exec "$CONTAINER" sh -c "cd /var/www/html/custom_apps && rm -rf $APP && tar -xzf /tmp/$APP.tar.gz && rm /tmp/$APP.tar.gz && chown -R www-data:www-data $APP"
sudo docker exec --user www-data "$CONTAINER" php occ app:enable "$APP"
rm "$APP.tar.gz"
```

### Regular server (Apache or nginx)

Replace `/var/www/nextcloud` with your Nextcloud folder, and `www-data` with your web server's user if it differs (`apache` on Fedora/RHEL, `nginx` on some setups).

```sh
APP=integration_pdfcraft
NC=/var/www/nextcloud

cd "$NC/custom_apps"
sudo curl -fLO "https://github.com/CyberFox-81/nextcloud_plugins/raw/main/$APP/$APP.tar.gz"
sudo rm -rf "$APP" && sudo tar -xzf "$APP.tar.gz" && sudo rm "$APP.tar.gz"
sudo chown -R www-data:www-data "$APP"
sudo -u www-data php "$NC/occ" app:enable "$APP"
```

If your Nextcloud has no `custom_apps` folder, use `apps` instead.

### Check it worked

Reload Files in the browser. The files each app handles get an **Edit in …** entry in their **⋯** menu:

| App | Files |
|---|---|
| PdfCraft | PDF |
| WordCraft | Word (.docx, .doc…), OpenDocument text, RTF |
| DeckCraft | PowerPoint (.pptx, .potx, .ppsx), DeckCraft |
| CADCraft | DXF, DWG |
| PhotoCraft | PNG, JPEG, TIFF, WebP, HEIC, camera raw, Photoshop (PSD, PSB), PhotoCraft… |
| VectorCraft | SVG, Illustrator (.ai), EPS, VectorCraft |
| FilmCraft | Videos (MP4, MOV, WebM, MKV, MXF, MPEG-TS), FilmCraft projects |
| EffectCraft | EffectCraft projects, videos (MP4, MOV, WebM) |
| GridCraft | Excel (.xlsx, .xlsm, .xlsb, .xltx), OpenDocument spreadsheets (.ods), CSV, TSV |
| SoundCraft | Audio (WAV, AIFF, FLAC, MP3, Ogg Vorbis, AAC/M4A, CAF), SoundCraft sessions (.scraft) and session bundles (.scraftz) |
| DesignCraft | DesignCraft documents (.designcraft), IDML packages (.idml) |
| LightCraft | Photos (JPEG, PNG, TIFF, WebP, GIF, BMP, JPEG XL) and camera raws (DNG, CR2, NEF, ARW) |

A file that several apps open lists each of them. `occ app:list | grep integration_` lists the installed apps and their versions.

### Optional: check the download

Right after the `curl -fLO` step, in the same folder, you can compare the archive with the checksum published here; it should print `OK`:

```sh
curl -fLO https://github.com/CyberFox-81/nextcloud_plugins/raw/main/SHA256SUMS
sha256sum -c --ignore-missing SHA256SUMS
```

## Update

When this repository has a newer version, repeat the install steps for that app: they remove the old folder before unpacking the new one, so no leftover files remain. Then finish the update:

```sh
sudo -u www-data php "$NC/occ" upgrade                          # regular server
docker exec -u www-data "$CONTAINER" php occ upgrade             # Docker
sudo docker exec --user www-data "$CONTAINER" php occ upgrade    # AIO
```

Each app's `CHANGELOG.md` (linked in the table) says what changed.

## Remove

```sh
sudo -u www-data php "$NC/occ" app:remove "$APP"                 # regular server
docker exec -u www-data "$CONTAINER" php occ app:remove "$APP"    # Docker (AIO: sudo docker exec --user www-data …)
```

This disables the app and deletes its folder. Your files in Nextcloud are not touched.

## Troubleshooting

- **The "Edit in …" entry doesn't appear:** reload the page with the cache bypassed (Ctrl+Shift+R), and check `occ app:list` shows the app as enabled.
- **"App … cannot be installed because it is not compatible with this version":** these apps support Nextcloud 33–35.
- **The editor stays on "Loading…" or says it couldn't start:** the browser needs WebGL2 or WebGPU (check hardware acceleration is on). If the browser console shows a wasm MIME type error, the web server isn't sending `application/wasm` for `.wasm` files (see [Before you start](#before-you-start)).
- **Two "Edit in PdfCraft" entries:** an early test build used the app id `pdfcraft`. Remove it with `occ app:remove pdfcraft`.
- **Videos or projects open slowly:** FilmCraft and EffectCraft load the media into the browser first, so large files take a while and need memory; a render or saved project is uploaded when it finishes, so keep the tab open until then.
- **Code-integrity warnings:** none are expected. These archives aren't signed for the App Store yet, and Nextcloud only checks apps that ship a signature.

## Licenses

Each app is licensed under the AGPL-3.0-or-later; see the `LICENSE` file inside its archive. PdfCraft and WordCraft, bundled inside the apps, are by the ArtCraft team under MIT OR Apache-2.0; these apps are community integrations, not made or endorsed by the ArtCraft team.

## Maintainers: publishing a new version

Build the app's archive (`make dist` in its repository), then:

```sh
scripts/update-plugin.py ../integration_pdfcraft/build/dist/integration_pdfcraft-0.1.1.tar.gz
git add -A && git commit -m "integration_pdfcraft 0.1.1" && git push
```

The script replaces that app's archive and `CHANGELOG.md`, and rewrites `SHA256SUMS` and the table above. Never commit App Store signing keys (`*.key`) here.

DeckCraft, CADCraft, PhotoCraft, VectorCraft, FilmCraft and EffectCraft are generated from one template, kept in [`template/`](template/README.md) with how to regenerate and release them.
