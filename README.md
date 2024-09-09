# Автотесты API & UI

Это проект, написанный на Python (PageObject) с помощью фреймворка Playwright.
Больше о Playwright — https://playwright.dev/.

Для API тестов использовался пакет httpx.

Основные пакеты:

- pytest
- playwright
- httpx
- allure
- pydantic

Статьи на habr:

- [Пишем АПИ автотесты на Python по шагам](https://habr.com/en/articles/765512/)
- [Как правильно писать UI авто тесты на Python](https://habr.com/en/articles/708932/)

## Требования

- Python 3.12+
- Java 8+

## Установка

1. Установить `pip install virtualenv`
2. Установить Playwright: `pip install playwright && playwright install --with-deps chromium`
3. Создать виртуально окружение `virtualenv venv --python=python3.12`
4. Активировать:
    - Windows `.\venv\Scripts\activate`
    - Linux `chmod +x venv/bin/activate && . venv/bin/activate`
5. Установить зависимости `pip install -r requirements.txt`
6. Установка Allure — [https://docs.qameta.io/allure/#_get_started](https://docs.qameta.io/allure/#_get_started)
7. В файле `.env` переключить параметр `HEADLESS_ENABLED=False`. **Перед пушем в GitLab переключить в `True`**

## Браузеры

Чтобы добавить больше браузеров, посетите – https://playwright.dev/docs/browsers

## Эмуляция мобильных устройств

Использование: добавьте декоратор `@pytest.mark.mobile` в тесте для метода или класса.

Чтобы добавить больше мобильных устройств:

1. Добавьте марку в `pytest.ini`;
2. Добавьте новое устройство в `core/driver.py`;
3. Измените функцию `is_mobile` в `conftest.py` — потребуется новая логика;

### Еще о маркерах

Запуск только API тестов `pytest -m 'api'`. Аналогично UI тесты - `pytest -m 'ui'`.

## Запуск

Многопоточность:

- Single-thread — исполните команду `pytest` для запуска всех (ui + api) тестов в одном потоке;
- Multi-thread — исполните команду `pytest -n 5` для запуска всех тестов в 5 потоках.

Генерация отчёта `Allure`:

- Исполните команду `pytest --alluredir=./allure-results` для запуска всех тестов и генерации отчета в директории
  `./allure-reports`. Чтобы открыть удобочитаемый отчёт, исполните команду `allure serve ./allure-results`.