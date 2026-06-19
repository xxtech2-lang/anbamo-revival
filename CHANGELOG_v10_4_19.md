# CHANGELOG v10.4.19 — Block 1: Dead Button Fixes

Baseline: `AN_BAMO_Command_Center_v10_4_18_Critical_Fixes.html`
Delivered: `AN_BAMO_Command_Center_v10_4_19_Block1_DeadButtons.html`

Один слой в конце `<body>` (`<style>` + `<script>`), +15 609 символов.
`totals()`, ключ localStorage, `window.statusClassV473` — не тронуты.

---

## Исправление 1 — Под-табы замера (Паспорт / Другие работы / Задачи / Сводка)

### Симптом
Кнопки под-шагов в `m491-shell` (Паспорт, Другие работы, Задачи, Сводка) не реагировали на клики — не было атрибута `data-action`, не было обработчика.

### Точная первопричина
`renderMeasureV10491()` (L4143) — активный финальный рендерер замера — рендерил кнопки `.m491-step` без каких-либо атрибутов `data-action` и `data-step`:
```html
<button class="m491-step active">Позиции</button>
<button class="m491-step">Паспорт</button>   ← нет data-action!
<button class="m491-step">Другие работы</button>
<button class="m491-step">Задачи</button>
<button class="m491-step">Сводка</button>
```
Обработчик из v10.4.10.4 (L4155) перехватывает только `m491*` действия. Обработчик из v10.4.5.1 (L2168) перехватывает только `stepNav`. Без атрибутов — ни один не срабатывает.

### Исправление
**Архитектура**: Post-render декоратор `decorateMeasureV1419()` — запускается после каждого `renderMeasure()` как последний шаг в цепочке обёрток.

1. Находит пять `.m491-step` кнопок в DOM
2. Добавляет `data-action="stepNav"` и `data-step="${id}"` по индексу (порядок DOM: positions/passport/other/tasks/summary)
3. Обновляет класс `active` по `state.measureUi.step`
4. Если `step !== 'positions'` — заменяет `main.m491-col` контентом текущего шага

**Обработка кликов**: использует существующий capture-listener из v10.4.5.1 (L2168), который уже правильно обрабатывает `stepNav` — устанавливает `state.measureUi.step` и вызывает `renderCurrent()`. Декоратор подхватывает обновлённое состояние при следующем рендере.

**Контент шагов** (написан в v10.4.19 IIFE, без зависимостей от недоступных IIFE v10.4.5.1):

| Шаг | Контент |
|-----|---------|
| **Позиции** | Без изменений — оригинальный m491 entry/items view |
| **Паспорт** | Форма с полями `data-v1413-pp` (v10.4.13 обрабатывает change-события) — lowerHeight, upperHeight, tallHeight, axisOffsetBottom, axisOffsetTop, hingeEdgeOffset, axisMode, lowerColor, upperColor |
| **Другие работы** | Список other-type позиций из `state.measureItems` + кнопка `+ Зафиксировать / добавить` |
| **Задачи** | Быстрые чипы + текстовый ввод + кнопки «+ Нам», «+ Клиенту», «+ Риск»; список из `state.measureTasks + state.measureRisks + state.measureNotes` |
| **Сводка** | KPI (фасадов / площадь / задачи / риски) + список позиций + другие работы |

---

## Исправление 2 — Кнопка «+ Зафиксировать» в шапке Замера

### Симптом
Кнопка `data-action="capture"` в `m491-shell` header не открывала sheet.

### Первопричина
`renderMeasureV10491()` рендерит `data-action="capture"`, но ни один из зарегистрированных обработчиков не обрабатывает `a==='capture'`:
- Base (L1105): нет условия для `capture`
- v10.4.3.x (L1134): обрабатывает `openCapture`, не `capture`
- Все capture-phase listeners: не содержат `capture` в списках

### Исправление
В v10.4.19 добавлен capture-phase listener (регистрируется после v10.4.10.4, чтобы перехватить до bubble), который для `a==='capture'` вызывает `openMeasureCaptureSheet()` — глобальная функция, доступная из базового скрипта (L1444).

---

## Проверка — addPayment / addExpense

По итогам аудита v10.4.19: `+ Платёж` и `+ Расход` **уже работали** через v10.4.7.1 (L2994). Этот capture-phase listener с `stopImmediatePropagation()` перехватывает клики до базового stub-обработчика (L1105: `if(a==='addPayment'){return}`). Модальная форма v10.4.7.1 (`v471FinanceModal`) — полная реализация с полями Сумма / Дата / Способ / Назначение / Кто внёс / Заметка. Реализация в v10.4.19 не потребовалась.

---

## Аудит dead elements — итог Block 1

| # | Экран | Элемент | Статус после v10.4.19 |
|---|-------|---------|----------------------|
| 1 | Замер | Паспорт / Другие работы / Задачи / Сводка | ✅ Исправлено |
| 2 | Замер | `+ Зафиксировать` (capture) | ✅ Исправлено |
| 3 | Деньги | `+ Платёж` | ✅ Работало (v10.4.7.1) |
| 4 | Деньги | `+ Расход` | ✅ Работало (v10.4.7.1) |
| 5 | Все | `#modeBtn` / `#themeBtn` в `.toprow` | Скрыты v10.4.17, заменены в ⋯-меню |

---

## Проверка

**Гейт** `node verify_measure.js AN_BAMO_Command_Center_v10_4_19_Block1_DeadButtons.html`:
```
LOAD ERRORS 0 / TAB SWEEP 0/9 / DASHBOARD RENDERS len=2427 / MEASURE FIELDS 26
```
Все жёсткие гейты PASS. DOC RENDER INCONCLUSIVE под jsdom — без изменений.

**Браузер**: ноль предупреждений и ошибок в консоли.
Паспорт, Другие работы, Задачи (quick chips + CRUD), Сводка — все рабочие.
+ Зафиксировать открывает capture sheet. + Платёж и + Расход открывают finance modal.

---

## НЕ ТРОНУТО

`totals()`, `materialQuote()`, ключ localStorage `anbamo_v10_4_6_mvp_stabilization`, `window.statusClassV473`, скидки v10.4.15, импорт v10.4.15, чистая шапка v10.4.17, исправления v10.4.18.
