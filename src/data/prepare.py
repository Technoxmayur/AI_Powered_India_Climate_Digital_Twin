import argparse
from pathlib import Path
import pandas as pd
import numpy as np

COLUMNS = ["date","lat","lon","rainfall_mm","tmax_c","tmin_c"]

def normalize(df):
    rename = {c:c.lower().strip().replace(" ","_") for c in df.columns}
    df = df.rename(columns=rename)
    aliases = {
        "temperature_max":"tmax_c","max_temp":"tmax_c","tmax":"tmax_c",
        "temperature_min":"tmin_c","min_temp":"tmin_c","tmin":"tmin_c",
        "rain":"rainfall_mm","rain":"rainfall_mm","rainfall":"rainfall_mm"
    }
    df = df.rename(columns={k:v for k,v in aliases.items() if k in df.columns})
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}. Expected {COLUMNS}")
    df["date"] = pd.to_datetime(df["date"])
    for c in COLUMNS[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["date","lat","lon"])
    return df.sort_values(["lat","lon","date"]).reset_index(drop=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default="data/raw")
    ap.add_argument("--output",default="data/processed/climate.csv")
    a=ap.parse_args()
    files=list(Path(a.input).glob("*.csv"))
    if not files: raise SystemExit("No CSV found. Convert downloaded data to the documented long-table CSV first.")
    df=normalize(pd.concat([pd.read_csv(f) for f in files],ignore_index=True))
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(a.output,index=False)
    print(a.output, len(df))
if __name__=="__main__": main()
