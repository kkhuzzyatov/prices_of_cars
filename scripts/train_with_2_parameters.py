import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Загрузка данных
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "cardekho_without_skips.csv"

df = pd.read_csv(DATA_PATH)

# Признаки
X = df[["year", "engine"]]

# Target
y = df["selling_price"]

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Создание модели
model = LinearRegression()

# Обучение модели
model.fit(X_train, y_train)

# Предсказания
predictions = model.predict(X_test)

# Коэффициент детерминации R²
r2 = r2_score(y_test, predictions)

# Формирование отчёта
report = f"""# Отчёт по линейной регрессии (2 признака)

## Используемая модель
Linear Regression

## Целевая переменная
selling_price

## Используемые признаки
- engine
- year

## Метрика качества модели
- R²: {r2:.4f}

## Интерпретация метрики

### R²
Доля дисперсии target, объясняемая моделью.

## Коэффициенты модели

### Коэффициенты признаков
- year: {model.coef_[0]:.4f}
- engine: {model.coef_[1]:.4f}

### Свободный член
{model.intercept_:.4f}
"""

# Путь для сохранения отчёта
REPORT_PATH = (
    BASE_DIR
    / "generated_reports"
    / "linear_regression_report_with_2_parameters.md"
)

# Создание директории, если её нет
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

# Сохранение отчёта
REPORT_PATH.write_text(report, encoding="utf-8")

print(f"Отчёт сохранён: {REPORT_PATH}")