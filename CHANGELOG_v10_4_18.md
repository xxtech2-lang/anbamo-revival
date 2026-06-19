# CHANGELOG v10.4.18 — Critical Fixes

Baseline: `AN_BAMO_Command_Center_v10_4_17_Clean_Header.html`
Delivered: `AN_BAMO_Command_Center_v10_4_18_Critical_Fixes.html`

Один слой в конце `<body>` (`<style>` + `<script>`). Два хирургических исправления. `totals()`, ключ localStorage, `window.statusClassV473`, скидка/видимость/импорт v10.4.15, чистая шапка v10.4.17 — не тронуты.

---

## BUG 1 — Клик «Замер» в левом навигаторе открывал экран «Проверка»

### Симптом
При нажатии кнопки «Замер» в левом навигаторе (или нижнем таббаре на мобайле) пользователь видел экран с надписью **«Шаг 4 из 6 · Проверка»** вместо ожидаемого экрана замера.

### ТОЧНАЯ ПЕРВОПРИЧИНА

В слое v10.4.7.2 определены обработчики `workflowStep` и `workflowNext` (строки 3204–3205). Когда пользователь нажимал кнопку workflow-шага «check» / «Проверка» или кнопку «Дальше», находясь на шаге «Замер», обработчик выполнял:

```javascript
state.measureStep = 'tasks';
```

Это значение **навсегда оставалось в `state`** — ни один из существующих слоёв его не сбрасывал.

Функция `activeWorkflowIndex()` (строка 3146):
```javascript
if (tab === 'measure' && state.measureStep === 'tasks') idx = 3;
```
— при `state.ui.tab === 'measure'` возвращала **3 (Проверка)** вместо **2 (Замер)**.

После любого последующего перехода на вкладку «Замер» через nav-кнопку функция `injectWorkflow()` (вызываемая из обёртки `setTab` v10.4.7.2) injektировала workflow-bar с mobile-pill:

```
Шаг 4 из 6 · Проверка  [Дальше]
```

Сам контент замера (`m491-shell`) рендерился корректно, но владелец видел крупную надпись **«Проверка»** и считал, что попал не на тот экран.

### Почему обёртка `setTab` безопасна

Обработчики `workflowStep` и `workflowNext` выставляют `state.ui.tab` **напрямую** (не через `setTab`) и затем вызывают `renderCurrent()`. Поэтому новая обёртка срабатывает **только** при кликах на nav-кнопку «Замер», не мешая workflow-переходам.

### Исправление

В v10.4.18 `setTab` обёрнут так:

```javascript
var _stBase18 = typeof setTab === 'function' ? setTab : null;
if (_stBase18) {
  window.setTab = setTab = function(tab) {
    if (tab === 'measure' && typeof state === 'object' && state !== null) {
      state.measureStep = null;  // сброс флага Проверка
    }
    _stBase18.apply(this, arguments);
  };
}
```

После сброса `activeWorkflowIndex()` возвращает 2, workflow-bar показывает **«Шаг 3 из 6 · Замер»**.

---

## BUG 2 — Колесо мыши не прокручивало страницу на десктопе

### Симптом
На десктопе (≥1024px) прокрутка колесом мыши не работала.

### Первопричина
`overflow-x:hidden` на элементах `html,body` (строка 39) преобразует html-элемент в scroll-container: браузер неявно трактует `overflow-y` как `auto`, что делает `<html>` контейнером прокрутки с фиксированным viewport. На десктопе window-scroll перестаёт работать.

### Исправление

Тело-scroll-изоляция вынесена в медиазапрос mobile-only:

```css
@media (max-width:1023px) {
  html { height: 100%; overflow: hidden; }
  body { height: 100%; overflow-y: auto; -webkit-overflow-scrolling: touch; }
}
```

На десктопе `html`/`body` не получают `height:100%` и `overflow:hidden` из этого правила → нормальная window-scroll, колесо работает.
На мобайле (≤1023px) тело-scroll-изоляция активна → pull-to-refresh заблокирован, нижний навбар не исчезает.

`overscroll-behavior-y:none` на `html,body` остаётся **глобальным** (установлен в v10.4.13.1, не изменяется).

`.topbar { position: sticky }` продолжает работать на десктопе, так как новый scroll container не создаётся.

---

## НЕ ТРОНУТО

`totals()`, `materialQuote()`, `improvementValue()`, ключ localStorage `anbamo_v10_4_6_mvp_stabilization`, `window.statusClassV473`, `state.quote.discount` (v10.4.15), импорт 106 позиций владельца (v10.4.15), экраны видимости (v10.4.15), чистая шапка v10.4.17.

---

## ПРОВЕРКА

Гейт `node verify_measure.js AN_BAMO_Command_Center_v10_4_18_Critical_Fixes.html`:
```
LOAD ERRORS 0 / TAB SWEEP 0/9 / DASHBOARD RENDERS len=2427 / MEASURE FIELDS 26
```
Все жёсткие гейты PASS. `DOC RENDER` INCONCLUSIVE под jsdom (без изменений).
