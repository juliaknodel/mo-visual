# Визуализация методов оптимизации. Метод золотого сечения

## Задание
Нужно реализовать GUI приложение для визуализации работы/результатов методов оптимизации.

## Реализация
Реализована визуализация метода золотого сечения (одномерная минимизация)

## Инструкция по запуску

1. Клонируйте этот репозиторий
> git clone https://github.com/juliaknodel/mo-visual.git
2. Установите всё упомянутое в requirements.txt
> pip install -r requirements.txt
3. Перейдите в корень проекта и запустите source/visual.py
> python source/visual.py


## Пример использования

1. В появившемся окне введите:
    + Function - функция, минимум которой ищем на промежутке
        > x**2
    + Left border - левая граница исходного промежутка неопределенности
        > -1
    + Right border - правая граница промежутка неопределенности
        > 1
    + Accuracy - точность, с которой будет получено решение
        > 0.01

2. Нажмите на кнопку "Показать", в окне появится график, визуализирующий 0 итерацию
3. С помощью кнопок "<-" и "->" меняйте номер визуализируемой итерации





