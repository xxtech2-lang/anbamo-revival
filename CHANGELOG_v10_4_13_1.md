# CHANGELOG v10.4.13.1 — Mobile Hotfix

Baseline: `AN_BAMO_Command_Center_v10_4_13_Field_Measure_Restore.html`
Delivered: `AN_BAMO_Command_Center_v10_4_13_1_Mobile_Hotfix.html`

CSS-only change in a single new `<style>` layer appended at the end of `<body>`. No JS, no layout rewrite, no earlier block edited.

## Added (fixes two Android Chrome bugs found on a real phone)

### BUG 1 — swipe-down reloaded the page (pull-to-refresh)
```css
html, body { overscroll-behavior-y: none; }
```
Disables Chrome's pull-to-refresh and the vertical rubber-band, so a swipe near the top can no longer reload the page and drop local state. (The existing horizontal `overscroll-behavior-x` on chips/settings was left untouched.)

### BUG 2 — bottom navigation occasionally disappeared on long scroll (Step A, kept)
```css
.mobile-nav {
  will-change: transform;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  transform: translateZ(0);
}
```
`translateZ(0)` puts the fixed bottom nav on its own compositor layer so it stops "dropping" when the Android address bar shows/hides and forces a repaint.

### BUG 2 — Step B (move scroll root to `<body>`): evaluated and DROPPED
The brief's Step B (`html{height:100%;overflow:hidden}` + `body{height:100%;overflow-y:auto}`) was tried and rolled back, per the brief's own "if unsure, keep only Step A + BUG 1" fallback:
- It changes the scroll model globally (window → body) on desktop and mobile. On Android the `html{overflow:hidden;height:100%}` interaction with the dynamic browser toolbar can clip content, and that can't be verified in this headless environment.
- It is unnecessary: Step A alone keeps `.mobile-nav` pinned to the viewport bottom through scrolling (verified — `getBoundingClientRect().bottom === innerHeight` after scrolling 650px). Keeping the original window-scroll model also avoids any risk to the existing layout.

Note discovered during verification: the `.topbar` is `position:sticky` but its ancestor `.app` computes to `overflow: hidden auto`, which disables sticky pinning at mobile width. This behavior is **identical in the untouched baseline** (verified) — it is pre-existing and unrelated to this hotfix; not in scope here.

## Not changed
- No JS logic touched.
- Field contract, localStorage key, dashboard, measure, documents, КП — untouched.
- v10.4.12.5 dashboard fix (`window.statusClassV473 = …`) — intact.
- v10.4.13 measure layer — read-only, not edited.
- Desktop layout (`@media (min-width:1024px)`) — verified intact (sidebar present, window-scroll works, no horizontal overflow, mobile-nav stays `display:none`).

## Verification

Gate — `node verify_measure.js AN_BAMO_Command_Center_v10_4_13_1_Mobile_Hotfix.html`:
- `LOAD ERRORS: 0` — PASS
- `TAB SWEEP: 0 errors across 9 tabs` — PASS
- `DASHBOARD RENDERS: len=2427` — PASS
- `MEASURE FIELDS: all 26 fields present (saved=true)` — PASS (preserved from v10.4.13)
- `DOC RENDER` — INCONCLUSIVE under jsdom (renderers in closures), unchanged.

Real browser (Chromium, DevTools mobile emulation):
- Mobile 390px: `overscroll-behavior-y: none` applied; `.mobile-nav` carries `translateZ` + `will-change` and stays pinned to the viewport bottom after scrolling (bottom = innerHeight = 780); window-scroll model preserved; nav tab switch (Замер → Деньги) works; modal covers the full viewport.
- Desktop 1200px: mobile-nav hidden (`display:none`); desktop sidebar present; no horizontal overflow; window-scroll works on a tall pane (settings); `html` overflow stayed at the baseline `hidden auto` (no Step B residue).
- Screenshots: desktop 1200px captured (layout intact). The headless screenshot tool was intermittently unresponsive this session, so the mobile nav-pinned behavior is evidenced by the DOM measurements above (bottom === innerHeight after scroll) rather than a pixel capture.
