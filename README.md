# Relative Wealth Index to GeoTIFF

[RWI (Relative Wealth Index)](https://dataforgood.fb.com/tools/relative-wealth-index/) is a dataset produced by Facebook that quantifies wealth at ~2.4km resolution in low- to middle-income countries.
These scripts download and unzip RWI data, and export them into a global GeoTIFF.

## Disclaimer

This code has not been formally tested, and while it appears to work as expected, [there are pieces that deserve review](https://github.com/jacobwhall/rwi-to-geotiff/blob/2caa88fbf1731a030e0b99ef4f388c6a9c6291fb/convert_data.py#L56-L64).
If you would like to chat about this project, or have me flesh it out further, please be in touch!

## Version

These scripts were written for the April 2021 update of RWI datasets.
If the data is updated in the future, make sure it is formatted the same way before running them.

## Instructions

1. Run download.sh
   
   ```
   bash download.sh
   ```
5. [Install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html), and create the conda environment environment.yml
   ```
   bash create_env.sh
   ```
   Conda will confirm that the environment was created, and give you the command to activate it:
   ```
   conda activate RWI
   ```
   Alternatively, you can install the appropriate Python 3 version and packages yourself.

6. Run convert_data.py to create GeoTIFF
   ```
   python prepare_daily.py
   ```

## References
https://arxiv.org/abs/2104.07761
