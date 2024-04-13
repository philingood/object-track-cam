# Проект по цифровой кафедре

## Установка зависимостей

Для работы необходим `python` версии 3.11.

Для установки модулей с помощью `pip` выполните команду

```bash
pip install -r requirements.txt
```

или для создания окружения `conda`:

```bash
conda env create -f environment.yml
```

## Проблемы

- После ухода обьекта из кадра, трекер ложно продолжает распознавать объект в кадре, из-за чего объект полностью теряется.
