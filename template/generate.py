#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Generate (or refresh) a Nextcloud app for one of the Craft apps from app/ and a config.

Usage: generate.py apps/<id>.json OUT_DIR

Files from the template are (re)written; patches/, screenshots/, web/ build output, js/,
node_modules/ and an existing CHANGELOG.md are left alone.
"""

import datetime
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "app"
KEEP_IF_PRESENT = {"CHANGELOG.md"}


def values(cfg: dict) -> dict:
    app_id = f"integration_{cfg['id']}"
    mimes = cfg["mimes"]
    v = {
        "APP_ID": app_id,
        "ID": cfg["id"],
        "ID_UPPER": cfg["id"].upper(),
        "NAME": cfg["name"],
        "NAMESPACE": f"{cfg['name']}Integration",
        "KIND": cfg["kind"],
        "NOUN": cfg["noun"],
        "NOUNS": cfg["nouns"],
        "NOUNS_CAPITAL": cfg["nouns"][:1].upper() + cfg["nouns"][1:],
        "FILE_TYPES": cfg["file_types"],
        "SUMMARY": cfg["summary"],
        "DESCRIPTION": cfg["description"].strip(),
        "MIME_TYPES_PHP": "\n".join(f"\t\t'{m}'," for m in mimes),
        "MIME_TYPES_TS": "\n".join(f"\t'{m}'," for m in mimes),
        "EXTENSIONS_PHP": "\n".join(f"\t\t'{e}'," for e in cfg.get("extensions", [])),
        "EXTENSIONS_TS": ", ".join(f"'{e}'" for e in cfg.get("extensions", [])),
        "DOCUMENT_EXTENSIONS_TS": ", ".join(f"'{e}'" for e in cfg["document_extensions"]),
        "CATEGORIES_XML": "\n".join(f"\t<category>{c}</category>" for c in cfg["categories"]),
        "CANVAS_ID": cfg["canvas_id"],
        "LOADING_ID": cfg.get("loading_id", f"{cfg['id']}_loading"),
        "FRAME_EXTRA_HTML": cfg.get("frame_extra_html", ""),
        "FRAME_CSP_PHP": "".join(f"\t\t{line}\n" for line in cfg.get("frame_csp_php", [])),
        "BACKGROUND": cfg.get("background", "#262626"),
        "BACKGROUND_DARK": cfg.get("background_dark", "#1e1e20"),
        "ICON_PATH": cfg["icon_path"],
        "README_FEATURES": cfg["readme_features"].strip(),
        "README_LIMITATIONS": cfg.get("readme_limitations", "").strip() + ("\n" if cfg.get("readme_limitations") else ""),
        "PATCH_EXTRA": cfg.get("patch_extra", ""),
        "BINDGEN_VERSION": cfg.get("bindgen_version", "0.2.129"),
        "DEFAULT_REF": cfg["upstream_ref"],
        "UPSTREAM_SHORT": cfg["upstream_ref"][:7],
        "UPSTREAM_VERSION": cfg["upstream_version"],
        "APP_VERSION": cfg.get("version", "0.1.0"),
        "CARGO_PACKAGE": cfg.get("cargo_package", f"{cfg['id']}-web"),
        "WASM_FILE": cfg.get("wasm_file", f"{cfg['id']}-web.wasm"),
        "CARGO_FEATURES_ARGS": f" --features {cfg['cargo_features']}" if cfg.get("cargo_features") else "",
        "BINDGEN_FLAGS": "".join(f" {f}" for f in cfg.get("bindgen_flags", [])),
        "WASM_OPT_FLAGS": "".join(f" {f}" for f in cfg.get("wasm_opt_flags", [])),
        "EXTRA_ASSETS_SH": cfg.get("extra_assets_sh", ""),
        "BOOT_BEFORE": cfg.get("boot_before", ""),
        "BOOT_AFTER": cfg.get("boot_after", ""),
        "BOOT_INIT_ARG": cfg.get("boot_init_arg", "new URL('./$WASM_NAME', import.meta.url)"),
        "CARGO_PROFILE": cfg.get("cargo_profile", "release"),
        "BINDGEN_OUT_NAME": cfg.get("bindgen_out_name", f"{cfg['id']}-web"),
        "CARGO_PROFILE_DIR": cfg.get("cargo_profile", "release"),
        "CARGO_PROFILE_ENV": cfg.get("cargo_profile", "release").upper().replace("-", "_"),
        "WASM_OPT_LEVEL": cfg.get("wasm_opt_level", "-Oz"),
        "OPEN_AS_BLOB": "true" if cfg.get("open_as_blob") else "false",
        "NEW_FORMAT_HINT": cfg.get("new_format_hint", "{{NAME}} saves {name} in a different format, so it goes to a new file and the original stays as it is."),
        "WEB_EXTRA_ROWS": "".join(f"{row}\n" for row in cfg.get("web_extra_rows", [])),
        "PICK_SAVE_ROWS": (
            f"| `{cfg['id']}:pick-save` | {cfg['name']} → parent | `id`, `name` | Save As or Export asks where to save; `name` is the suggested file name (its extension sets the format). |\n"
            f"| `{cfg['id']}:picked` | parent → {cfg['name']} | `id`, `path` | The answer; a missing or empty `path` cancels. |\n"
            if cfg.get("pick_save") else ""
        ),
        "BRIDGE_NOTES": cfg.get("bridge_notes", "").strip(),
        "DATE": datetime.date.today().isoformat(),
        **frame_values(cfg),
    }
    return v


ROUTED_FRAME_URL = """$this->urlGenerator->linkToRoute(Application::APP_ID . '.frame.index', [
				'host' => 'parent',
				'author' => $user->getDisplayName(),
			])"""

STATIC_FRAME_PHP = """	/**
	 * The current build's frame.html (web/build-<hash>/, named in web/build.txt). A static page,
	 * so the app's relative URLs (its workers, worklets and data files) resolve inside its build
	 * folder, which a new version replaces as a whole: nothing is served from a stale cache.
	 */
	private function staticFrameUrl(string $author): string {
		$file = __DIR__ . '/../../web/build.txt';
		$build = is_file($file) ? trim((string)file_get_contents($file)) : '';
		if (preg_match('/^build-[0-9a-f]+$/', $build) !== 1) {
			$build = 'missing-build';
		}
		$query = ['host' => 'parent', 'author' => $author];
		return $this->urlGenerator->linkTo(Application::APP_ID, 'web/' . $build . '/frame.html') . '?' . http_build_query($query);
	}

"""

ROUTED_WEB_ROWS = """| `boot.js` | Loaded by the editor's iframe (`templates/frame.php`); imports the files below by content-hashed name |
| `{{ID}}-web-<hash>.js` | wasm-bindgen glue (ES module) |
| `{{ID}}-web-<hash>.wasm` | {{NAME}}, built from storytold/{{ID}} with `patches/{{ID}}-nextcloud.patch` |
"""

ROUTED_LAYOUT_SH = """# Content-hashed names: Nextcloud lets browsers cache app assets for months.
DEST="$OUT"
JS_NAME="{{ID}}-web-$(hash "$STAGE/$OUT_NAME.js").js"
WASM_NAME="{{ID}}-web-$(hash "$STAGE/${OUT_NAME}_bg.wasm").wasm"
rm -f "$OUT"/{{ID}}-web-*.js "$OUT"/{{ID}}-web-*.wasm
"""

STATIC_LAYOUT_SH = """# One folder per build (its name in build.txt): the files keep the names the app's own code uses
# for them, and a new version is a new folder, so browsers never mix cached files of two builds.
BUILD="build-$(cat "$STAGE/$OUT_NAME.js" "$STAGE/${OUT_NAME}_bg.wasm" | sha256sum | cut -c1-12)"
rm -rf "$OUT"/build-*
DEST="$OUT/$BUILD"
mkdir -p "$DEST"
JS_NAME="$OUT_NAME.js"
WASM_NAME="${OUT_NAME}_bg.wasm"
"""

STATIC_FRAME_SH = """# The page in the editor's iframe: static, so relative URLs (workers, worklets) resolve in its
# build folder.
cat > "$DEST/frame.html" <<FRAME
<!DOCTYPE html>
<!-- Generated by scripts/build-{{ID}}-web.sh. SPDX-License-Identifier: AGPL-3.0-or-later -->
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
	<meta name="robots" content="noindex, nofollow">
	<title>{{NAME}}</title>
	<style>
		html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: {{BACKGROUND}}; }
		#{{CANVAS_ID}} { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
		#{{LOADING_ID}} { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; pointer-events: none; }
	</style>
</head>
<body>
	<canvas id="{{CANVAS_ID}}"></canvas>
	<div id="{{LOADING_ID}}"></div>{{FRAME_EXTRA_HTML}}
	<script type="module" src="boot.js"></script>
</body>
</html>
FRAME
echo "$BUILD" > "$OUT/build.txt"

"""


def frame_values(cfg: dict) -> dict:
    if cfg.get("static_frame"):
        return {
            "FRAME_URL_PHP": "$this->staticFrameUrl($user->getDisplayName())",
            "EDITOR_EXTRA_PHP": STATIC_FRAME_PHP,
            "STATIC_FRAME_SH": STATIC_FRAME_SH,
            "LAYOUT_SH": STATIC_LAYOUT_SH,
            "DIST_CHECK_FILE": "web/build.txt",
            "WEB_FILE_ROWS": "",
        }
    return {"FRAME_URL_PHP": ROUTED_FRAME_URL, "EDITOR_EXTRA_PHP": "", "STATIC_FRAME_SH": "", "LAYOUT_SH": ROUTED_LAYOUT_SH, "DIST_CHECK_FILE": "web/boot.js", "WEB_FILE_ROWS": ROUTED_WEB_ROWS}


def fill(text: str, v: dict, where: str) -> str:
    # Values can contain other placeholders (e.g. DESCRIPTION mentions {{NAME}}): two passes.
    for _ in range(2):
        text = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: v[m.group(1)] if m.group(1) in v else m.group(0), text)
    left = set(re.findall(r"\{\{([A-Z_]+)\}\}", text))
    if left:
        sys.exit(f"error: {where}: unknown placeholders {sorted(left)}")
    return text


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    cfg = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    v = values(cfg)
    out.mkdir(parents=True, exist_ok=True)
    for src in sorted(TEMPLATE.rglob("*")):
        if src.is_dir():
            continue
        rel = fill(str(src.relative_to(TEMPLATE)), v, str(src))
        dst = out / rel
        if rel in KEEP_IF_PRESENT and dst.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.name == "LICENSE":
            shutil.copyfile(src, dst)
            continue
        dst.write_text(fill(src.read_text(), v, rel))
        if src.stat().st_mode & 0o111:
            dst.chmod(0o755)
    print(f"generated {v['APP_ID']} in {out}")


if __name__ == "__main__":
    main()
