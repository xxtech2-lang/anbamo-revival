# TASK — v10.4.13 Field Measure Foundation Restore

**Role:** You (Claude Code) implement. The plan, scope and acceptance below are fixed — follow them literally. Do not expand scope.

**Baseline file to edit:** `AN_BAMO_Command_Center_v10_4_12_5_FIXED.html` (included in this package).
This is the **fixed** build — it already contains the v10.4.12.5 ReferenceError fix. Build on THIS file, not on any older `v10_4_12_4` file.

---

## 1. Goal (one sentence)

Make the professional measure (замер) controls **visible and usable again** on the Measure screen, in a **compact, collapsible** layout — without bloating the first mobile screen and without touching anything outside Measure.

This is a **UX surfacing task**, not a data-model task. The fields already exist in `state` and in the document renderers (verified). You are re-exposing them in the UI, not inventing them.

---

## 2. Scope — what you MAY touch

- The Measure tab render path only: the measure entry form, the measure draft, the collapsible sections, and the measure-specific CSS.
- You add functionality by appending a **new `<script>` + `<style>` layer at the end of `<body>`** (a `v10.4.13` layer) that **wraps** existing measure render functions. See `CONTEXT_CODE_MAP_v10_4_12_5.md` for the exact functions and how the layering works.

## 3. Scope — what you MUST NOT touch (hard non-goals)

- ❌ Fast Quote / КП formulas, totals(), pricing.
- ❌ Documents output (`measureSheet113`, `productionSheet113`, `painterBlank113`) — they already consume these fields; do **not** change them. Your job is to keep feeding them the same field names.
- ❌ Money / payments, dashboard, project list, settings logic.
- ❌ Backend / PWA / APK / cloud / integrations — none of that exists and none is in scope.
- ❌ The localStorage key `anbamo_v10_4_6_mvp_stabilization` — **do not rename it**. Renaming orphans the user's saved projects (data loss). New fields are backfilled at runtime via the `ensure*` pattern (see code map).
- ❌ Do **not** remove or weaken the `v10.4.12.5` fix at line ~3388 (`window.statusClassV473 = ...`). Removing it re-breaks the dashboard.

---

## 4. Hard architectural guardrails (READ — this is where the last bug came from)

1. **Layered IIFE model.** Every feature version is its own `(function(){ ... })()` block. Variables/functions declared inside a block are **private to that block** unless attached to `window`. The last shipped bug (v10.4.12.4) was exactly this: helper functions declared inside one IIFE were called from a later IIFE → `ReferenceError`.
   - **Rule:** any function your v10.4.13 layer defines that is referenced from anywhere else MUST be attached to `window` (e.g. `window.renderMeasureV1413 = renderMeasureV1413`). If it's only used inside your own block, keep it local.
2. **Wrap, don't rewrite.** To change a render function, capture the previous one and call it, e.g.
   ```js
   const baseRenderMeasure = renderMeasure;
   renderMeasure = function(){ ensureV1413(); baseRenderMeasure(); decorateMeasureV1413(); };
   ```
   Do not edit the earlier measure blocks in place.
3. **State migration via ensure, not key bump.** Add an `ensureV1413()` that backfills any new draft defaults onto existing state:
   `state.measureDraft = { ...newDefaults, ...(state.measureDraft||{}) }`. Chain it into the `ensureV1044State`/`renderCurrent` wrappers like every other layer does.
4. **Field names are a contract.** The documents read specific keys (see §6). Write the **exact** same keys back to `state.measureDraft` and `measureItems`.

---

## 5. What to build

> **Design north star:** read `PRODUCT_PHILOSOPHY.md` first. The Measure entry is a **notebook**:
> a замерщик must record size + opening + hinge axes as fast as jotting on paper, one-handed, on a
> phone (incl. Samsung Z Fold 7/6). The first-level controls below ARE the notebook — keep them
> instant. Everything heavier collapses.

### 5.1 First level — the notebook (always visible, fast, no collapsing)
For a swing facade this is the core "sketch" and must be enterable in seconds:
- Position: module, position no., **H / W / Qty**, status.
### 5.0 The passport is the engine (build/confirm this FIRST)
The whole point of fast entry is that a **project passport (паспорт заказа)** pre-fills the per-facade
defaults. `renderMeasurePassport` (line 1552) already exists — make sure the passport captures and
feeds these defaults into new facade cards via `inheritedMeasureDraft`:
- **Lower height / upper height** per group (uppers may be multi-tier 2–3 levels; glass is a type).
- **Lower color / upper color**.
- **Axis offset base** (e.g. `100 / 100`) inherited by every facade.
- **Measuring base** `от низа / от верха` (`axisMode`) — a passport default that floats per site.
A new facade must come out of the passport with height, color, axes and measuring base already set.

### 5.1 First level — the fast card (always visible; width + L/R + handle)
Because the passport pre-fills the rest, the per-facade fast path is tiny and must stay tiny:
- **Height** — auto-filled from passport by group; editable but rarely touched.
- **Width** — the one number the замерщик almost always types. **Qty**, status.
- **Opening** chips: `L / R / P / ?` → `opening`.
- **Hinge axes — bottom / top**, shown inline on the card, **pre-filled from the passport offset** and
  **one-tap-overridable per facade** (`hingeAxisBottom` / `hingeAxisTop`). The замерщик does NOT retype
  them every time — they inherit; he only changes the value when THIS facade deviates (e.g. 100 → 90).
  Keep an **axis template** shortcut (`100/100 · 80/80 · 95/110 · пред. · свои` → `axisTemplate`).
  Indicate hinge **orientation** (vertical / horizontal) — additive field (e.g. `hingeOrientation`) is
  fine; do not remove any existing field.
- Handle quick chips: `нет / W / H / ?` → `handleMode`, + where the handle is.
- Live **preview** line (group · size · opening · axes · handle).
- Add actions: **Add**, **+ same module**, **+ next module** (reuse `inheritedMeasureDraft`).

> Note: v10.4.9.1 hid the axes; the owner's philosophy keeps them on the card — but as **inherited,
> overridable** values, not as fields to fill from scratch. Prominent + compact (steppers/short numeric).

### 5.2 Collapsible section «Петли / фурнитура» (collapsed by default)
The heavier hinge/hardware detail that is NOT needed for every facade:
- **Hinge geometry** (GEOMETRY, not brand): `накл / полу / вклад / 155° / 45° / другая` → `hingeType`.
- **Hardware brand** (separate control): `стандарт / Blum / Riex-GTV / ?` → `hardwareBrand`.
- **Hinge count:** `auto / 2 / 3 / 4 / свои` → `customHingeCount` (auto logic already exists).
- **Measuring mode:** `от верха / от низа` → `axisMode`.
- **Hinge edge offset:** `21 / 22 / свои` mm → `hingeEdgeOffset`, **side** → `hingeEdgeSide`.

### 5.3 Type-specific (show only for the relevant type)
- **Lift-up facade:** direction `↑ / ↓ / ?`, mechanism `газлифт / Aventos / другой / ?` → `liftMechanism`. Do NOT show regular hinge axes for lift-up unless expanded.
- **Drawer:** guide type + handle fields.

### 5.4 Collapsible section «Производство» (collapsed by default)
- Color/decor/RAL override (`decorName` / `colorName` / `ralCode`).
- Edge on/off (`edgeEnabled`), edge sides (`edgeSides`), edge type (`edgeType`), finish (`finishType`), texture direction (`textureDirection`).

### 5.5 Collapsible section «Заметки» (collapsed by default)
- Painter note (`painterNote`), production note (`productionNote`), cutting note (`cuttingNote`), risk note (`riskNote`).

### 5.6 Inheritance & per-facade override (the heart of the speed)
- A new facade inherits from the **passport / group**: height, color/RAL, axis offset, measuring base,
  hinge type, brand, edge, handle, production settings. Helpers exist — `inheritedMeasureDraft`
  (line 1302) and `getEffectiveMeasureItem` (line 3872). Reuse them; do not reinvent.
- **Override must be local and obvious.** When a facade deviates from the inherited value (e.g. axis
  offset 100 → 90, or a different color), the change applies to **that facade only** and never mutates
  the passport or sibling facades. Record overrides via the existing `overrides` field. Show a small
  "изменено" / inherited-vs-overridden cue so the замерщик can see at a glance what is custom.
- Changing a value **in the passport** re-flows to all facades that still inherit it (not to ones already
  overridden).

### 5.7 On-site reality fields (from BUSINESS_SALES_PLAYBOOK §5 — additive, cheap, high-value)
The замерщик must never get stuck on site. Add these (additive fields, backfilled via `ensure`):
- **Per-position `comment`** — a free-text note right on the card ("позиция нестандартная…"). Saves the
  workshop a dozen calls. Show it compactly (one tap to expand), not as a always-open textarea.
- **`colorPending`** (order- and/or position-level) — "цвет уточняется". When set, the **workshop ТЗ can
  be sent without color** (color appended later); the client КП and ТЗ both show "цвет уточняется", and
  a soft reminder appears until resolved. Do NOT force a color to proceed.
- **Extra works / services quick-add** — reuse the existing `custom`/`other` measure type so the замерщик
  can add плинтус/цоколь, подцокольный профиль, карниз, ножки, подпил/подгонка with a price + comment in
  two taps. These are easy on-site upsells and pure margin.

---

Do not drop any of these from the draft → item flow (documents depend on them):

```
type, groupId/zoneId, module, position, height, width, qty, status,
opening, handleMode, handleLength, handleCount,
hingeType, hardwareBrand, axisTemplate, axisMode,
hingeAxisTop, hingeAxisBottom, hingeTop, hingeBottom,
hingeEdgeOffset, hingeEdgeSide,
material, materialType, decorName, colorName, ralCode,
edgeEnabled, edgeSides, edgeType, edgeLengthAuto, edgeLengthManual,
finishType, extraLacquer, textureDirection,
painterNote, productionNote, cuttingNote, riskNote,
includeInQuote, sendToProduction, showInstaller, overrides
```

You MAY add new fields (additive only) if a control needs one — e.g. `hingeOrientation`
(vertical/horizontal), `comment` (per-position note), `colorPending` (color undecided). Adding fields is
fine; **removing or renaming** any field above is not, and new fields must be backfilled via
`ensureV1413()` so old saved data still loads.

---

## 7. Acceptance criteria (all must pass before you call it done)

Run the automated gate first (no browser/Chromium needed — works in this environment):

```bash
node verify_measure.js AN_BAMO_Command_Center_v10_4_13_*.html
```

It must report:
- **`LOAD ERRORS: 0`** — no console/runtime errors on load.
- **`TAB SWEEP: 0 errors`** — every tab switches cleanly (regression guard for the v10.4.12.5 fix; dashboard must still render non-empty).
- **`MEASURE FIELDS: PASS`** — after programmatically filling a swing item with all advanced fields and saving, every field in §6 is present on the saved `measureItems[0]` and survives an export round-trip.
- **`DOC RENDER: PASS`** — `measureSheet113` / `productionSheet113` / `painterBlank113` render the new fields without throwing.

Then a **real-browser spot check** (you have a static server + Edge in your env):
- Measure screen first view is compact (advanced sections collapsed).
- Each collapsible («Петли/фурнитура», «Производство», «Заметки») opens/closes.
- Hinge geometry and hardware brand are two **separate** controls.
- Hinge axes (bottom/top) are visible on the **first level** (not collapsed) for a swing facade.
- **Passport → inherit:** set lower-facade height + axis offset in the passport, add a new lower
  facade → height and axes come pre-filled; the замерщик only typed the width.
- **Per-facade override:** change one facade's axis 100 → 90 → only that facade changes; passport and
  siblings stay 100; the facade shows an "изменено"/override cue.
- Entering values and re-opening the item shows them persisted.
- **Phone / foldable check:** at a narrow viewport (~360–420px, Z Fold outer screen) the notebook
  core (H/W + L/R/P + axes) is reachable one-handed without horizontal scroll; at a wide viewport
  (~768–900px, Z Fold unfolded) the layout uses the width sensibly. Test both widths.

## 8. Versioning / housekeeping
- New filename: `AN_BAMO_Command_Center_v10_4_13_Field_Measure_Restore.html`.
- Stamp `DEFAULT.version` and your `ensureV1413()` to `v10.4.13 Field Measure Restore`; update `document.title` and the visible version pill.
- Add a `CHANGELOG_v10_4_13.md` describing only what changed (Measure UI restore) and an explicit "Not changed" list (quote/docs/money/dashboard/storage key).

## 9. Deliverables back
- The new HTML.
- `verify_measure.js` output (paste the PASS lines).
- 2-3 real-browser screenshots of the Measure screen (collapsed + one section expanded).
- `CHANGELOG_v10_4_13.md`.
