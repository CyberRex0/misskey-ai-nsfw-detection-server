from fastapi import Depends, FastAPI, File, HTTPException, Request
from starlette.datastructures import UploadFile
from PIL import Image
from fastapi.datastructures import FormData
from transformers import pipeline
from typing import Annotated, List
from io import BytesIO
import config

app = FastAPI()
MAX_FILE_SIZE_BYTES = 1024 * 1024 * 24

@app.get("/")
async def app_root():
    return "test"

async def validate_upload(request: Request):
    content_type = request.headers.get('Content-Type')
    if content_type is None:
        raise HTTPException(status_code=400, detail='No Content-Type provided!')
    elif (content_type.startswith('multipart/form-data')):
        try:
            return await request.form()
        except Exception:
            raise HTTPException(status_code=400, detail='Invalid Form data')
    else:
        raise HTTPException(status_code=400, detail='Content-Type not supported!')

@app.post("/v1/detect-images")
#async def eval_image(files: Annotated[list[bytes], File()]):
async def eval_image(body: FormData = Depends(validate_upload)):
    results: List[dict] = []
    files: List[UploadFile] = []

    for k in body:
        if k.startswith('image'):
            entries = body.getlist(k)
            for ff in entries:
                if isinstance(ff, UploadFile):
                    files.append(ff)
                
    for f in files:
        try:
            img = Image.open(BytesIO(await f.read()))

            classifier = pipeline(
                "image-classification",
                model=config.MODEL_NAME,
                token=config.HUGGINGFACE_TOKEN
            )

            result = classifier(img)
            nsfw_score = [x for x in result if x["label"] == "nsfw"][0]["score"]
            normal_score = [x for x in result if x["label"] == "normal"][0]["score"]

            is_nsfw = (nsfw_score > normal_score)

            results.append({
                'success': True,
                'predictions': [
                    { 'className': 'Neutral', 'probability': 1.0 if not is_nsfw else 0.0 },
                    { 'className': 'Sexy', 'probability': 1.0 if is_nsfw else 0.0 },
                    { 'className': 'Hentai', 'probability': 1.0 if is_nsfw else 0.0 }
                ]
            })
        except Exception as e:
            results.append({
                'success': False,
                'error': {
                    'code': 'FAILED',
                    'message': 'Error occured while processing image:\n' + str(e)
                }
            })

    return {
        'success': True,
        'result': {
            'results': results
        }
    }
