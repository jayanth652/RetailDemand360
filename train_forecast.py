import pandas as pd
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import joblib, glob
try:
    import mlflow
    MLFLOW=True
except Exception:
    MLFLOW=False

def load_features():
    import pyarrow.parquet as pq
    files = glob.glob("./features/snapshot/*.parquet")
    if not files:
        raise FileNotFoundError("No features found. Run feature_store/feature_build.py first.")
    df = pq.read_table(files[0]).to_pandas()
    df["store_ix"] = df["store_id"].astype("category").cat.codes
    df["product_ix"] = df["product_id"].astype("category").cat.codes
    X = df[["store_ix","product_ix","avg_units_alltime"]].fillna(0.0)
    y = df["units"]
    return X, y

def main():
    X, y = load_features()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.08, subsample=0.9, colsample_bytree=0.8, random_state=42)
    model.fit(Xtr, ytr)
    preds = model.predict(Xte)
    mae = float(mean_absolute_error(yte, preds))
    if MLFLOW:
        mlflow.set_experiment("RetailDemand360")
        with mlflow.start_run():
            mlflow.log_metric("mae", mae)
            mlflow.sklearn.log_model(model, "model")
    joblib.dump(model, "./artifacts/demand_xgb.pkl")
    print("MAE:", mae)

if __name__ == "__main__":
    main()
