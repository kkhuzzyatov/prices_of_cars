import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def extract_numeric(column: pd.Series) -> pd.Series:
    """Извлекает числа из строковых колонок."""
    return (
        column.astype(str)
        .str.extract(r"(\d+\.?\d*)")[0]
        .astype(float)
    )


# Загрузка данных
df = pd.read_csv(BASE_DIR / "dataset" / "cardekho.csv")

# Отчёт файл
report_path = BASE_DIR / "generated_reports" / "replacing_skips_report.md"
report_path.parent.mkdir(parents=True, exist_ok=True)

report_lines = []
report_lines.append("# Отчёт о замене пропусков\n")

report_lines.append(f"- Исходное количество строк: {len(df)}\n")

# Замена некорректных значений
df = df.replace("?", pd.NA)

# --- numeric conversion ---
df["max_power"] = extract_numeric(df["max_power"])

if "mileage(km/ltr/kg)" in df.columns:
    df["mileage(km/ltr/kg)"] = extract_numeric(df["mileage(km/ltr/kg)"])

# ---- NUMERIC IMPUTATION ----
numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

report_lines.append("\n## Числовые признаки (median imputation)\n")

for col in numeric_columns:
    missing_before = df[col].isna().sum()
    median_value = df[col].median()

    df[col] = df[col].fillna(median_value)

    report_lines.append(f"### {col}")
    report_lines.append(f"- Пропусков до: {missing_before}")
    report_lines.append(f"- Заполнено значением (median): {median_value}")
    report_lines.append("")

# ---- CATEGORICAL IMPUTATION ----
categorical_columns = df.select_dtypes(include=["object"]).columns

report_lines.append("\n## Категориальные признаки (mode imputation)\n")

for col in categorical_columns:
    missing_before = df[col].isna().sum()
    mode_value = df[col].mode()[0]

    df[col] = df[col].fillna(mode_value)

    report_lines.append(f"### {col}")
    report_lines.append(f"- Пропусков до: {missing_before}")
    report_lines.append(f"- Заполнено значением (mode): {mode_value}")
    report_lines.append("")

# Сохранение очищенного датасета
output_path = BASE_DIR / "dataset" / "cardekho_clean.csv"
df.to_csv(output_path, index=False)

# Сохранение отчёта
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"Очищенный датасет сохранён: {output_path}")
print(f"Отчёт сохранён: {report_path}")