"""
Building Materials & Home Features: Impact on Property Values
=============================================================
Analysis of the Ames Housing dataset (2930 properties) to understand
how construction materials, finishes, and quality ratings drive sale price.

Author: Tommy Nguyen
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import os

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "ames_housing.tsv")
VIS_DIR = os.path.join(os.path.dirname(__file__), "visuals")
os.makedirs(VIS_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.05)
PALETTE = "muted"
DPI = 150

# Helper: format y-axis as $K
def dollar_fmt(ax, axis="y"):
    fmt = ticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K")
    if axis == "y":
        ax.yaxis.set_major_formatter(fmt)
    else:
        ax.xaxis.set_major_formatter(fmt)


# ---------------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH, sep="\t")
print(f"Loaded {len(df)} properties, {df.shape[1]} columns\n")

# Quick sanity check
print(f"Sale price range: ${df['SalePrice'].min():,.0f} - ${df['SalePrice'].max():,.0f}")
print(f"Median sale price: ${df['SalePrice'].median():,.0f}\n")


# ===================================================================
# 1. EXTERIOR CLADDING MATERIAL vs SALE PRICE
# ===================================================================
# Group rare materials (< 30 properties) to keep the chart readable
ext_counts = df["Exterior 1st"].value_counts()
common_ext = ext_counts[ext_counts >= 30].index
df["Exterior_Clean"] = df["Exterior 1st"].where(
    df["Exterior 1st"].isin(common_ext), "Other"
)

# Order by median sale price
ext_order = (
    df.groupby("Exterior_Clean")["SalePrice"]
    .median()
    .sort_values(ascending=False)
    .index
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(
    data=df, x="Exterior_Clean", y="SalePrice",
    order=ext_order, hue="Exterior_Clean", palette=PALETTE, ax=ax,
    fliersize=2, legend=False
)
ax.set_title("Sale Price by Exterior Cladding Material", fontsize=14, fontweight="bold")
ax.set_xlabel("Exterior Material")
ax.set_ylabel("Sale Price")
dollar_fmt(ax)
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "01_exterior_material_vs_price.png"), dpi=DPI)
plt.close()
print("[OK] Chart 1 saved: Exterior material vs price")

# Print summary table
ext_summary = (
    df.groupby("Exterior_Clean")["SalePrice"]
    .agg(["median", "mean", "count"])
    .sort_values("median", ascending=False)
)
ext_summary["median"] = ext_summary["median"].map("${:,.0f}".format)
ext_summary["mean"] = ext_summary["mean"].map("${:,.0f}".format)
print(ext_summary.to_string())
print()


# ===================================================================
# 2. OVERALL QUALITY RATING vs SALE PRICE
# ===================================================================
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(
    data=df, x="Overall Qual", y="SalePrice",
    hue="Overall Qual", palette="YlOrRd", ax=ax, fliersize=2, legend=False
)
ax.set_title("Sale Price by Overall Quality Rating (1-10)", fontsize=14, fontweight="bold")
ax.set_xlabel("Overall Quality Rating")
ax.set_ylabel("Sale Price")
dollar_fmt(ax)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "02_overall_quality_vs_price.png"), dpi=DPI)
plt.close()
print("[OK] Chart 2 saved: Overall quality vs price")

# Median price per quality level
qual_med = df.groupby("Overall Qual")["SalePrice"].median()
print(f"  Quality 5 -> 7 median jump: ${qual_med[7] - qual_med[5]:,.0f}")
print(f"  Quality 7 -> 9 median jump: ${qual_med[9] - qual_med[7]:,.0f}")
print()


# ===================================================================
# 3. KITCHEN QUALITY vs SALE PRICE
# ===================================================================
kq_order = ["Po", "Fa", "TA", "Gd", "Ex"]
kq_labels = {
    "Po": "Poor", "Fa": "Fair", "TA": "Average", "Gd": "Good", "Ex": "Excellent"
}
df["Kitchen_Label"] = df["Kitchen Qual"].map(kq_labels)
kq_label_order = [kq_labels[k] for k in kq_order if k in df["Kitchen Qual"].values]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Box plot
sns.boxplot(
    data=df, x="Kitchen_Label", y="SalePrice",
    order=kq_label_order, hue="Kitchen_Label", palette="Blues", ax=axes[0],
    fliersize=2, legend=False
)
axes[0].set_title("Sale Price by Kitchen Quality", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Kitchen Quality")
axes[0].set_ylabel("Sale Price")
dollar_fmt(axes[0])

# Bar chart - median price
kq_medians = df.groupby("Kitchen_Label")["SalePrice"].median().reindex(kq_label_order)
axes[1].bar(kq_medians.index, kq_medians.values, color=sns.color_palette("Blues", len(kq_medians)))
axes[1].set_title("Median Sale Price by Kitchen Quality", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Kitchen Quality")
axes[1].set_ylabel("Median Sale Price")
dollar_fmt(axes[1])

# Annotate bars
for i, (label, val) in enumerate(kq_medians.items()):
    axes[1].text(i, val + 3000, f"${val/1000:.0f}K", ha="center", fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "03_kitchen_quality_vs_price.png"), dpi=DPI)
plt.close()
print("[OK] Chart 3 saved: Kitchen quality vs price")

premium = kq_medians["Excellent"] - kq_medians["Average"]
print(f"  Excellent vs Average kitchen premium: ${premium:,.0f}")
print()


# ===================================================================
# 4. FOUNDATION TYPE vs SALE PRICE
# ===================================================================
found_order = (
    df.groupby("Foundation")["SalePrice"]
    .median()
    .sort_values(ascending=False)
    .index
)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=df, x="Foundation", y="SalePrice",
    order=found_order, hue="Foundation", palette="Greens_r", ax=ax,
    estimator="median", errorbar=("ci", 95), legend=False
)
ax.set_title("Median Sale Price by Foundation Type", fontsize=14, fontweight="bold")
ax.set_xlabel("Foundation Type")
ax.set_ylabel("Median Sale Price")
dollar_fmt(ax)

# Add labels
foundation_labels = {
    "PConc": "Poured\nConcrete", "CBlock": "Cinder\nBlock",
    "BrkTil": "Brick &\nTile", "Slab": "Slab",
    "Stone": "Stone", "Wood": "Wood"
}
ax.set_xticklabels([foundation_labels.get(t.get_text(), t.get_text()) for t in ax.get_xticklabels()])

plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "04_foundation_vs_price.png"), dpi=DPI)
plt.close()
print("[OK] Chart 4 saved: Foundation type vs price")
print()


# ===================================================================
# 5. MASONRY VENEER TYPE vs SALE PRICE
# ===================================================================
# More interesting than roof material (which is 98.5% comp shingle)
df["Mas Vnr Type"] = df["Mas Vnr Type"].fillna("None")

vnr_order = (
    df.groupby("Mas Vnr Type")["SalePrice"]
    .median()
    .sort_values(ascending=False)
    .index
)

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(
    data=df, x="Mas Vnr Type", y="SalePrice",
    order=vnr_order, hue="Mas Vnr Type", palette="Set2", ax=ax,
    fliersize=2, legend=False
)
ax.set_title("Sale Price by Masonry Veneer Type", fontsize=14, fontweight="bold")
ax.set_xlabel("Masonry Veneer Type")
ax.set_ylabel("Sale Price")
dollar_fmt(ax)

vnr_labels = {
    "Stone": "Stone", "BrkFace": "Brick Face",
    "BrkCmn": "Common\nBrick", "None": "None",
    "CBlock": "Cinder Block"
}
ax.set_xticklabels([vnr_labels.get(t.get_text(), t.get_text()) for t in ax.get_xticklabels()])

plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "05_masonry_veneer_vs_price.png"), dpi=DPI)
plt.close()
print("[OK] Chart 5 saved: Masonry veneer type vs price")
print()


# ===================================================================
# 6. FEATURE COMBINATION HEATMAP — Quality Indicators & Price
# ===================================================================
# Map quality columns to numeric for correlation
qual_map = {"Po": 1, "Fa": 2, "TA": 3, "Gd": 4, "Ex": 5}

df["Kitchen_Num"] = df["Kitchen Qual"].map(qual_map)
df["Exter_Num"] = df["Exter Qual"].map(qual_map)
df["Heating_Num"] = df["Heating QC"].map(qual_map)
df["Bsmt_Num"] = df["Bsmt Qual"].map(qual_map)
df["Fireplace_Num"] = df["Fireplace Qu"].map(qual_map)

corr_cols = {
    "Overall Qual": "Overall Quality",
    "Kitchen_Num": "Kitchen Quality",
    "Exter_Num": "Exterior Quality",
    "Heating_Num": "Heating Quality",
    "Bsmt_Num": "Basement Quality",
    "Fireplace_Num": "Fireplace Quality",
    "Mas Vnr Area": "Masonry Veneer Area (sqft)",
    "Garage Cars": "Garage Capacity (cars)",
    "Total Bsmt SF": "Total Basement SF",
    "Gr Liv Area": "Above-Grade Living Area",
    "SalePrice": "Sale Price",
}

corr_df = df[list(corr_cols.keys())].rename(columns=corr_cols)
corr_matrix = corr_df.corr(numeric_only=True)

# Only show correlations with Sale Price for a focused view
price_corr = corr_matrix[["Sale Price"]].drop("Sale Price").sort_values(
    "Sale Price", ascending=False
)

fig, ax = plt.subplots(figsize=(8, 7))
sns.heatmap(
    price_corr, annot=True, fmt=".2f", cmap="YlOrRd",
    vmin=0, vmax=1, ax=ax, linewidths=0.5
)
ax.set_title("Correlation with Sale Price\n(Building Material & Quality Features)",
             fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "06_feature_correlation_heatmap.png"), dpi=DPI)
plt.close()
print("[OK] Chart 6 saved: Feature correlation heatmap")
print()

# Print the correlation values
print("Correlation with Sale Price (strongest to weakest):")
for feat, row in price_corr.iterrows():
    print(f"  {feat:30s}  r = {row['Sale Price']:.3f}")

print()


# ===================================================================
# SUMMARY — KEY FINDINGS
# ===================================================================
print("=" * 60)
print("KEY FINDINGS")
print("=" * 60)
print()
print("1. EXTERIOR MATERIAL")
top_ext = ext_summary.index[0]
print(f"   Highest median price: {top_ext} ({ext_summary.loc[top_ext, 'median']})")
print()

print("2. OVERALL QUALITY")
print(f"   Each quality point adds roughly ${(qual_med[8]-qual_med[4])/4:,.0f} to median price")
print(f"   Quality 10 median: ${qual_med[10]:,.0f}")
print()

print("3. KITCHEN QUALITY")
print(f"   Excellent kitchen premium over Average: ${premium:,.0f}")
print()

print("4. FOUNDATION")
found_med = df.groupby("Foundation")["SalePrice"].median().sort_values(ascending=False)
print(f"   Top foundation: {found_med.index[0]} (${found_med.iloc[0]:,.0f} median)")
print()

print("5. MASONRY VENEER")
vnr_med = df.groupby("Mas Vnr Type")["SalePrice"].median().sort_values(ascending=False)
top_vnr = vnr_med.index[0]
print(f"   Stone veneer median: ${vnr_med.get('Stone', 0):,.0f}")
print(f"   No veneer median: ${vnr_med.get('None', 0):,.0f}")
print()

print("6. STRONGEST CORRELATIONS")
print(f"   Overall Quality:   r = {corr_matrix.loc['Sale Price','Overall Quality']:.3f}")
print(f"   Kitchen Quality:   r = {corr_matrix.loc['Sale Price','Kitchen Quality']:.3f}")
print(f"   Exterior Quality:  r = {corr_matrix.loc['Sale Price','Exterior Quality']:.3f}")
print()
print("Done. All charts saved to visuals/")
