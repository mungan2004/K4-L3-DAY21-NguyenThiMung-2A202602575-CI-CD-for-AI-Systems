from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure.storage.blob import BlobServiceClient
import joblib
import os

app = FastAPI()

# Chuỗi kết nối Azure được truyền qua biến môi trường AZURE_STORAGE_CONNECTION_STRING
CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
ARTIFACT_CONTAINER = os.environ.get("ARTIFACT_BUCKET")  # Dùng chung biến môi trường cho tiện
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")


def download_model():
    """
    Tải file model.joblib từ cloud storage về máy khi server khởi động.
    """
    if CONNECTION_STRING:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=ARTIFACT_CONTAINER, blob=MODEL_KEY)
        
        with open(MODEL_PATH, "wb") as f:
            f.write(blob_client.download_blob().readall())
        print("Model đã được tải xuống từ Azure Blob Storage.")
    else:
        print("WARNING: AZURE_STORAGE_CONNECTION_STRING not set. Model download skipped if running locally.")

download_model()
model = joblib.load(MODEL_PATH)


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    """
    Endpoint kiem tra suc khoe server.
    GitHub Actions goi endpoint nay sau khi deploy de xac nhan server dang chay.

    Tra ve: {"status": "ok"}
    """
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    """
    Endpoint suy luan chinh.

    Dau vao : JSON {"features": [f1, f2, ..., f10]}
    Dau ra  : JSON {"prediction": <0|1>, "label": <"thu_nhap_thap"|"thu_nhap_cao">}

    Thu tu 10 dac trung (khop voi thu tu trong FEATURE_NAMES cua test):
        age, workclass, education_num, marital_status, occupation,
        relationship, sex, capital_gain, capital_loss, hours_per_week
    """
    if len(req.features) != 10:
        raise HTTPException(status_code=400, detail="Expected 10 features (adult income)")

    pred = model.predict([req.features])[0]
    label = "thu_nhap_cao" if pred == 1 else "thu_nhap_thap"

    return {"prediction": int(pred), "label": label}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
