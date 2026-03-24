"""
Multi-Temporal NDVI Analysis for Agricultural Monitoring
Panchkhal Region, Kavre District, Nepal

Purpose: Process Sentinel-2 imagery to calculate NDVI for crop monitoring
"""

import rasterio
from rasterio.windows import Window
import numpy as np
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# Configuration
BASE_FOLDER = r"C:\Users\sabee\Downloads\NDVI"
OUTPUT_FOLDER = os.path.join(BASE_FOLDER, "processed_ndvi")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_date_from_filename(safe_path):
    """Extract acquisition date from Sentinel-2 filename."""
    name = safe_path.name
    date_str = name.split('_')[2][:8]
    return datetime.strptime(date_str, '%Y%m%d')

def calculate_ndvi(safe_path, crop_size=4000):
    """
    Calculate NDVI from Sentinel-2 .SAFE file.
    
    Parameters:
    safe_path: Path to Sentinel-2 .SAFE folder
    crop_size: Size of cropped area in pixels
    
    Returns: Dictionary with NDVI array, statistics, and metadata
    """
    
    print(f"\nProcessing: {safe_path.name}")
    
    granule_folder = safe_path / "GRANULE"
    img_folder = list(granule_folder.glob("*/IMG_DATA/R10m"))[0]
    
    red_file = list(img_folder.glob("*_B04_10m.jp2"))[0]
    nir_file = list(img_folder.glob("*_B08_10m.jp2"))[0]
    
    with rasterio.open(red_file) as src:
        full_width = src.width
        full_height = src.height
        crs = src.crs
        transform = src.transform
    
    center_x = full_width // 2
    center_y = full_height // 2
    col_start = max(0, center_x - crop_size // 2)
    row_start = max(0, center_y - crop_size // 2)
    
    window = Window(col_start, row_start, crop_size, crop_size)
    
    with rasterio.open(red_file) as src:
        red = src.read(1, window=window).astype(float)
        window_transform = src.window_transform(window)
    
    with rasterio.open(nir_file) as src:
        nir = src.read(1, window=window).astype(float)
    
    ndvi = (nir - red) / (nir + red)
    ndvi = np.where((nir + red) == 0, np.nan, ndvi)
    
    stats = {
        'date': extract_date_from_filename(safe_path),
        'mean_ndvi': np.nanmean(ndvi),
        'max_ndvi': np.nanmax(ndvi),
        'min_ndvi': np.nanmin(ndvi)
    }
    
    print(f"  Date: {stats['date'].strftime('%B %d, %Y')}")
    print(f"  Mean NDVI: {stats['mean_ndvi']:.3f}")
    
    return {
        'ndvi': ndvi,
        'stats': stats,
        'crs': crs,
        'transform': window_transform
    }

def save_ndvi_geotiff(ndvi_data, output_path):
    """Save NDVI as GeoTIFF for QGIS visualization."""
    
    with rasterio.open(
        output_path, 'w', driver='GTiff',
        height=ndvi_data['ndvi'].shape[0],
        width=ndvi_data['ndvi'].shape[1],
        count=1, dtype=ndvi_data['ndvi'].dtype,
        crs=ndvi_data['crs'],
        transform=ndvi_data['transform'],
        nodata=np.nan
    ) as dst:
        dst.write(ndvi_data['ndvi'], 1)
    
    print(f"  Saved: {output_path}")

def main():
    """Main processing workflow."""
    
    print("NDVI Analysis - Panchkhal Region, Kavre District")
    print("="*60)
    
    safe_folders = sorted(list(Path(BASE_FOLDER).glob("*.SAFE")))
    
    if not safe_folders:
        print("No Sentinel-2 data found!")
        return
    
    print(f"Found {len(safe_folders)} images\n")
    
    all_stats = []
    
    for safe_folder in safe_folders:
        ndvi_data = calculate_ndvi(safe_folder)
        
        date_str = ndvi_data['stats']['date'].strftime('%Y%m%d')
        output_file = os.path.join(OUTPUT_FOLDER, f"NDVI_{date_str}.tif")
        save_ndvi_geotiff(ndvi_data, output_file)
        
        all_stats.append(ndvi_data['stats'])
    
    summary_df = pd.DataFrame([
        {
            'Date': s['date'].strftime('%B %d, %Y'),
            'Mean_NDVI': f"{s['mean_ndvi']:.3f}",
            'Max_NDVI': f"{s['max_ndvi']:.3f}",
            'Min_NDVI': f"{s['min_ndvi']:.3f}"
        }
        for s in all_stats
    ])
    
    print("\nSummary:")
    print(summary_df.to_string(index=False))
    
    summary_file = os.path.join(OUTPUT_FOLDER, "ndvi_summary.csv")
    summary_df.to_csv(summary_file, index=False)
    
    print(f"\nProcessing complete! Output: {OUTPUT_FOLDER}")

if __name__ == "__main__":
    main()