import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from scipy.stats import shapiro
from scipy.stats import probplot

import os

def safe_filename(name: str) -> str:
    import re
    return re.sub(r'[^\w\-_.]', '_', name)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "cardekho_without_skips.csv"
df = pd.read_csv(DATA_PATH)

def check_distribution(column_name: str):
    data = pd.to_numeric(df[column_name], errors="coerce").dropna()

    safe_name = safe_filename(column_name)
    PLOTS_BASE = BASE_DIR / "plots" / "normal_distribution_reports"
    base_dir = PLOTS_BASE / safe_name
    base_dir.mkdir(parents=True, exist_ok=True)

    # Гистограмма
    plt.figure(figsize=(8, 5))
    plt.hist(data, bins=30)
    plt.title(f"Histogram of {column_name}")
    plt.xlabel(column_name)
    plt.ylabel("Frequency")

    hist_path = base_dir / f"{safe_name}_histogram.png"
    plt.savefig(hist_path, dpi=300, bbox_inches="tight")
    plt.close()

    # Q-Q график
    plt.figure(figsize=(6, 6))
    probplot(data, dist="norm", plot=plt)

    plt.title(f"Q-Q Plot of {column_name}")

    qq_path = base_dir / f"{safe_name}_qqplot.png"
    plt.savefig(qq_path, dpi=300, bbox_inches="tight")
    plt.close()

    # Тест Шапиро-Уилка
    stat, p = shapiro(data)

    alpha = 0.05

    if p < alpha:
        conclusion = "H0 отвергается: распределение не является нормальным"
    else:
        conclusion = "Нет оснований отвергать H0"

    # Markdown-отчёт
    report_path = BASE_DIR / "generated_reports" / "normal_distribution_reports" / f"{safe_name}_normal_distribution_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report = f"""# Отчёт по распределению: {column_name}

## Тест Шапиро-Уилка
- статистика: {stat}
- p-value: {p}
- уровень значимости alpha: {alpha}

## Вывод
{conclusion}
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    columns_to_check = [
        "year",
        "selling_price",
        "km_driven",
        "engine",
        "max_power",
        "seats"
    ]

    for col in columns_to_check:
        check_distribution(col)