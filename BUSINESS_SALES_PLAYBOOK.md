# BUSINESS & SALES PLAYBOOK — facade & countertop replacement

Read this with a salesman's head on. The app is not a calculator — it is a **sales manager in your
pocket** that turns an ordinary request into a wow КП, raises the average check, and hands the workshop
a spec so clean they ask zero questions. Every screen should either (a) speed up the замерщик, or
(b) help sell. If it does neither, cut it.

## 1. The business in one picture
You replace kitchen **facades** (doors/fronts) and **countertops**, plus hardware and small extra works.
The client keeps the carcass; gets a "new kitchen" at a fraction of the price in ~10–14 days. Margin
lives in: facade material tier, **countertop upgrade**, hardware (soft-close, brand), LED, edge, and
**extra works** (plinth/cornice/legs/refit). Two very different audiences consume your data:
- **The client** — wants to *feel* it's a modern, high-tech, trustworthy company. Needs value + emotion + a clean price.
- **The workshop (цех/распил/маляр)** — wants *dry facts only*: H, W, axes, offsets, edge, color/decor, notes. No marketing.

## 2. The sales funnel mapped to the app (and the upsell moment at each step)
| Stage | App screen | The sell |
|---|---|---|
| Cold lead | Заявка | Capture want + book the measure. Preliminary КП with a value ladder (база/стандарт/премиум) — sell the dream, not €/m². |
| Preliminary price | Быстрый расчёт → КП | Ranges, not exact. Lead with value. Goal: client says "приезжайте на замер". |
| On-site measure | Замер (the notebook) | The real moment. Area is usually a bit bigger → naturally larger order. **This is where you upsell face-to-face.** |
| On-site upsell | Улучшения / Услуги | Offer the upgrades the client didn't know exist (see §3). Add extra works found on-site. |
| Final КП on phone | КП (final) | Value-first, emotional, stylish PDF. Show preliminary-vs-final honestly. Close. |
| To the workshop | Документы (ТЗ) | Dry, configurable spec. Send even **without color** if undecided; add color later. |

## 3. Revenue levers — the upsell catalog (with value language, not specs)
Each should be a one-tap toggle that the app can *proactively suggest* at the right moment.

- **Countertop upgrade — ЛДСП 38мм → компакт-ламинат (HPL) 12мм.** Grounded value: waterproof
  monolithic core (no chipboard to swell), non-porous & hygienic/antibacterial, heat-resistant (~180°),
  scratch/impact resistant, thin modern look, wide decors. **Unlocks the undermount sink.**
  Copy: *"Тонкая столешница, которая не боится воды и горячего, легко моется и выглядит дорого."*
- **Undermount sink (мойка подстольного монтажа).** Enabled by compact laminate: seamless, modern,
  hygienic (no rim to trap water/mold), easy to wipe crumbs straight in.
  Copy: *"Мойка под столешницей — ни шва, ни бортика: красиво, гигиенично, крошки сметаются одним движением."*
- **Soft-close hinges / drawers (доводчики, Blum/Tandembox).** Copy: *"Кухня больше не хлопает — фасады и ящики закрываются тихо и плавно."*
- **LED lighting.** Copy: *"Тёплый свет вдоль рабочей зоны — удобно готовить, и красиво вечером."*
- **Edge upgrade (лазерная кромка / ABS).** Copy: *"Кромка без видимого шва — не отклеится от пара и влаги, как старая."*
- **Glass / aluminium-frame facades, fresh fronts on open shelves** — small adds that lift the look.
- **Extra works / services (often found on-site):** replace **цоколь/сокаль**, **подцокольный профиль**,
  **карнизы**, **кухонные ножки** (new/adjustable), **подпил/запил/подгонка**, custom nonstandard parts.
  These are easy yeses on-site and pure margin — the app must let you **quick-add** them with a comment.
- **Handles — who buys?** Default: *we install*, but the client often buys them himself (he sees the
  price, picks what he likes, we mount it). Support handle mode: **мы / клиент / уточнить позже**, and a
  "клиент покупает сам" path that can generate a "send client to the shop" note. Already partly modelled
  (`handleMode`, handle-count warning) — keep and surface it.

## 4. The two outputs — design them as opposites
- **Client КП (sell):** stylish, calm, **value on top, price at the bottom**, human/emotional copy,
  no jargon, no cost/margin ever. A **clean PDF** that signals "modern, high-tech company". Bilingual RU/ET.
  (Mechanics in `CLIENT_CONTENT_AND_LANGUAGE.md`.)
- **Workshop ТЗ (build):** **dry facts only** — per facade: H, W, qty, opening, hinge axes top/bottom,
  edge offset & side, hinge type/brand, edge on/off & sides, color/decor/RAL, notes. **Configurable**
  (workshop picks which columns/blocks it needs) and **PDF/print friendly**. Must be sendable **without
  color** (color "уточняется") so the workshop can start cutting; color appended later.

## 5. On-site scenarios the app MUST absorb (so the замерщик never gets stuck)
1. **Color not chosen yet.** Client has catalogs in hand, undecided. → mark facade/order "цвет
   уточняется", send the workshop ТЗ now without color, add color later. The app should not force a color.
2. **Lift-up facades** (фасад над фасадом, в 2–3 уровня): gas-lift / Aventos vs regular hinges — different
   logic; don't show hinge axes where they don't apply.
3. **Handles undecided / client buys them** — handle mode + "купит сам" note.
4. **Nonstandard position** — needs a free **comment** field right on the card ("позиция нестандартная,
   уточнить…"). Comments are cheap and save the workshop a dozen calls.
5. **Extra works discovered on-site** — quick-add plinth/cornice/legs/refit with price + comment.
6. **Area grew vs preliminary** — surface it, and turn it into the honest final-vs-preliminary КП story.

## 6. The app as a proactive sales manager (later phase, list now)
Contextual prompts at the right moment, gentle not pushy:
- Wet zone / sink position → *"Предложить компакт-ламинат + подстольную мойку?"*
- Old kitchen "хлопает" / many doors → *"Доводчики?"*
- Long run under wall units → *"LED-подсветка рабочей зоны?"*
- Before sending КП → a quiet checklist: *"Предложено: столешница ✓ · мойка ✗ · доводчики ✓ · LED ✗"* —
  so you never forget an easy upsell.
- Educate: most clients don't know modern materials exist — the value copy does the teaching.

## 7. Guardrails for the salesman in you
- **The notebook comes first.** The upsell layer must never slow down fast measure entry. Prototype =
  a beautiful, fast notebook you *want* to use; selling rides on top.
- **Honest, not pushy.** Value and emotion, yes; pressure and fake scarcity, no. Trust closes facade jobs
  (the reviews that win are "без спешки, всё объяснили, посоветовали").
- **Not a CRM.** Keep it a focused standalone tool now; it can attach to your CRM later as a data source.
  Don't grow it into a heavy system — that kills the "always want to use it" feeling.

## 8. What this adds to the build (ripples into the phases)
- **Phase 1 (measure):** add a per-position **`comment`** field (additive); make **extra works/services**
  an easy quick-add type; add a **"color pending"** flag so ТЗ can go out without color.
- **Phase 3–4 (КП):** value-first bilingual copy + the upsell value library above + the full-catalog
  selling/technical content model and reference surface (`CLIENT_CONTENT_AND_LANGUAGE.md §6`).
- **Phase 5:** the proactive upsell prompts + "did you offer?" checklist; configurable workshop ТЗ;
  stylish client PDF; preliminary-vs-final comparison.

## 9. The on-site swap loop & two-price model (mostly EXISTS — polish, don't rebuild)
Audited in the current file — these mechanics are already present; the job is to make them fast,
obvious, and well-copied, not to re-engineer them:
- **Two-price model.** Every catalog item already carries `price` (client sell) and `cost` (internal),
  with margin computed and a "Видимость"/tech mode hiding cost from the client. Keep cost/margin strictly
  internal; the client only ever sees the sell price. The mini price-list lives in Settings → Прайс/Справочники.
- **Instant recalc on swap.** `selectMaterial` already re-runs totals + render. The on-site magic is:
  замерщик swaps крашеный MDF → Fenix/премиум, the **client immediately sees the new total** and how each
  option moves the price. Make this the centerpiece of the quote screen: visible total, one-tap material
  swap, instant number. The client "sees what and for how much" in real time.
- **Project resurrection.** A project register + КП version snapshots already exist. The required flow:
  client vanishes for a month → reopen the project → see **what was calculated vs what the client agreed
  to** → on-site, the замерщик (a junior salesman) upsells extras, swaps facades, and the client sees the
  fresh final price. Verify this round-trips cleanly; it's the backbone of the "cold lead → final КП" story.
