# Housing Feature Impact Analysis (Python)

[View Interactive Report](https://htmlpreview.github.io/?https://raw.githubusercontent.com/Tommy-Nguyen-Stonera/python-housing-features-analysis/main/report.html)

Analysis of the Ames Housing dataset to understand how building materials and finishes drive property value. Examines exterior materials, kitchen quality, foundation types, and masonry veneer impact on sale price.

## Key Findings

- Overall quality rating is the strongest single predictor of sale price
- Kitchen quality upgrade from Average to Excellent adds $80K+ to median price
- Stone masonry veneer adds $102K to median price compared to no veneer ($245K vs $143K)
- Poured concrete foundations sit at $208K median, $43K above cinder block
- Exterior material choice spans $103K in median price from metal siding ($135K) to cement board ($238K)

## Tools

Python 3.12, Pandas, Matplotlib, Seaborn

## Files

- `analysis.py` - Full analysis script
- `report.html` - Interactive report with 6 embedded charts
- `ames_housing.tsv` - Source dataset
- `visuals/` - 6 chart PNGs
