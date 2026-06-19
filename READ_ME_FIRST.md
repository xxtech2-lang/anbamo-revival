# READ ME FIRST — v10.4.13 handoff package

You (Claude Code) are implementing **v10.4.13 Field Measure Foundation Restore**.
Work in this exact order:

1. **Read** `PRODUCT_PHILOSOPHY.md` — the soul of the product. The Measure screen is a phone-first
   "notebook": size + opening + hinge axes recorded as fast as on paper, one-handed, on a Samsung
   Z Fold. Every UI choice is judged against this. Read it before anything else.
2. **Read** `CONTEXT_CODE_MAP_v10_4_12_5.md` — the real map of the file (functions, line numbers) and
   the architecture hazard that caused the last shipped bug. Mandatory; it stops you re-introducing
   the cross-IIFE ReferenceError class.
3. **Read** `TASK_v10_4_13_FIELD_MEASURE_RESTORE.md` — scope, controls to restore, hard non-goals, acceptance.
4. **Edit** `AN_BAMO_Command_Center_v10_4_12_5_FIXED.html` — the FIXED baseline (already contains the
   v10.4.12.5 dashboard fix). Do not start from any `v10_4_12_4` file.
5. **Verify** continuously with the automated gate:
   ```bash
   npm install jsdom        # once
   node verify_measure.js AN_BAMO_Command_Center_v10_4_13_Field_Measure_Restore.html
   ```
   The three hard gates (LOAD ERRORS, TAB SWEEP, DASHBOARD RENDERS) must stay PASS at all times — they are your regression guard. If TAB SWEEP or DASHBOARD breaks, you've re-created the scope-leak bug: a helper used across blocks must be attached to `window`.
5. **Real-browser spot check** (you have static server + Edge): open the Measure screen, confirm compact-by-default + collapsibles + separated hinge/brand controls.

## Golden rules (the short version)
- Add a NEW `<script>`/`<style>` layer at the end; **wrap**, don't rewrite earlier blocks.
- Any function called from another block → `window.fnName = fnName`.
- Keep writing the exact `measureItems` field names listed in the task (documents depend on them).
- Never rename the localStorage `KEY` (data loss). Backfill new fields via `ensureV1413()`.
- Do not touch quote/КП, documents, money, dashboard, settings logic.
- Measure-only scope. If something tempts you outside Measure, stop — it's a separate task.

## Package contents
| File | What it is |
|---|---|
| `READ_ME_FIRST.md` | this file |
| `REVIVAL_ROADMAP.md` | the staged plan for the whole revival (Phases 0–5) |
| `PRODUCT_PHILOSOPHY.md` | the soul of the product — read first |
| `BUSINESS_SALES_PLAYBOOK.md` | the business head: funnel, upsell levers, on-site scenarios, two-audience output |
| `DESIGN_SYSTEM_UX_UI.md` | calm/minimal UX-UI fusion rules (applies to every phase) |
| `CLIENT_CONTENT_AND_LANGUAGE.md` | value-first КП, human copy, RU/ET (Phases 4–5) |
| `CLOSING_HANDOFF_AND_OPERATIONS.md` | PDF/send/sign/checklist/backup — the closing loop (Phase 2) |
| `TASK_v10_4_13_FIELD_MEASURE_RESTORE.md` | the current task (Phase 1) — spec / acceptance |
| `CONTEXT_CODE_MAP_v10_4_12_5.md` | grounded code map + hazards |
| `AN_BAMO_Command_Center_v10_4_12_5_FIXED.html` | baseline to edit |
| `verify_measure.js` | automated headless gate (no Chromium needed) |

The current task is **Phase 1 (v10.4.13 measure restore)**. The roadmap, philosophy, design-system and
content docs are the standing context for the whole revival — read the philosophy + design-system before
touching UI, and the content doc before touching anything the client sees.

The two foundation reports (`FIELD_MEASURE_FOUNDATION_RECOVERY` / `..._MAP_RU`) you produced earlier are the source of truth for *which* controls existed — the TASK file already distills them, but consult them if you need the original rationale.
