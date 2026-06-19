# REVIVAL ROADMAP — AN BAMO Command Center

Goal: revive the project and bring it to an ideal — a calm, minimal, phone-first tool whose core is a
fast measurer's notebook (passport + inheritance), layered with fast quote, value-first bilingual КП,
and clean money/docs. **Staged, gated, no big-bang.** The project nearly died from undisciplined
layering; the cure is discipline, not more speed.

## Operating rules for every phase
- **One phase at a time.** Don't bleed scope between phases.
- **Wrap, don't rewrite.** New `<script>`/`<style>` layer at the end; capture+call the previous fn.
- **Cross-block helper → `window`.** (The exact mistake that broke the dashboard.)
- **Gate after every step:** `node verify_measure.js <file>` — LOAD ERRORS / TAB SWEEP / DASHBOARD must
  stay PASS — then a real-browser spot check.
- **Contracts hold:** never remove/rename existing state fields or client privacy guards; backfill new
  fields via `ensure`; never rename the localStorage `KEY`.
- **Design + content principles apply continuously** (see `DESIGN_SYSTEM_UX_UI.md`,
  `CLIENT_CONTENT_AND_LANGUAGE.md`), not as a separate "polish later" step.

## Phases

### ✅ Phase 0 — Stabilize (v10.4.12.5) — DONE
Fixed the cross-IIFE `ReferenceError` that left the dashboard empty and froze the version stamp.
Baseline for everything else: `AN_BAMO_Command_Center_v10_4_12_5_FIXED.html`.

### ▶ Phase 1 — Measure foundation restore (v10.4.13) — NEXT
Passport as the engine; fast card = width + L/R + handle (height/axes/color inherited); axes first-level,
inherited + per-facade overridable; collapsibles for hinge detail / production / notes; lift-up & drawer
types; phone/Z-Fold compact. Spec: `TASK_v10_4_13_FIELD_MEASURE_RESTORE.md`. **Measure only.**

### Phase 2 — Closing & Handoff loop (ELEVATED — makes it usable end-to-end)
Source: a solo-owner gap analysis whose core point is right — there are screens but no closed loop
"КП → согласие → ТЗ → запуск". Spec: `CLOSING_HANDOFF_AND_OPERATIONS.md`. Standalone, no backend:
- **PDF export** of client КП and workshop ТЗ, one button (real gap — no PDF engine today).
- **Send via Web Share** (expand the existing `navigator.share`) to client/цех/маляр; log what was sent.
- **Readiness checklist** on the dashboard (КП подписан · аванс · ТЗ отправлено → green light).
- **Client finger-signature** on КП/acceptance (no canvas capture today); embed in the PDF.
- **One-tap backup** + reminder (cloud sync is a later, backend decision — not now).
This is the 80/20 that turns the screens into an operable one-person workflow. Comes BEFORE copy/language
polish because without send+sign you can't actually run a job.

### Phase 3 — Design-system pass (rolling)
Apply `DESIGN_SYSTEM_UX_UI.md` — noise reduction, state-color semantics, accordions with remembered
state, subtle transitions — starting on Measure (Phase 1) and rippling outward screen by screen.
Not a separate redesign; it rides along each phase and gets a dedicated cleanup sweep at the end.

### Phase 4 — Client content + value-first КП (RU)
Extract hardcoded client strings into a central dictionary with a global `t()`; restructure every client
output as value→price; richer human/emotional copy; full-catalog selling+technical text + photos +
reference («Справочник»); editable in Settings → Контент. RU first.
Specs: `CLIENT_CONTENT_AND_LANGUAGE.md`, `BUSINESS_SALES_PLAYBOOK.md`.

### Phase 5 — Language RU/ET
Add `clientLang` + per-document language toggle; fill ET strings with RU fallback; mark ET for native
review before client-facing use.

### Phase 6 — Sales engine, workshop spec & polish
The app becomes a proactive **sales manager** (`BUSINESS_SALES_PLAYBOOK.md`):
- Preliminary КП with tiers (база/стандарт/премиум); on-site **final КП** with honest preliminary-vs-final
  comparison and add-on upsell.
- **Contextual upsell prompts** (wet zone → compact laminate + undermount sink; "хлопает" → soft-close;
  long run → LED) and a "did you offer?" checklist before sending.
- **Configurable workshop ТЗ**; **stylish client PDF**; light local **calendar** (замер/монтаж reminders);
  **roles** (admin/measurer) for when a замерщик is hired.

## Strategic fork (owner decision — raise before Phase 2 grows)
Two ways to reach "ideal" on a 24-layer file:
- **(A) Keep layering** — fastest per step, lowest immediate risk, but technical debt keeps accruing and
  the file gets harder to reason about. Fine for Phases 1, 3, 4 if disciplined.
- **(B) Consolidate first** — a one-time refactor that flattens the measure (and later content/design)
  logic into clean modules before piling more on. Slower up front, but the only honest path to a truly
  "ideal", maintainable product. Higher risk; must be done with the gate + real-browser checks as a net.
Recommendation: do Phase 1 as (A) to deliver value fast, then decide (B) for the foundation before
Phases 3–5, when the content/language work would otherwise smear strings across all 24 layers.
