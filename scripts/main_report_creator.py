import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "cardekho_clean.csv"
REPORT_PATH = BASE_DIR / "generated_reports" / "main_report.md"

df = pd.read_csv(DATA_PATH)

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(REPORT_PATH, "w", encoding="utf-8") as report:

    report.write("# Анализ данных\n\n")

    # Базовая информация
    report.write("## Основная информация\n\n")
    report.write(f"- Количество строк: {len(df)}\n")
    report.write(f"- Количество колонок: {len(df.columns)}\n\n")

    # Типы данных
    report.write("## Типы данных\n\n")
    report.write("```text\n")
    report.write(str(df.dtypes))
    report.write("\n```\n\n")

    # Числовая статистика
    num_df = df.select_dtypes(include=["int64", "float64"])

    stats = pd.DataFrame({
        "min": num_df.min(),
        "max": num_df.max(),
        "mean": num_df.mean(),
        "var": num_df.var(),
        "std": num_df.std(),
        "Q1": num_df.quantile(0.25),
        "median": num_df.quantile(0.5),
        "Q3": num_df.quantile(0.75),
    }).round(3)

    report.write("## Основные статистики\n\n")

    for col in stats.index:
        report.write(f"### {col}\n")
        for k, v in stats.loc[col].items():
            report.write(f"- {k}: {v}\n")
        report.write("\n")

print(f"Отчёт сохранён: {REPORT_PATH}")