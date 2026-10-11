# Craft integration template

The DeckCraft, CADCraft, PhotoCraft, VectorCraft, FilmCraft, EffectCraft, GridCraft and SoundCraft Nextcloud apps are generated from this template, so a fix to the editor page or the Files action reaches all of them. (PdfCraft and WordCraft have their own repositories and came first; the template grew out of the WordCraft app.)

- `app/` is the Nextcloud app with `{{PLACEHOLDERS}}`: the editor page (`src/editor.ts`), the Files action (`src/files.ts`), the PHP controllers, the build and signing scripts, and the README.
- `apps/<id>.json` says what differs per app: its name, the file types it opens, its icon (an original 24×24 path), the canvas it draws in, how its browser build is made, and the README and App Store texts.
- `generate.py apps/<id>.json ../nextcloud-<id>` writes the app. It rewrites the template's files and leaves `patches/`, `screenshots/`, the build output in `web/` and `js/`, and an existing `CHANGELOG.md` alone.

Each app also needs a patch to its upstream project (`patches/<id>-nextcloud.patch` in the app): the embedding bridge in the project's web shell, and for FilmCraft and EffectCraft an `unbranded` feature that leaves out the ArtCraft marks. The bridges are on the `nextcloud-embedding-bridge` branch of each fork (github.com/CyberFox-81/<id>).

Two layouts for the page in the editor's iframe:

- **Routed** (default): `/apps/integration_<id>/frame`, a PHP page whose Content Security Policy allows compiling WebAssembly. The build output has content-hashed names in `web/`.
- **Static** (`"static_frame": true`, FilmCraft and EffectCraft): `web/build-<hash>/frame.html`, for apps that load workers and worklets by relative URLs. Each build is a new folder named in `web/build.txt`, so browsers never mix files of two builds.

## Updating an app

1. Change the template (or the app's JSON), then regenerate: `python3 generate.py apps/<id>.json ../../nextcloud-<id>`.
2. Bump `version` in `apps/<id>.json` (it fills `appinfo/info.xml` and `package.json`), and add a `CHANGELOG.md` entry in the app.
3. In the app: `make js`, `make wasm` (or reuse `web/` when the upstream build didn't change), `make dist`.
4. Publish here: `scripts/update-plugin.py ../nextcloud-<id>/build/dist/integration_<id>-<version>.tar.gz`, commit `integration_<id> <version>` and push.

Building PhotoCraft's `wasm-release` profile with fat LTO needs more than 8 GB of memory; on a smaller machine set `CARGO_PROFILE_WASM_RELEASE_LTO=thin`.
