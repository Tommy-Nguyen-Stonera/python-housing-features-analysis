# Housing Feature Impact Analysis (Python)

[View Interactive Report](https://htmlpreview.github.io/?https://raw.githubusercontent.com/Tommy-Nguyen-Stonera/python-housing-features-analysis/main/report.html)

## Overview

This project analyses the Ames Housing dataset to quantify how specific building materials and finishes drive property sale price. The goal was to answer which individual features add the most dollar value, and whether overall quality rating overshadows specific material choices when predicting price.

## Dataset

- Source: Ames Housing Dataset (ames_housing.tsv)
- Record count: 2,930 rows
- Key columns analysed: SalePrice, OverallQual, ExterMaterial, KitchenQual, Foundation, MasVnrType
- Single flat table, no joins required

## Research Questions

1. Does exterior material choice have a measurable impact on sale price?
2. How much does overall quality rating affect price compared to individual material features?
3. What is the dollar impact of kitchen quality from the lowest to highest grade?
4. Do foundation types show a consistent price premium, and how large is it?
5. Does masonry veneer type add measurable value, and which type adds the most?
6. Which feature combination most strongly correlates with higher sale prices?

## Data Model

Single flat table: ames_housing. Each row is one residential property sale with structural and finish attributes alongside the final sale price. All analysis is done within this one table using groupby aggregations and correlation calculations.

## What Was Analysed

- Median sale price by exterior material type, ranked across all material categories
- Correlation between overall quality rating and sale price vs individual feature correlations
- Median sale price by kitchen quality grade (Poor, Fair, Typical, Good, Excellent)
- Median sale price by foundation type
- Median sale price by masonry veneer type (None, BrkFace, Stone, etc.)
- Combined feature combinations ranked by median sale price

## Key Insights

1. Overall quality rating is the strongest single predictor of sale price, outperforming any individual material or finish feature on its own.
2. Kitchen quality upgrade from Average to Excellent adds over $80K to median sale price, making it one of the highest-return individual improvements in the dataset.
3. Stone masonry veneer adds $102K to median price compared to no veneer ($245K vs $143K), the largest single-feature premium in the analysis.
4. Poured concrete foundations sit at a $208K median, which is $43K above cinder block foundations. The premium is consistent across property sizes.
5. Exterior material choice spans $103K in median price from metal siding at $135K to cement board at $238K, a wider range than most buyers would expect from a single exterior decision.
6. Properties combining high overall quality with stone veneer and excellent kitchen quality consistently sit in the top price tier, confirming that features compound rather than average out.

## Recommendations

1. For renovation ROI, prioritise kitchen quality upgrades before exterior cosmetic work. The $80K+ price lift from kitchen quality improvement is the most reliable single-feature investment in this dataset.
2. Consider masonry veneer seriously as a value-add for properties in the mid-price tier. The $102K premium for stone veneer is large relative to the installation cost in most markets.
3. Do not overlook foundation type when evaluating properties for purchase or renovation. The $43K gap between poured concrete and cinder block is not widely priced into buyer expectations but shows up consistently in the data.
4. Use overall quality rating as the primary screening filter when comparing properties. Individual features matter, but overall quality is the best single proxy for final price and is harder to manipulate through cosmetic improvements alone.

## Tools

Python 3.12, Pandas, Matplotlib, Seaborn

## Files

- `analysis.py` - Full analysis script
- `report.html` - Interactive report with 6 embedded charts
- `ames_housing.tsv` - Source dataset
- `visuals/` - 6 chart PNGs
