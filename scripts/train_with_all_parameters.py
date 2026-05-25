import re
from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "dataset"
    / "cardekho_without_skips.csv"
)

REPORT_PATH = (
    BASE_DIR
    / "generated_reports"
    / "linear_regression_report_with_all_parameters.md"
)


def extract_numeric(series: pd.Series) -> pd.Series:
    """
    Извлекает числовые значения из строк.
    Пример:
    '1248 CC' -> 1248
    '81.86 bhp' -> 81.86
    """

    extracted = (
        series.astype(str)
        .str.extract(r"(\d+\.?\d*)")[0]
    )

    return pd.to_numeric(
        extracted,
        errors="coerce"
    )


# Загрузка данных
df = pd.read_csv(DATA_PATH)

# Очистка числовых колонок
df["engine"] = extract_numeric(df["engine"])
df["max_power"] = extract_numeric(df["max_power"])

# Удаление строк без target
df = df.dropna(subset=["selling_price"])

# Числовые признаки
numeric_features = [
    "year",
    "engine",
    "km_driven",
    "max_power",
]

# Категориальные признаки
categorical_features = [
    "fuel",
    "seller_type",
    "transmission",
    "owner",
]

# Признаки
X = df[
    numeric_features
    + categorical_features
]

# Целевая переменная
y = df["selling_price"]

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Pipeline для числовых признаков
numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ]
)

# Pipeline для категориальных признаков
categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)

# Общий препроцессор
preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        ),
    ]
)

# Полный pipeline модели
model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "regressor",
            LinearRegression()
        )
    ]
)

# Обучение модели
model.fit(X_train, y_train)

# Предсказания
predictions = model.predict(X_test)

# R²
r2 = r2_score(
    y_test,
    predictions
)

# Получение обученной регрессии
regressor = model.named_steps["regressor"]

# Получение имён признаков
feature_names = (
    model.named_steps["preprocessor"]
    .get_feature_names_out()
)

# Формирование списка коэффициентов
coefficients = zip(
    feature_names,
    regressor.coef_
)

coefficients_text = "\n".join(
    [
        f"- {name}: {coef:.4f}"
        for name, coef in coefficients
    ]
)

# Формирование отчёта
report = f"""# Отчёт по линейной регрессии

## Используемая модель
Linear Regression

## Целевая переменная
selling_price

## Используемые числовые признаки
- year
- engine
- km_driven
- max_power

## Используемые категориальные признаки
- fuel
- seller_type
- transmission
- owner

## Кодирование категориальных признаков
OneHotEncoder

## Метрика качества модели

### R²
{r2:.4f}

## Интерпретация R²

Доля дисперсии target, объясняемая моделью.

## Коэффициенты модели

{coefficients_text}

## Свободный член

{regressor.intercept_:.4f}
"""

# Создание директории
REPORT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Сохранение отчёта
REPORT_PATH.write_text(
    report,
    encoding="utf-8"
)

print(f"R²: {r2:.4f}")
print(f"Отчёт сохранён: {REPORT_PATH}")