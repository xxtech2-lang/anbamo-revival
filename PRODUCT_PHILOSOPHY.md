# PRODUCT PHILOSOPHY — AN BAMO Command Center (read before designing UI)

This is the soul of the product. Every UI decision in Measure (and beyond) is judged against it.
If a change makes the core slower or more cluttered, it is wrong — even if it adds a "feature".

## 1. The core is a measurer's notebook — powered by a project passport + inheritance

The primary job: on-site, the замерщик records every facade **in as few taps as possible**. The speed
does NOT come from drawing — it comes from a **project passport (паспорт заказа)** that pre-fills the
defaults, so each facade card only needs the 1–2 things that actually differ.

### 1a. Step one — fill the passport (once, on arrival)
The passport holds the base values shared by most facades:
- **Lower facades height** (e.g. 800) and **upper facades height** (e.g. 920). Uppers can be **multi-tier
  (2–3 levels)** depending on the kitchen; glass facades are also a type.
- **Lower color / upper color**.
- **Hinge axis offset base** (e.g. `100 / 100`) inherited by all facades.
- **Measuring base for axes:** measured **from the bottom** or **from the top** of the facade
  (`от низа / от верха`). This genuinely **floats** with on-site conditions — it's a passport setting, not a constant.

### 1b. Step two — add facades fast (each card inherits the passport)
Tap **"new facade"**:
- **Height auto-fills** from the passport (by group: lower / upper / tall / panel).
- The замерщик types only the **width**.
- Taps **L / R** (left/right facade; P = pair, ? = clarify).
- Taps **where the handle is**.
- The card is complete — color, axis offset, measuring base all **inherited**. Two or three taps + one number.

### 1c. The hinge-axis tool (the nuance that must be handled, not hidden)
Hinge mounting axes (монтажные оси) are the drilling spec the workshop bores to. They are inherited
from the passport, shown on the facade, and **overridable per facade**:
- Hinges can sit **vertically or horizontally** — the tool must let the замерщик indicate orientation.
- The measuring base (from bottom / from top) comes from the passport but can be adjusted.
- The passport offset (e.g. `100/100`) flows to every facade automatically.
- **Per-facade override:** if one facade deviates (manufacturer drilled 90, not 100), the замерщик
  changes that facade's value `100 → 90` in place, without touching the passport or the other facades.

**Implication for v10.4.13:** the *first-level* fast path is **width + L/R + handle** (height & axes
inherited and shown). Axes are **visible and one-tap-overridable**, not re-typed each time and not buried.
The passport is the engine that makes the notebook fast — treat it as a first-class surface, not a setting.

### 1d. What the data feeds
- **Client report:** a clean facade list (height × width per facade) the client can read.
- **Painter / manufacturer ТЗ:** the full spec — axes, offsets, orientation, color, edge, notes — so the
  workshop sees everything it needs with no guessing.

## 2. Everything else is a layer ON TOP of the notebook, never in front of it

Built up over versions, in priority order of how much they may intrude on the core (least → most allowed to be tucked away):
1. **Fast quote** — digitize the measure and instantly tell the client a price.
2. **Client КП (commercial proposal)** — present a price ladder: **база / стандарт / премиум**.
3. **Upsell** — sell additional options/services to raise the average check. This is a primary business goal.
4. **Money**, **Projects**, **Documents**, **Improvements** — supporting layers.

The rule: a new layer may add a tab, a section, a button — but it may **never slow down or crowd
the notebook entry**. When in doubt, the notebook wins.

## 3. The sales journey the product serves

```
Cold lead
  → Preliminary КП  (price range: база / стандарт / премиум)        ← sells the dream, books the measure
  → Client agrees, books a measure
  → On-site measure (the notebook)                                  ← real area often a bit larger
  → Upsell options/services on the spot
  → Final КП delivered on the phone, on-site
        • shows the price
        • COMPARES to the preliminary КП: "was X, now Y, here's why it changed"
        • lists add-on services typical for this business
```

Two business priorities to keep front of mind:
- **Sell high / sell add-ons** → raise the average order value.
- **Always give the client a КП** → a clear, comparable price they can say yes to.

(КП and final-vs-preliminary comparison are **out of scope for v10.4.13** — Measure only — but this
explains *why* the measure must capture clean, complete data: the КП and the comparison are built from it.)

## 4. Form factor: phone-first, foldable-aware

- Primary device is a **phone**, used one-handed on a job site.
- Explicitly target foldables: **Samsung Galaxy Z Fold 7 / 6** — a narrow outer screen and a wide
  inner screen. Layout must stay usable at a narrow width and make sensible use of the wide width
  (the existing desktop/mobile split via `matchMedia('(max-width:1023px)')` is the hook for this).
- Compact, thumb-reachable, minimal typing. Chips/steppers over free-text where possible.

## 5. The one-line test for any Measure change

> "Could the замерщик record a facade — size, opening, hinge axes — in the same number of taps as
> jotting it in a paper notebook, standing up, on a phone, with one hand?"

If yes, it fits the philosophy. If a change adds taps to that core path, move it into a collapsible.
