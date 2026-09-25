from dataclasses import dataclass
import numpy as np
import torch
from src.models.train import ClimateMLP

@dataclass
class TwinState:
    rainfall_mm: float
    tmax_c: float
    tmin_c: float

class DigitalTwin:
    def __init__(self, model_path="models/climate_mlp.pt"):
        self.model=ClimateMLP(9)
        try:
            self.model.load_state_dict(torch.load(model_path,map_location="cpu"))
            self.model.eval()
        except Exception:
            self.model=None

    def predict(self, history, temp_delta=0.0, rain_pct=0.0):
        h=np.array(history,dtype=np.float32)
        if h.shape != (3,3): raise ValueError("history must be 3x3: rainfall,tmax,tmin")
        h=h.copy()
        h[:,1]+=temp_delta
        h[:,0]*=(1+rain_pct/100)
        if self.model is None:
            return np.array([max(0,h[:,0].mean()*1.02), h[:,1].mean()+0.1])
        with torch.no_grad():
            return self.model(torch.tensor(h.reshape(1,-1))).numpy()[0]
