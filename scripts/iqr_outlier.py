import pandas as pd
from pathlib import Path

# загрузка данных
BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR / "dataset" / "cardekho_without_skips.csv"
)

# директория для отчётов
REPORTS_DIR = BASE_DIR / "generated_reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = REPORTS_DIR / "outliers_report.md"

# числовые признаки
num_cols = df.select_dtypes(include=["int64", "float64"]).columns

# копия данных
clean_df = df.copy()

outliers_summary = {}

# количество наблюдений
n_observations = len(clean_df)

report_lines = [
    "# Отчёт по выбросам\n"
]

for col in num_cols:
    Q1 = clean_df[col].quantile(0.25)
    Q3 = clean_df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # маска выбросов
    outliers = clean_df[
        (clean_df[col] < lower_bound)
        | (clean_df[col] > upper_bound)
    ]

    outliers_count = len(outliers)

    # доля выбросов
    outliers_ratio = outliers_count / n_observations

    outliers_summary[col] = {
        "count": outliers_count,
        "ratio": outliers_ratio
    }

    report_lines.extend([
        f"## {col}\n",
        f"- Q1: {Q1}",
        f"- Q3: {Q3}",
        f"- IQR: {IQR}",
        f"- Нижняя граница: {lower_bound}",
        f"- Верхняя граница: {upper_bound}",
        f"- Количество выбросов: {outliers_count}",
        f"- Доля выбросов: {outliers_ratio:.4f}\n"
    ])

report_lines.append("## ИТОГО выбросов по признакам\n")

for col, stats in outliers_summary.items():
    report_lines.extend([
        f"### {col}",
        f"- Количество выбросов: {stats['count']}",
        f"- Доля выбросов: {stats['ratio']:.4f}\n"
    ])

# сохранение отчёта
REPORT_PATH.write_text(
    "\n".join(report_lines),
    encoding="utf-8"
)

print(f"Отчёт сохранён: {REPORT_PATH}")