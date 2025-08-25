from fastapi import FastAPI
from pydantic import BaseModel
import joblib, os

app = FastAPI(title="RetailDemand360 Forecast API")
MODEL_PATH = os.environ.get("MODEL_PATH","./artifacts/demand_xgb.pkl")
_model = joblib.load(MODEL_PATH)

class ForecastIn(BaseModel):
    store_id: str
    product_id: str
    avg_units_alltime: float = 0.0

@app.post("/forecast")
def forecast(inp: ForecastIn):
    store_ix = hash(inp.store_id) % 1000
    product_ix = hash(inp.product_id) % 10000
    X = [[store_ix, product_ix, inp.avg_units_alltime]]
    yhat = float(_model.predict(X)[0])
    return {"store_id": inp.store_id, "product_id": inp.product_id, "forecast_units": yhat}
