# CONTEXT — Code Map & Hazards (baseline: v10.4.12.5 FIXED)

This file makes you "in the know" about the actual file so you don't rediscover it the hard way.
All line numbers refer to `AN_BAMO_Command_Center_v10_4_12_5_FIXED.html`.

## 0. The one bug that already bit this project (DO NOT repeat)

In v10.4.12.4, three helpers (`statusClassV473`, `checklistV473`, `realWarningsV473`) were declared **inside the v10.4.7.3 IIFE** (lines ~3302–3391) but called from **later IIFE blocks** (`renderImprovementsV4731` ~3529, `renderImprovementsV4732` ~3723). Result: `ReferenceError: statusClassV473 is not defined` on every render → improvements pane broke AND the render chain aborted before the dashboard, so the **dashboard rendered empty**, and the version stamp froze early.

**Fix already applied** at line ~3388:
```js
window.statusClassV473=statusClassV473;window.statusRuV473=statusRuV473;window.checklistV473=checklistV473;window.realWarningsV473=realWarningsV473;
```
Keep this. The lesson generalizes: **cross-block helper → attach to `window`.**

## 1. File shape
- Single self-contained HTML, ~5916 lines. ~24 `<script>` blocks + matching `<style>` blocks.
- Architecture: layered. Each version = `(function(){ const VERSION=...; ...; })()`. Later layers **override** earlier functions by capturing a `base` reference and re-assigning the global.
- Core globals live in the FIRST block (~1033+): `state` (declared `const` — NOT on window), and bare-assigned globals like `render`, `renderCurrent`, `ensureV1044State`, `totals`, helpers. Bare assignment = global property, which is why later blocks can see them.
- Append your new layer at the very end of `<body>`, after the last existing `<script>`.

## 2. Measure render surface (functions you will wrap/extend)
| Function | Line | Role |
|---|---|---|
| `renderMeasure` | 1126 (base), re-wrapped ~2158 (`renderMeasure=function(){…}`) | Top-level Measure pane renderer. Mobile vs desktop split via `matchMedia('(max-width:1023px)')`. Writes into `#pane-measure`. |
| `renderMeasureDraft` | 1351 | The entry form (the draft being edited/added). Type tabs: swing/drawer/panel/corner/led/custom. |
| `renderMeasureTypeBlock` | ~1360 | Per-type field block (this is where type-specific controls render). |
| `productionDraft` | 2869 | Production fields block, currently **prepended** into the draft toolbar via a wrap of `renderMeasureDraft` (see line ~2870). Good example of the wrap pattern to copy. |
| `renderMeasureStepContentV10451` | 2156 | Step content (positions / other steps). |
| `renderMeasureStepsV10451` | 2149 | Step rail/chips. |
| `renderMeasureHeadV10451` | 2157 | Measure header. |
| `renderMeasurePassport` | 1552 | Passport summary (material, RAL, heights, axis template, edge offset). |
| `renderMeasureGroupSelector` | 1331 | Group/zone selector. |
| `renderMeasureSummaryPanel` | 1369 | Right-side summary (desktop). |
| `inheritedMeasureDraft` | 1302 | Builds a new draft inheriting group/passport defaults — REUSE for "+ next/same". |
| `getEffectiveMeasureItem` | 3872 | Resolves inherited fields for an item — REUSE for rendering/documents. |
| `measureGroup` | 1249 | Returns the active group object. |

### Draft model
- `state.measureDraft` holds the in-progress entry. Numeric keys are whitelisted:
  `MEASURE_NUMERIC_KEYS=['height','width','qty','customHingeCount','hingeTop','hingeBottom','handleCount','drawerCount','cornerA','cornerB','ledLen']` (line 1292).
  **If you add new numeric inputs (e.g. `hingeAxisTop`), add their keys here** or numeric coercion won't apply.
- Draft input wiring: there is a delegated `input` listener that reads `x.dataset.measureDraft` and writes `state.measureDraft[key]` (around line 1502). Reuse this dataset convention (`data-measure-draft="hingeType"`) so you don't need new listeners for simple fields.

## 3. Documents that READ measure fields (do NOT break — keep field names)
| Function | Line | Reads |
|---|---|---|
| `measureSheet113` | 5247 | opening, handle, hinge, axes, hinge edge offset |
| `painterBlank113` | 5254 | color/decor, RAL, finish, hinge, hardware, axis top/bottom, edge offset, notes |
| `productionSheet113` | 5258 | material, decor/color, edge, hinge/brand, handle |
| `measureAxes` | 1252 | axis fallback for rendering |

## 4. Proof the fields already exist (this is a re-surfacing task)
Reference counts in current source: `hardwareBrand`×19, `axisMode`×23, `hingeEdgeOffset`×16, `hingeAxisTop`×8, `hingeAxisBottom`×7, `liftMechanism`×7, `handleMode`×57, `hingeEdgeSide`×3, `riskNote`×6. The model and documents already know these; the **UI just stopped showing them** after the v10.4.9.1 mobile simplification.

## 5. Storage (do not change)
- Main key: `const KEY='anbamo_v10_4_6_mvp_stabilization';` (line 1034).
- There is a `LEGACY_KEYS=[...]` array (line 1035) — migration from old keys already exists.
- Project register/current-project use separate keys (`anbamo_project_register_v10_4_7_2`, `anbamo_current_project_id_v10_4_7_2`, lines ~3106–3107).
- Migration mechanism = the `ensure*` chain backfilling defaults at load. Add `ensureV1413()` the same way; never rename `KEY`.

## 6. Browser-API notes
- The app uses `matchMedia`, `CSS.escape`, clipboard, print — all real in browsers. (They are absent in jsdom; `verify_measure.js` polyfills them so the automated gate matches real-browser behavior.)
- Default active tab on load does NOT touch the broken path, which is why a naive "does it load" check looked green in the original QA. **Always sweep all tabs.**
