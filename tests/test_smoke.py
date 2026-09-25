import pandas as pd
from src.twin.engine import DigitalTwin
def test_sample_prediction():
    df=pd.read_csv("data/sample/pilot_climate.csv")
    h=df[df.region=="Mumbai"].tail(3)[["rainfall_mm","tmax_c","tmin_c"]].to_numpy()
    p=DigitalTwin().predict(h)
    assert len(p)==2
    assert p[0]>=0
