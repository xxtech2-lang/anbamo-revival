# CHANGELOG v10.4.15 — Гибкость, Скидка, Импорт прайса, Уборка

Baseline: `AN_BAMO_Command_Center_v10_4_14_Price_And_Closing.html`
Delivered: `AN_BAMO_Command_Center_v10_4_15_Flex_And_Discount.html`

One appended layer at the end of `<body>`: a `<script type="application/json">` with the owner's 106-item catalog + one `<script>` with all logic (Blocks A–C). Wrap, not rewrite; cross-block via `window`; `totals()` / localStorage key / `window.statusClassV473` untouched.

## БЛОК A — Скидка клиенту
- `ensureV1415` backfills `state.quote.discount = {type:'none'|'percent'|'amount', value, reason}`.
- Discount panel injected into **Деньги** and **Смета**: переключатель Нет / Процент % / Сумма €, поле значения, поле «Причина», live-пересчёт (Цена до скидки → Скидка −X → К оплате).
- `applyDiscount(total)` / `discountInfo(total)` (on `window`): percent → `total*(1−v/100)`, amount → `max(0,total−v)`, none → `total`. Применяется к итогу клиенту; себестоимость не трогается.
- **КП**: при активной скидке в `docHtml('kp')` после блока итога добавляются строки «Стоимость по предложению / Скидка (причина) / К оплате». Без скидки строки не выводятся. Анкер устойчив к layout kp112 (`<article>`), `doc-total` и обычному.

## БЛОК B — Гибкость каталога
- Настройки → **«Видимость позиций — что показывать клиенту»**: все каталоги (Фасады / Столешницы / Кромка / Фурнитура / LED / Доп.работы / Услуги) свёрнутыми группами; у каждой позиции тумблер **ON/OFF** (флаг `active`). OFF скрывает позицию из Сметы (данные целы), ON возвращает.
- В каждой категории — **«＋ Своя позиция»** (создаёт позицию в нужном каталоге, сразу доступна в Смете).

## БЛОК C — Импорт реального прайса владельца (106 позиций)
- Каталог встроен как `<script type="application/json" id="ownerCatalogV1415">` и распределён по `cat`:
  facade(7)→`materials`, countertop(4)→`topMaterials`, edge(5)→`edgeCatalog` (создан), hardware(41)→`hardwareCatalog`, led(13)→`ledCatalog`, extra(18)→`extraWorksCatalog`, service(7)→`servicesCatalog`, corpus(11)→`extraWorksCatalog`. Всего 106.
- Видимость по умолчанию: фасады/столешницы/кромка/услуги/доп.работы — `active+show:true`; LED — true только лента/профиль/драйвер; фурнитура — true только петли/доводчики/газлифт/Aventos/ручки; corpus и длинный хвост — `active:false` (в каталоге есть, владелец включит).
- Поля `supplier` и `art` сохранены на позициях (для ТЗ снабженцу/цеху).
- Импорт идемпотентный, **по имени** (`upsert`): отсутствующие добавляются, цены владельца не перетираются. Флаг `state.__catImportV1415` — один прогон на проект.

## БЛОК D — Уборка (отдельный коммит)
- Удалены старые сборки (есть в git history): v10.4.12.5_FIXED, v10.4.13, v10.4.13.1; старые `GATE_OUTPUT_*` (кроме v15). Оставлены v10.4.14 (откат) и v10.4.15.
- `vercel.json` → rewrite на `/AN_BAMO_Command_Center_v10_4_15_Flex_And_Discount.html`.
- `node_modules` остаётся в `.gitignore`. Уборка — отдельный коммит `chore: cleanup old build artifacts`.

## НЕ ТРОНУТО
- `totals()`, `materialQuote()`, `improvementValue()` — без изменений (скидка считается отдельно поверх итога).
- Ключ localStorage `anbamo_v10_4_6_mvp_stabilization`, фикс `window.statusClassV473`, слои v10.4.13/14 — не тронуты.
- Цены владельца импортом не перетираются.

## ПРОВЕРКА
Гейт `node verify_measure.js AN_BAMO_Command_Center_v10_4_15_Flex_And_Discount.html`:
`LOAD ERRORS 0` / `TAB SWEEP 0/9` / `DASHBOARD RENDERS` / `MEASURE FIELDS 26` — все PASS; `DOC RENDER` INCONCLUSIVE под jsdom (без изменений).

Реальный браузер (Chromium, чистый localStorage) — подтверждено через DOM/state:
- Импорт: materials 7, topMaterials 4, edge 5, hardware 41, led 13, extra 29 (18+11 corpus), service 7 = 106; supplier сохранён.
- Скидка: 10% от 1888 → 1699.2; €188 → 1700. Панель в Деньгах и Смете; в КП строки «Стоимость 1 657 € · Скидка −166 € · К оплате 1 491 €», без скидки — нет строк.
- Видимость: OFF на «Петли» убрал позицию из Сметы (picker 21→20); ON возвращает.
- Смета показывает импортированные позиции: фасады 10, услуги 10, столешницы 7.
- 0 ошибок в консоли.

Примечание: headless-скриншоты в этой среде нестабильны (известная «screenshots blocked» ситуация), доказательства приведены через DOM/state-инспекцию; на обычном Edge/Chrome скрин снимается мгновенно.
