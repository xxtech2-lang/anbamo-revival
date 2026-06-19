# DESIGN SYSTEM — UX/UI fusion (calm, minimal, state-honest)

This is the visual+interaction contract for the whole revival. UX and UI are one thing here:
**a control's appearance must tell the truth about its state.** If it's tappable, it looks tappable;
if it's active/selected, it carries a distinct, meaningful color; if a value is inherited vs overridden,
you can see which at a glance. Color is meaning, not decoration.

## 0. Don't rebuild — consolidate
The file already has a real token system in `:root` (color, space, radius, shadow, `--tap`, plus
`data-theme=dark`, `data-contrast=high`, `data-density=compact`, glass). **Reuse and extend these
tokens.** Never hardcode a hex or a one-off color in a new block — add/extend a token. New CSS goes in
the v10.4.13+ `<style>` layer and must reference `var(--…)`.

## 1. Calm by default — kill visual noise
The #1 complaint to design against: walls of bold text and too many accent colors.
- **One primary action per region.** Everything else is secondary/quiet (`.btn` default, not `.btn.primary`).
- **Bold is for true emphasis only.** Numbers that matter (price, size) can be heavy; labels and helper
  text are normal weight, muted color (`--muted`). Audit: if a card has >2 bold elements, reduce.
- **Accent colors are signals, not styling.** Blue = primary/interactive, green = confirmed/ok,
  amber = needs attention, red = problem. A card should not light up in 4 colors at once.
- **Whitespace over borders.** Prefer spacing and subtle `--surface-2` grouping to heavy lines.

## 2. State color semantics (use consistently everywhere)
| State | Token | Where |
|---|---|---|
| Interactive / primary action | `--blue` | the one main button |
| Selected / active chip or tab | `--blue` tint bg + blue text/border | chips, tabs, variant cards |
| Confirmed / done / inherited-ok | `--green` / `--ok-bg` | saved, paid, included |
| Needs attention / soft warning | `--amber` / `--warn-bg` | validations, unfilled |
| Problem / blocking | `--red` / `--bad-bg` | errors, missing required |
| Inherited (from passport) | muted/ghost style | measure card values |
| **Overridden** (deviates from passport) | distinct accent + small "изменено" tag | measure card |
A замерщик must see at a glance: what's inherited, what he changed, what still needs attention.

## 3. Collapsible accordions ("баяны") — progressive disclosure
- Screen opens **calm**: only the essentials visible; heavy/secondary blocks are collapsed.
- Use native-feel collapsibles (the app already uses `details`-style sections in Settings — reuse the pattern).
- **Remember open/closed state** per section (in `state.ui`, persisted) so it doesn't reset on re-render.
- Measure: «Петли/фурнитура», «Производство», «Заметки» collapsed by default; the fast card is open.
- Settings already group into sections — keep one open at a time (accordion), not all expanded.

## 4. Transitions — subtle, fast, purposeful
- 120–180ms ease for open/close, tab change, selection. Never slow, never bouncy-decorative.
- Respect `prefers-reduced-motion` — disable non-essential motion.
- A tap must give immediate feedback (the app already has `.btn:active{transform:translateY(1px)}` — keep that language).

## 5. Touch & foldable
- Keep `--tap` ≥ 44px; primary actions thumb-reachable (bottom area on phone).
- Works one-handed at ~360–420px (Z Fold outer); uses the width sensibly at ~768–900px (unfolded) —
  the existing `matchMedia('(max-width:1023px)')` split is the hook. Two-column only when there's room.

## 6. Typography & hierarchy
- One type scale (already in tokens). Title → subtitle(muted) → body. Don't introduce new sizes ad hoc.
- Money and key sizes are the visual anchors; let them be big and let everything else recede.

## 7. The test for any screen
> Open it cold. Is your eye pulled to **one** clear next action, with everything else quiet and
> grouped? Can you tell each control's state by its color alone? If the screen feels busy or shouty,
> it's not done.

## 8. Client-facing surfaces (КП, documents) get extra restraint
- Clean, document-like, emotionally warm but uncluttered. Value on top, price at the bottom (see
  `CLIENT_CONTENT_AND_LANGUAGE.md`). No internal colors/jargon/margins ever leak to the client view.
