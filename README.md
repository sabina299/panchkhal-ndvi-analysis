# Multi-Temporal NDVI Analysis for Agricultural Monitoring
**Panchkhal Region, Kavre District, Nepal**

## Overview
This project analyzes seasonal vegetation dynamics in Nepal's middle hill agriculture using Sentinel-2 satellite imagery and Python-based remote sensing tools. The analysis tracks crop development across the 2025 growing season through calculation and visualization of the Normalized Difference Vegetation Index (NDVI).

## Study Area
Panchkhal and surrounding agricultural areas in Kavre District, Nepal. The region features terraced agriculture typical of middle hill environments, with rice as the dominant summer crop.

## Data
- **Source:** Sentinel-2 Level 2A satellite imagery (ESA Copernicus)
- **Dates:** May 16, September 25, October 13, 2025
- **Resolution:** 10 meters
- **Coverage:** ~2,400 hectares

## Methods
1. Downloaded cloud-free Sentinel-2 scenes from Copernicus Open Access Hub
2. Extracted Red (Band 4) and Near-Infrared (Band 8) spectral bands
3. Calculated NDVI using formula: `(NIR - Red) / (NIR + Red)`
4. Generated GeoTIFF outputs for spatial analysis
5. Created professional cartographic maps using QGIS

## Key Findings
- Mean NDVI increased from **0.326 (May)** to **0.478 (October)** — a 47% increase
- Progression demonstrates healthy crop development through growing season
- Peak vegetation observed in late September (Mean NDVI: 0.438)
- Spatial variability indicates opportunities for precision agriculture applications

## Tools & Technologies
- **Python 3.9** - Data processing and analysis
- **Libraries:** rasterio, numpy, pandas
- **QGIS 3.28** - Cartographic visualization
- **Sentinel-2** - Satellite imagery source

## Results

### Temporal NDVI Progression
| Date | Mean NDVI | Max NDVI | Min NDVI |
|------|-----------|----------|----------|
| May 16, 2025 | 0.326 | 0.667 | -0.353 |
| September 25, 2025 | 0.438 | 1.000 | -0.456 |
| October 13, 2025 | 0.478 | 1.000 | -0.261 |

### Maps

![May NDVI](NDVI_May.jpg)
*Figure 1: NDVI distribution in May 2025 showing early crop establishment. Red areas indicate bare soil, green shows established vegetation.*

![September NDVI](NDVI_September.jpg)
*Figure 2: NDVI in September 2025 showing peak vegetation. Predominance of green indicates healthy crop canopies.*

![October NDVI](NDVI_October.jpg)
*Figure 3: NDVI in October 2025 showing mature crops approaching harvest.*

## Repository Contents
```
├── ndvi_analysis.py          # Main processing script
├── ndvi_summary.csv          # Summary statistics
├── NDVI_May.jpg              # May NDVI map
├── NDVI_September.jpg        # September NDVI map
├── NDVI_October.jpg          # October NDVI map
└── README.md                 # This file
```

## Usage
```python
# Process Sentinel-2 data and calculate NDVI
python ndvi_analysis.py
```

The script processes Sentinel-2 .SAFE files, calculates NDVI, and exports GeoTIFF files for visualization in QGIS.

## Applications
- Agricultural monitoring and crop health assessment
- Precision agriculture planning and management
- Seasonal vegetation dynamics analysis
- Variable rate management zone identification

## Future Work
- Multi-year analysis for inter-annual comparison
- Integration with ground-based validation data
- Additional spectral indices (NDWI, GNDVI, EVI)
- Crop yield correlation modeling

## Author
Sabina Pandit

## Acknowledgments
Satellite data provided by the European Space Agency's Copernicus Programme.






