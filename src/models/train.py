import argparse, json
from pathlib import Path
import numpy as np, pandas as pd, torch
from torch import nn
from sklearn.metrics import mean_absolute_error, mean_squared_error

FEATURES=["rainfall_mm","tmax_c","tmin_c"]

class ClimateMLP(nn.Module):
    def __init__(self, n=9):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(n,64),nn.ReLU(),nn.Linear(64,32),nn.ReLU(),nn.Linear(32,2))
    def forward(self,x): return self.net(x)

def make_xy(df, lag=3):
    rows=[]
    for (lat,lon),g in df.groupby(["lat","lon"]):
        g=g.sort_values("date").reset_index(drop=True)
        for i in range(lag,len(g)):
            hist=g.loc[i-lag:i-1,FEATURES].to_numpy().reshape(-1)
            y=g.loc[i,["rainfall_mm","tmax_c"]].to_numpy(dtype=float)
            if np.isfinite(hist).all() and np.isfinite(y).all(): rows.append((hist,y))
    X=np.array([r[0] for r in rows],dtype=np.float32); y=np.array([r[1] for r in rows],dtype=np.float32)
    return X,y

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",default="data/processed/climate.csv")
    ap.add_argument("--out",default="models")
    ap.add_argument("--epochs",type=int,default=40)
    a=ap.parse_args()
    df=pd.read_csv(a.data)
    X,y=make_xy(df)
    if len(X)<10: raise SystemExit("Not enough training rows.")
    cut=max(1,int(len(X)*.8))
    xt,yt=torch.tensor(X[:cut]),torch.tensor(y[:cut])
    xv,yv=torch.tensor(X[cut:]),torch.tensor(y[cut:])
    model=ClimateMLP(X.shape[1]); opt=torch.optim.Adam(model.parameters(),lr=1e-3); loss=nn.MSELoss()
    for _ in range(a.epochs):
        opt.zero_grad(); pred=model(xt); l=loss(pred,yt); l.backward(); opt.step()
    with torch.no_grad(): pv=model(xv).numpy()
    mae=mean_absolute_error(yv.numpy(),pv); rmse=mean_squared_error(yv.numpy(),pv)**0.5
    Path(a.out).mkdir(exist_ok=True)
    torch.save(model.state_dict(),Path(a.out)/"climate_mlp.pt")
    json.dump({"mae":float(mae),"rmse":float(rmse),"samples":len(X)},open(Path(a.out)/"metrics.json","w"),indent=2)
    print(json.dumps({"mae":mae,"rmse":rmse,"samples":len(X)},indent=2))
if __name__=="__main__": main()
