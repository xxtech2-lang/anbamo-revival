# ЗАДАЧА v10.4.14 — Расширенный прайс + Цикл закрытия сделки

Baseline: `AN_BAMO_Command_Center_v10_4_13_1_Mobile_Hotfix.html` (или v10.4.13 если хотфикс ещё в работе).
Выходной файл: `AN_BAMO_Command_Center_v10_4_14_Price_And_Closing.html`

Два независимых, но доставляемых вместе блока. Читай оба до начала.
Архитектура та же: новый `<style>` + `<script>` слой в конец `<body>`, wrap не rewrite, cross-block → window, ensure-chain. Фикс v10.4.12.5 не трогать.

---

## ЧТО УЖЕ ЕСТЬ (не строить заново — только расширять)

Код уже содержит:
- `state.hardwareCatalog` (петли, направляющие, ручки) — есть
- `state.servicesCatalog` (замер, демонтаж, доставка) — есть
- `state.customPriceItems[]` — массив для кастомных позиций — есть
- `priceAddCustom` / `priceDelete` / `priceDuplicate` actions — есть
- `PRICE_CATEGORY_NAMES_V10465` с группами: facade / countertop / hardware / led / work / montage / delivery / measure / tax / other — есть
- `addCustomPriceItemV10465(category)` — функция добавления — есть
- Settings → Прайс с группами по категориям — есть
- `navigator.share` (docShare action) — есть, шарит текст
- `docSaveHtml`, `docCopy`, `docMarkSent` — есть
- `upsertDocLog` — логирует статус документа — есть
- Checklist-стили (`.v473-checklist`, `.v473-check.ok/.warn`) — есть
- JSON-экспорт (`exportJson` action) — есть

---

## БЛОК A — Расширение прайса и быстрый заказ на объекте

### A1. Добавить позиции в существующие каталоги

В `ensureV1414()` добавить через `upsertCatalogItem` (добавляет если нет, не трогает если есть):

**hardwareCatalog** (новые ключи):
- `softClose` — Доводчики петель, unit: hinge, price: 4, cost: 1.8
- `liftGas` — Газлифт (подъёмник), unit: pcs, price: 22, cost: 9
- `aventos` — Aventos (подъёмный механизм), unit: pcs, price: 65, cost: 38
- `handleBar` — Ручка-скоба, unit: pcs, price: 0, cost: 0 (клиент покупает сам — цена 0)
- `handleProfile` — Ручка-профиль, unit: m, price: 0, cost: 0

**Новый каталог `state.ledCatalog`**:
- `ledStrip` — LED-лента, unit: m, price: 8, cost: 3.5
- `ledProfile` — LED-профиль алюминиевый, unit: m, price: 6, cost: 2.8
- `ledPower` — Блок питания, unit: pcs, price: 18, cost: 9
- `ledConnector` — Коннектор/диммер, unit: pcs, price: 12, cost: 5
- `ledInstall` — Монтаж LED, unit: m, price: 5, cost: 0 (labour)

**Новый каталог `state.extraWorksCatalog`**:
- `delivery` — Доставка, unit: project, price: 0, cost: 0
- `carrying` — Занос на этаж, unit: project, price: 0, cost: 0
- `installation` — Монтаж фасадов (работа), unit: project, price: 0, cost: 0
- `dismantleOld` — Демонтаж старых фасадов, unit: project, price: 80, cost: 30
- `plinth` — Цоколь / плинтус, unit: m, price: 0, cost: 0
- `cornice` — Карниз, unit: m, price: 0, cost: 0
- `legs` — Кухонные ножки, unit: pcs, price: 0, cost: 0
- `trimming` — Подпил / подгонка, unit: project, price: 0, cost: 0
- `custom` — Другая работа, unit: project, price: 0, cost: 0 (шаблон для добавления)

Все цены/себестоимость = 0 для позиций которые варьируются — владелец заполнит в Настройках.

### A2. Настройки → Прайс: добавить группы в баяны (accordion)

В секции «Прайс / Справочники» (Settings → Прайс) добавить две новые группы-баяна:
- **LED** — ledCatalog (все 5 позиций)
- **Доп.работы и услуги** — extraWorksCatalog (все позиции)

Каждая группа: заголовок-аккордеон + список строк с полями «Название клиенту», «Цена», «Себестоимость», единица.
Внизу каждой группы кнопка **«＋ Добавить позицию»** → `priceAddCustom` с нужной категорией.
Это уже работает для других каталогов — применить ту же `settingsCatalogListV10464` / `catalogRow` механику.

### A3. Быстрая смета на объекте («Смета» / Quick Order)

**Новая вкладка «Смета»** в разделе «Замер» (рядом с Позиции / Паспорт / Другие работы / Задачи / Сводка).

Сценарий: замерщик на объекте быстро накидывает позиции → видит итог клиенту и внутреннюю стоимость.

Структура экрана:
```
[ Смета ]
Быстрый подбор позиций и услуг для финального расчёта на объекте.

[ Фасады ]  [ Столешница ]  [ Фурнитура ]  [ LED ]  [ Услуги ]  [ Доп.работы ]
                   ← горизонтальный скролл категорий

Список добавленных позиций (qty × цена = сумма):
  Петли мягкие  ×16  = 128 €    [−] [＋] [✕]
  LED-лента  ×3м  = 24 €         [−] [＋] [✕]
  Монтаж фасадов  ×1  = 150 €   [−] [＋] [✕]

─────────────────────────────────
Итого клиенту:  302 €
Себестоимость:  148 €   (видна только в техрежиме)
Маржа:  51%             (видна только в техрежиме)
```

Данные хранятся в `state.quickOrder = []` (массив `{catalogId, source, name, qty, clientPrice, cost}`).
Обновляется `totals()` или добавляется к итогу в отдельной секции — не ломать существующие формулы.

---

## БЛОК B — Цикл закрытия сделки (Phase 2)

### B1. PDF: сохранить документ как файл (без CDN)

Аудит показал: `docSaveHtml` уже сохраняет HTML-файл. Этого **достаточно для MVP**:
- Добавить кнопку **«Скачать PDF»** в панель действий документа.
- Реализовать через `window.print()` с атрибутом `window.onbeforeprint` + `document.title` = имя файла → пользователь нажимает «Сохранить как PDF» в диалоге печати.
- ИЛИ — загрузить jsPDF с CDN: `https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js` (allowlisted). Если CDN доступен — использовать для реального PDF-файла. Если нет — fallback на print.
- Логировать через `upsertDocLog(doc, 'ready', 'pdf')`.

### B2. Отправить документ: расширить docShare

Текущий `docShare` шарит **текст**. Расширить:
1. При нажатии «Отправить» — показать bottom-sheet с выбором:
   - 📤 **Поделиться** (Web Share API — уже есть) 
   - 💾 **Скачать HTML** (уже есть как `docSaveHtml`)
   - 🖨️ **Печать / PDF** (новое — `window.print()`)
   - ✅ **Отметить отправленным вручную** (уже есть `docMarkSent`)
2. Bottom-sheet использует существующий стиль `numeric-sheet` / модалку — не создавать новый компонент с нуля.

### B3. Чек-лист готовности — вынести на видное место

Аудит: стили `.v473-checklist` уже есть. `checklistV473` уже считает пункты. Но он спрятан внутри «Улучшений».

Вынести **блок «Готов к запуску»** на:
- Вкладку **«Заявка»** (в существующую колонку «Проверка проекта» — она уже есть)
- И/или в шапку страницы (рядом с pill-статусом)

Пункты чек-листа (state-driven, не хардкод):
- ✅ / ⚠️ КП сформировано (`documentLog` содержит kp со статусом ready/sent)
- ✅ / ⚠️ КП отправлено клиенту (`documentLog` kp status = sent)
- ✅ / ⚠️ Аванс получен (`state.payments` содержит платёж)
- ✅ / ⚠️ ТЗ цеху отправлено (`documentLog` production/painter status = sent)
- ✅ / ⚠️ Цвет/декор зафиксирован (нет позиций с `colorPending = true`)

Зелёный = все ✅ → можно запускать заказ. Амбер = есть незакрытые пункты.

### B4. Подпись клиента пальцем

В документе **«Акт приёмки»** (тип `acceptance`) добавить canvas-подпись:
- `<canvas id="sigCanvas" width="600" height="180">` с рамкой и label «Подпись клиента»
- Touch/mouse drawing (touchstart/touchmove/mousedown/mousemove)
- Кнопки: «Очистить» и «Сохранить подпись»
- Сохранять как `state.clientSignature = canvas.toDataURL('image/png')`
- Показывать сохранённую подпись в документе при повторном открытии (`<img src="...">`)
- В `ensureV1414()` backfill: `state.clientSignature = state.clientSignature || ''`

### B5. Бэкап в один тап + напоминание

JSON-экспорт уже работает (`exportJson` action). Нужно только:
1. Добавить на экран **«Заявка»** (в существующую карточку «Версии / слепки» или рядом) кнопку **«Бэкап »** → тот же `exportJson`.
2. Показывать под кнопкой: «Последний бэкап: N дней назад» (или «сегодня»).
   - Хранить: `state.lastBackupAt = new Date().toISOString()` при каждом экспорте.
   - Считать разницу с `Date.now()`.
3. Если > 7 дней — кнопка становится amber-цвета + tooltip «Давно не делали бэкап».

---

## НЕЛЬЗЯ ТРОГАТЬ

- Формулы `totals()`, `materialQuote()`, `improvementValue()` — не изменять логику.
- Документные рендереры `measureSheet113`, `productionSheet113`, `painterBlank113` — не изменять.
- Ключ localStorage `anbamo_v10_4_6_mvp_stabilization` — не переименовывать.
- Фикс `window.statusClassV473` (строка ~3388) — не трогать.
- Слой v10.4.13 — только читать.

---

## ПРОВЕРКА

```bash
node verify_measure.js AN_BAMO_Command_Center_v10_4_14_Price_And_Closing.html
```
LOAD ERRORS / TAB SWEEP / DASHBOARD RENDERS / MEASURE FIELDS — все PASS.

Реальный браузер (телефон или DevTools 390px):
- [ ] Настройки → Прайс: видны новые группы LED и Доп.работы, позиции с ценой/себестоимостью.
- [ ] Кнопка «＋ Добавить позицию» в каждой группе работает, позиция появляется.
- [ ] Вкладка «Смета» в Замере: добавил позиции → итог считается.
- [ ] В документе «Кнопка Отправить» → bottom-sheet с вариантами.
- [ ] Чек-лист на «Заявке» показывает статусы.
- [ ] «Акт приёмки» — можно нарисовать подпись, сохранить, при повторном открытии — видна.
- [ ] Кнопка «Бэкап» на Заявке → скачивается JSON, время обновляется.
- [ ] 0 ошибок в консоли. Desktop layout не сломан.

---

## СДАЧА

- `AN_BAMO_Command_Center_v10_4_14_Price_And_Closing.html`
- Вывод `verify_measure.js` (все PASS)
- 3–5 скриншотов: Прайс (LED/Услуги), Смета, Чек-лист, Подпись, bottom-sheet отправки
- `CHANGELOG_v10_4_14.md`
