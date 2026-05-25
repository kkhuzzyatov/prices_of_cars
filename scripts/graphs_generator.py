import os
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "cardekho_without_skips.csv"

PLOTS_DIR = BASE_DIR / "plots"
DENSITY_DIR = PLOTS_DIR / "density"
DIST_DIR = PLOTS_DIR / "distribution"
SCATTER_DIR = PLOTS_DIR / "scatter"

# Загрузка данных
df = pd.read_csv(DATA_PATH)

selected_columns = [
    "engine",
    "km_driven",
    "max_power",
    "seats",
    "selling_price",
    "year"
]

existing_columns = [col for col in selected_columns if col in df.columns]

num_df = df[existing_columns].select_dtypes(include=["int64", "float64"])

# Папки
os.makedirs(DENSITY_DIR, exist_ok=True)
os.makedirs(DIST_DIR, exist_ok=True)
os.makedirs(SCATTER_DIR, exist_ok=True)


def safe_filename(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", str(name))

# Корреляционная матрица
corr = num_df.corr()

plt.figure(figsize=(10, 8))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    square=True,
    cbar=True
)

plt.title("Корреляционная матрица переменных")
plt.tight_layout()

plt.savefig(PLOTS_DIR / "correlation_matrix.png", dpi=300)
plt.close()

# Гистограммы плотности
for col in num_df.columns:
    series = num_df[col].dropna()

    if series.nunique() < 2:
        continue

    plt.figure(figsize=(6, 4))

    plt.hist(series, bins=30, density=True, alpha=0.6)
    series.plot(kind="kde")

    plt.title(f"Плотность переменной {col}")
    plt.xlabel(col)
    plt.ylabel("Плотность")

    plt.tight_layout()

    plt.savefig(DENSITY_DIR / f"density_{safe_filename(col)}.png", dpi=300)
    plt.close()


# Гистограммы распределения

for col in num_df.columns:
    series = num_df[col].dropna()

    if series.empty:
        continue

    plt.figure(figsize=(6, 4))

    plt.hist(series, bins=30, alpha=0.6)

    plt.title(f"Распределение переменной {col}")
    plt.xlabel(col)
    plt.ylabel("Количество")

    plt.tight_layout()

    plt.savefig(DIST_DIR / f"distribution_{safe_filename(col)}.png", dpi=300)
    plt.close()

# Boxplots
scaler = StandardScaler()

num_df_clean = num_df.fillna(num_df.median(numeric_only=True))

scaled_df = pd.DataFrame(
    scaler.fit_transform(num_df_clean),
    columns=num_df_clean.columns
)

plt.figure(figsize=(12, 6))
scaled_df.boxplot(rot=90)

plt.title("Boxplots для нормализованных числовых переменных")
plt.tight_layout()

plt.savefig(PLOTS_DIR / "boxplot.png", dpi=300)
plt.close()

# Диаграммы рассеивания
scatter_pairs = [
    ("selling_price", "engine"),
    ("selling_price", "year"),
    ("selling_price", "km_driven"),
    ("selling_price", "max_power"),
    ("selling_price", "seats")
]

for x_col, y_col in scatter_pairs:
    if x_col not in num_df.columns or y_col not in num_df.columns:
        continue

    x = num_df[x_col].dropna()
    y = num_df[y_col].dropna()

    common_index = x.index.intersection(y.index)

    x = x.loc[common_index]
    y = y.loc[common_index]

    if x.empty or y.empty:
        continue

    plt.figure(figsize=(6, 4))

    plt.scatter(x, y, alpha=0.5, s=10)

    plt.title(f"{x_col} vs {y_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)

    plt.tight_layout()

    filename = SCATTER_DIR / f"{safe_filename(x_col)}_vs_{safe_filename(y_col)}.png"

    plt.savefig(filename, dpi=300)
    plt.close()