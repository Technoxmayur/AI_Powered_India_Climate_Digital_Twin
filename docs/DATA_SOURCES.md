# National dataset sources

Official sources supplied in the challenge:

1. IMD gridded rainfall:
   https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_Bin.html
2. IMD maximum temperature:
   https://www.imdpune.gov.in/cmpg/Griddata/Max_1_Bin.html
3. IMD minimum temperature:
   https://www.imdpune.gov.in/cmpg/Griddata/Min_1_Bin.html
4. MOSDAC:
   https://www.mosdac.gov.in/

INSAT products named by the challenge:
- 3RIMG_L2B_LST
- 3RIMG_L2B_SST
- 3RIMG_L2B_IMC

Observed IMD specifications used by this PoC:
- Rainfall: 0.25 x 0.25 degree daily grid, 1901-2024, 135 x 129 grid points.
- Max temperature: 1 x 1 degree daily grid, 1951-2024, 31 x 31 grid points.
- Min temperature: 1 x 1 degree daily grid, 1951-2024, 31 x 31 grid points.

Important:
This package does NOT pretend to contain restricted/login-gated MOSDAC files.
Use the official portal to download authorized data and place them in data/raw.
The adapters accept CSV/NetCDF and the normalizer converts them into the common
long-table schema used by the model and dashboard.
