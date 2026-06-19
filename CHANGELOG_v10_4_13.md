# CHANGELOG v10.4.13 — Field Measure Foundation Restore

Baseline: `AN_BAMO_Command_Center_v10_4_12_5_FIXED.html` (the fixed build with the v10.4.12.5 dashboard ReferenceError fix). Delivered file: `AN_BAMO_Command_Center_v10_4_13_Field_Measure_Restore.html`.

Implemented as a single appended `<style>`+`<script>` v10.4.13 layer at the end of `<body>`. No earlier block was edited. The layer **wraps** `renderMeasure` and injects into the rendered `.m491-entry` DOM (the same pattern v10.4.10.4 and `productionDraft` already use); no measure function was rewritten in place.

## Added (Measure screen only)

- **Inline hinge axes on the first level** of the facade card (bottom / top, mm), shown with an inherited-vs-overridden cue, with an axis-template shortcut (`100/100 · 80/80 · 95/110 · пред. · свои`) and hinge orientation (вертик./гориз.). Axes are pre-filled from the passport and one-tap-overridable per facade — they are not re-typed for every facade.
- **Collapsible «Петли / фурнитура»** (collapsed by default): hinge geometry and hardware brand as two **separate** controls, hinge count, measuring mode (от низа / от верха), hinge edge offset + side.
- **Collapsible «Производство»** (collapsed by default): decor / color / RAL, edge type, edge sides, finish, texture direction.
- **Collapsible «Заметки»** (collapsed by default): painter / production / cutting / risk notes.
- **Type-specific lift-up block**: direction (↑/↓/?) and mechanism (газлифт / Aventos / другой / ?) for `lift` facades.
- **On-site fields**: per-position `comment`, and `colorPending` («цвет уточняется») — when set, the UI states the workshop ТЗ can be sent without color.
- **Editable order passport panel** («Паспорт заказа · наследуется фасадами»): lower/upper height, axis offset (bottom/top), hinge edge offset, measuring mode, lower/upper color. New facades inherit these.
- **Inheritance + per-facade override**: a fresh facade inherits height (by zone), axes, measuring mode and color from the passport; editing one facade's value marks it overridden (local only) and never mutates the passport or sibling facades. Collapsible open/closed state is remembered in `state.measureUi`.

## Field contract

All advanced fields are backfilled onto `state.measureDraft` via `ensureV1413()` and flow into `measureItems` through the existing `normItem` spread. The full `measureItems` field contract is preserved (no field removed or renamed). Hinge / brand / axis values use the app's **canonical vocabulary** (`накл/полу/вклад…`, `стандарт/Blum/Riex/GTV`, `100/100…`) so they survive `normalizeHingeTypeV10443` and render unchanged in the production documents.
New additive fields backfilled via `ensureV1413()`: `hingeOrientation`, `liftDirection`, `comment`, `colorPending`, plus the re-surfaced `hingeAxisTop/Bottom`, `hingeEdgeOffset/Side`, `hardwareBrand`, `axisTemplate`, `axisMode`, `decorName/colorName/ralCode`, `edgeType`, `finishType`, `textureDirection`, `painter/production/cutting/riskNote`.

## Not changed (hard non-goals respected)

- Fast Quote / КП formulas, `totals()`, pricing — untouched.
- Document renderers (`measureSheet113`, `productionSheet113`, `painterBlank113`, …) — untouched; they keep receiving the same field names.
- Money / payments, dashboard, project list, settings logic — untouched.
- localStorage key `anbamo_v10_4_6_mvp_stabilization` — **not renamed**; new fields backfilled at load via `ensureV1413()`.
- The v10.4.12.5 `window.statusClassV473` dashboard fix — kept intact.
- No backend / PWA / APK / cloud / integrations.

## Verification

Automated gate (`node verify_measure.js`):
- `LOAD ERRORS: 0` — PASS
- `TAB SWEEP: 0 errors across 9 tabs` — PASS (dashboard still renders, len=2427)
- `DASHBOARD RENDERS` — PASS
- `MEASURE FIELDS: all 26 fields present (saved=true)` — PASS
- `DOC RENDER` — INCONCLUSIVE under jsdom (renderers are in closures); verified in a real browser instead (production sheet shows `вклад`/`Blum`, painter blank shows `RAL 7016`/note).

Real browser (Chromium, clean localStorage):
- Passport → inherit: a fresh lower facade comes out with H from the passport and axes 100/100 pre-filled; only the width is typed.
- Per-facade override: changing one facade's axis bottom 100 → 70 changes only that facade; the passport stays 100 and a new sibling re-inherits 100.
- hinge geometry and hardware brand are two separate controls; the hinge select holds its value across re-renders.
- save → re-open round-trips all fields; `colorPending` and notes persist.
- collapsibles open/close and remember state; no console errors.
- No horizontal overflow at 390px (collapsed and fully expanded); at 800px the grid uses two columns (foldable-aware).

Note: the headless screenshot tool was wedged for the whole session (the project's known "screenshots blocked" condition) while the page itself stayed healthy; verification above was done via real-browser DOM/state inspection and an accessibility-tree snapshot instead of pixel captures.
