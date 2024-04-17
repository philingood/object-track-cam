# Проект по цифровой кафедре

## Описание

Это проект на Python, использующий техники компьютерного зрения для отслеживания объектов в реальном времени, снимаемых камерой. Система определяет и следит за объектами в поле зрения камеры, а также управляет движением камеры с помощью мотора, подключенного к Arduino. Для обработки изображений используется OpenCV, предоставляющий функциональность по обнаружению и отслеживанию объектов.

### Запуск программы

Запустить программу можно командой

```bash
make run
```

### Управление

- Трекер лица - запуск клавишей `f`, отсанов - `F`
- Центрирование объекта - `c`, останов - `C`
- Трекер выделенной области - запуск клавишей `s`, останов - `S`
- Останов всех трекеров по клавише `Q`
- Завершение программы - `ESC`

> NOTE: Нажатие может не срабатывать, лучше зажимать клавишу.

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

Активация окружения:

```bash
conda activate highflyer
```

## Проблемы

- После ухода обьекта из кадра, `CSRT` (когда объект выбирается вручную) трекер ложно продолжает распознавать объект в кадре, из-за чего объект полностью теряется.
