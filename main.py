from fastapi import FastAPI, File
from PIL import Image
from transformers import pipeline
from typing import Annotated
from io import BytesIO
import config

app = FastAPI()

@app.get("/")
def app_root():
    return "test"

@app.post("/api/eval-image")
def eval_image(file: Annotated[bytes, File()]):
    img = Image.open(BytesIO(file))

    classifier = pipeline(
        "image-classification",
        model=config.MODEL_NAME,
        token=config.HUGGINGFACE_TOKEN
    )

    result = classifier(img)
    nsfw_score = [x for x in result if x["label"] == "nsfw"][0]["score"]
    normal_score = [x for x in result if x["label"] == "normal"][0]["score"]
    return {"is_nsfw": (nsfw_score > normal_score)}
