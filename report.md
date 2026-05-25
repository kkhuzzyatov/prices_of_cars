# Отчёт по проекту математической статистики

## 1. Описание данных

Для выполнения проекта по математической статистике использовался набор данных, содержащий характеристики автомобилей, проданных на вторичном рынке, и цены, по которым они были реализованы.

Набор данных был скачан с Kaggle:  
https://www.kaggle.com/datasets/sukhmandeepsinghbrar/car-price-prediction-dataset/data

Датасет содержит 12 признаков. Описание каждого признака можно найти в файле:  
[variable_description.md](./variable_description.md)

---

## 2. Первичный анализ данных

Работа с данными была начата с получения общей информации о датасете. Отчёт доступен по ссылке:  
[main_report.md](./generated_reports/main_report.md)

Код для генерации отчёта:  
[main_report_creator.py](./scripts/main_report_creator.py)

---

## 3. Обработка пропусков

Все пропуски были заменены медианными значениями.

Данные без пропусков сохранены в файл:  
`cardekho_without_skips.csv`

Логика обработки пропусков реализована в:  
[dataset_skips_replacer.py](./scripts/dataset_skips_replacer.py)

Отчёт по замене пропусков:  
[replacing_skips_report.md](./generated_reports/replacing_skips_report.md)

---

## 4. Визуализация данных

Для каждого числового параметра были построены диаграммы плотности и распределения:

Плотности:
[density](./plots/density)

Распределения:
[distribution](./plots/distribution)

Cdfs:
[cdfs](./plots/cdfs)

Также были построены диаграммы рассеяния:

- `./plots/scatter`

Логика генерации графиков:  
[graphs_generator.py](./scripts/graphs_generator.py)

---

## 5. Основные наблюдения

- Около 75% автомобилей выпущены в период с 1994 по 2020 год.
- Цены большинства автомобилей варьируются в диапазоне от 270_000 до 690_000. При этом присутствуют значительные выбросы как в меньшую, так и в большую сторону.
- Большинство автомобилей имеют относительно высокий пробег: 35_000 – 95_750 км.
- Почти все автомобили рассчитаны на 5 пассажиров, что подтверждается графиками плотности и распределения:  
    - [density_seats.png](./plots/density)
    - [distribution_seats.png](./plots/distribution)
  
    Однако присутствует заметная доля автомобилей с 7 местами.

---

## 6. Выбросы

Выбросы определялись по правилу IQR:

\[
[Q1 - 1.5 * (Q3 - Q1), Q3 + 1.5 * (Q3 - Q1)]
\]

Полный отчёт по выбросам:  
[outliers_report.md](./generated_reports/outliers_report.md)

Особенность переменной `seats`:  
при Q3 − Q1 = 0 стандартное правило IQR некорректно интерпретируется, однако по min/max видно, что распределение логически согласованное.

Реализация поиска выбросов:  
[iqr_outlier.py](./scripts/iqr_outlier.py)

---

## 7. Проверка нормальности распределений

Были проверены гипотезы о нормальном распределении следующих признаков:

- year  
- selling_price  
- km_driven  
- engine  
- max_power  
- seats  

Все гипотезы были отвергнуты: ни для одной переменной p-value не оказался близким к уровню значимости.

Отчёты:  
[normal_distribution_reports](./generated_reports/normal_distribution_reports)

Скрипт проверки:  
[normal_distribution_checker.py](./scripts/normal_distribution_checker.py)

---

## 8. Модель линейной регрессии

На очищенных данных была обучена модель линейной регрессии (`LinearRegression` из sklearn) для предсказания цены автомобиля на основе:

- года выпуска  
- объёма двигателя (engine)

Качество модели:

- Доля объяснённой дисперсии (R²): **37%**

Логика обучения модели:  
[train_with_2_parameters.py](./scripts/train_with_2_parameters.py)

Отчёт по модели:  
[linear_regression_report_with_2_parameters.md](./generated_reports/linear_regression_report_with_2_parameters.md)

---

## 9. Итоговая модель

Математическая форма модели:

\[
selling\_price = 83451.7465 * year + 713.0193 * engine - 168464187.6098
\]