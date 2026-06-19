# CLIENT CONTENT & LANGUAGE — value-first КП, human copy, RU/ET

Covers everything the **client** sees: the КП (commercial proposal), material/improvement/service
copy, and the language it's written in. This is a dedicated phase — do NOT entangle it with the
measure work. But design measure data so this layer can consume it cleanly.

## 0. Current state (audited — know before you build)
- **No i18n exists.** No language toggle, no string dictionary, no Estonian. All client text is
  **hardcoded inline** in render functions, in Russian. The only `ru-RU` in the code is `Intl.NumberFormat`
  (money/number formatting), not language.
- The value-first intent is **already stated** in code (fast quote: "Не продаём €/м². Показываем понятные
  варианты и итог за кухню"). Materials already have a client name + description + badge, and cost/margin
  hide behind a tech mode. So the spirit exists — it needs to be made systematic, richer, and bilingual.

## 1. Content layer architecture (build this)
1. **Central dictionary**, not inline strings:
   ```js
   const CONTENT = {
     ru: { kp_intro: '...', mat_painted_value: 'Окрашенный фасад — оптимум цены и качества…', ... },
     et: { kp_intro: '...', mat_painted_value: '…', ... }
   };
   ```
2. **Global `t()` helper** (cross-block → attach to window!):
   ```js
   window.t = (key) => (CONTENT[clientLang()] && CONTENT[clientLang()][key]) || CONTENT.ru[key] || key;
   ```
   RU is the fallback so a missing ET string never breaks output.
3. **Language in state:** `state.settings.clientLang` ∈ {'ru','et'}, default 'ru'. Backfill via `ensure`.
4. **Editable in Settings → Контент** (this section already exists): the manager can edit the client
   texts per language. Keep internal/technical text separate from client text.
5. **Per-document language choice:** the КП should be sendable in the client's language — a toggle on
   the КП/Documents surface (RU/ET) that flips `clientLang` for the rendered client output.

> Migration: extract strings gradually, key by key, RU first (fallback guarantees nothing breaks),
> then fill ET. Do not big-bang rip every string at once.

## 2. Estonian
- The owner is in Estonia; some clients are Estonian-speaking. ET is a real requirement, not cosmetic.
- **Do not ship machine-translated ET to clients as final.** Provide ET slots with RU fallback now;
  mark ET strings for **native review** before they're presented as polished. Flag clearly in Settings
  which ET strings are still unreviewed.

## 3. Value-first КП — the structure (every client output)
Order is non-negotiable: **value first, price last.**
1. **Warm opening** — a human line addressed to the client (configurable, per language).
2. **What they get** — the facades/options described as *benefits and feel*, not specs. Emotional but honest.
3. **Comparison ladder** (when relevant) — база / стандарт / премиум, framed as choices of value, not a price grid.
4. **Final-vs-preliminary** (final КП on-site) — "предварительно было X, по факту Y, потому что …" — honest,
   reassuring, explains the change.
5. **Price** — at the **bottom**, clean, total-for-the-kitchen (not €/m²).
6. **Never**: internal cost, margin, supplier names, technical jargon, or app-internal accent colors.

## 4. Copy rules (human, warm, a touch of emotion)
- Lead with the benefit and the feeling, then the fact.
- Concrete, sensory, honest. No hype that can't be defended.
- Examples (RU) — transform spec → value:
  - "крашеный фасад" → **"Окрашенный фасад — оптимальное соотношение цены и качества: ровная гладкая
    поверхность, мягкий бархатистый тон, благородный матовый вид."**
  - "доводчики" → **"Тихое мягкое закрывание — кухня больше не хлопает, фасады закрываются плавно."**
  - "LED-подсветка" → **"Тёплый свет вдоль рабочей зоны — удобно готовить и красиво вечером."**
- Keep a short, editable phrase library per material/improvement/service, per language, in Settings → Контент.

## 6. Catalog content model — the WHOLE facade catalog, not one item
Today each catalog item has only `client` (name) + one `desc` + a short `tech` label + `price`/`cost`.
The selling layer needs **two distinct texts per item**, for every **facade** material/product (cheap
commodity items like a plastic leg don't need rich copy — "надёжная пластиковая ножка" is enough):
- **`sellingText`** — value/emotional, human, what the client *feels and gains* (per language RU/ET).
- **`techText`** — dry facts that build trust ("компакт-ламинат: монолит без ДСП, до 180 °C, без шва под
  мойку, не боится влаги и царапин").
- **`photos[]`** — 1+ images per facade type, **zoomable** in-app. The замерщик carries physical
  samples, but a quick tap-to-enlarge photo helps show options and upsell on the spot.
All additive fields, editable in Settings → Контент, RU/ET with RU fallback.

### Reference surface («Справочник»)
A place the замерщик/монтажник opens instantly to *read selling + technical text and show the client*
(name, photo, sellingText, techText) for any facade — so he never fumbles or "тупит" on site. It can be
the expanded state of a material card ("почему этот материал") and/or a dedicated reference tab. It must
be one tap away from the measure/quote flow.

## 5. Guardrails
- `t()` and the dictionary are **global** (cross-block usage → `window`). This is the same scope rule
  that, when ignored, broke the dashboard. Don't repeat it.
- Client privacy regression must hold: cost/margin/internal fields never reach client output. There is
  already a privacy check in QA — keep it green.
- This phase touches many render blocks (strings are everywhere). Move in small, verifiable steps and
  run `verify_measure.js` after each (the hard gates catch regressions). RU output must stay identical
  until a key is intentionally rewritten.
