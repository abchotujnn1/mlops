from fastapi import FastAPI
import torch
import numpy as np
from pydantic import BaseModel

from fastapi import FastAPI
from contextlib import asynccontextmanager
import torch

MODEL_PATH = "/models/model.pt"

class Input(BaseModel):
    data: list[list[float]]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.model = torch.jit.load(MODEL_PATH)
    app.state.model.eval()
    print("Model loaded and ready.")
    
    yield  # Application runs here
    
    # Shutdown
    print("Shutting down... cleaning up resources if needed.")

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
async def predict(req: Input):
    model = app.state.model
    print("---"*10)
    print("req_data:", req.data)
    x = torch.tensor(req.data, dtype=torch.float32)
    print("x_tensor:", x.shape)
    with torch.no_grad():
        y = model(x)
        print("y_output:", y)
        y = y.numpy().tolist()
    return {"predictions": y}
