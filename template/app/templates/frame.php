<?php
/**
 * SPDX-FileCopyrightText: 2026 Britton Couchman <brittondcouchman@gmail.com>
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */
/** @var array $_ */
?>
<!DOCTYPE html>
<html lang="<?php p($_['language']); ?>">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
	<meta name="robots" content="noindex, nofollow">
	<title>{{NAME}}</title>
	<style>
		html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: {{BACKGROUND}}; }
		#{{CANVAS_ID}} { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
		#{{LOADING_ID}} { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; pointer-events: none; }
		@media (prefers-color-scheme: dark) { html, body { background: {{BACKGROUND_DARK}}; } }
	</style>
</head>
<body>
	<canvas id="{{CANVAS_ID}}"></canvas>
	<div id="{{LOADING_ID}}"></div>{{FRAME_EXTRA_HTML}}
	<?php emit_script_tag($_['bootUrl'], '', 'module'); ?>
</body>
</html>
