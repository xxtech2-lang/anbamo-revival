# CLOSING & HANDOFF LOOP + OPERATIONS

Source: an external solo-owner gap analysis, triaged against the actual code. Its core thesis is correct
and valuable: **the product has screens but not a closed loop "КП → согласие → ТЗ → запуск".** This doc
captures the genuinely-missing pieces that make the tool usable end-to-end for ONE owner — without
turning it into a CRM or requiring a backend.

## Standalone constraints (read first — keeps us honest)
This is a single self-contained HTML app on the phone, data in `localStorage`. Therefore:
- ✅ **Works offline already** — it's a local file; no network needed for core use. (The analysis's
  "no offline mode" is wrong; the real gap is cloud backup/sync, not offline operation.)
- ✅ **Standalone-friendly:** PDF generation in-browser, **Web Share API**, `mailto:`, JSON/CSV export.
  These need no server. `navigator.share` is **already present** in the code — expand it, don't start over.
- ⚠️ **Needs a backend / external account (out of "standalone" scope — owner decides later):** Telegram Bot
  API, webhooks (Zapier/Make), Firebase/Supabase sync, automatic nightly cloud backup. Do NOT build these
  now; they cross the "not a CRM" line the owner drew. Offer the standalone equivalents instead.

## P0 — the closing loop (this is what makes it real)

### 1. PDF export — КП and workshop ТЗ, one button
Audited: **no PDF engine exists** (`jsPDF`/`html2canvas` = 0; only `window.print`). This is the #1 real gap.
- Add a PDF generator (jsPDF + html2canvas, or a clean print-to-PDF stylesheet) producing:
  - **Client КП** — stylish, value-first, price at bottom, no cost/margin, bilingual-ready (Phases later).
  - **Workshop ТЗ** — dry facts only, configurable columns, **sendable without color** (`colorPending`).
- The existing doc renderers (`measureSheet113`, `productionSheet113`, `painterBlank113`, КП/acceptance)
  are the content source — render them to a clean printable layout, then to PDF. Don't rewrite their data.
- Keep client-facing privacy: cost/margin/internal never appear on client PDFs.

### 2. Send via Web Share (expand existing `navigator.share`)
- One "Отправить" button → share the generated PDF (or a link) to WhatsApp/Telegram/email via the native
  share sheet. Pick recipient context (клиент / цех / маляр). Log what was sent + when into the project.
- `mailto:` as a fallback where share isn't available. No bot/server required.

### 3. Readiness checklist (launch gate on the dashboard)
A simple, glanceable gate before a job is "launched":
- КП сформировано/подписано ✓ · Аванс получен ✓ · ТЗ отправлено в цех ✓ · Бланк маляру отправлен ✓
- Green light = ready to launch. Drives off existing `documentLog` / `payments` / deal status — mostly a
  presentation layer over data that already exists. Cheap, high-value (stops "забыл отправить ТЗ").

### 4. Client signature (finger sign on the phone)
Audited: a `signature` field is referenced (×9) but there's **no `<canvas>` capture**. Add it:
- On the КП and the acceptance act: "Принимаю условия" + a canvas to sign with a finger.
- Save the signature image into the project and embed it in the saved/exported PDF.
- Closes the "сказал да устно → передумала" risk; looks professional.

## P1 — operational safety (pragmatic, standalone)

### 5. Backup that a solo owner won't lose
The real risk: localStorage cleared / phone lost. Standalone-safe mitigations (no backend):
- Prominent **one-tap "Бэкап"** → JSON via Web Share / download / `mailto:` to self.
- A gentle **reminder** ("последний бэкап N дней назад").
- (Optional, owner's call later) connect a cloud account for real sync — that's a backend decision, not now.

### 6. Light local calendar (no external calendar integration)
Per project, capture and remind on key dates: замер, КП, аванс, запуск производства, монтаж. Local
reminders only (the CHANGELOG already lists "no Google Calendar integration" as a non-goal — keep it local).

## P2/P3 — later

### 7. Roles (seeded already — `role` ×6)
Forward-looking for when a замерщик is hired: admin sees cost/margin/notes; measurer sees client fields +
ТЗ only. Ties to the existing "Видимость"/tech mode. Solo now → low priority, but don't fight the seed.

### 8. CSV/Excel export for accounting
JSON export already exists (×50). Add a CSV/Excel shape for taxes/materials when needed. A webhook hook
is possible later but is a backend concern.

## Already present — do NOT rebuild (the analysis overstated these)
- Numeric entry: custom `measureKeypad` (×40) + `inputmode` (×32) — built.
- `duplicate` position (×25) — present; just ensure it's reachable from the position list.
- JSON export (×50) — strong.
- Contextual upsell, `colorPending`, per-position `comment` — already specced in our docs (Phases 1/5).

## What to take into the roadmap
Insert a dedicated **Closing & Handoff** phase right after the notebook (Phase 1), ahead of bilingual
copy polish: PDF (КП+ТЗ) → Web Share send → readiness checklist → signature → one-tap backup. This is the
80/20 that turns "a set of screens" into "a tool you can run a one-person business on."
