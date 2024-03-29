import base64
import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utilities.endpoint_configs import EndpointConfigManager
from utilities.data_models import Text2VideoRequest, Image2VideoRequest
from main import main as generate_video_main
import loguru
from PIL import Image

logger = loguru.logger

manager = EndpointConfigManager()
config = manager.text2video

logger.debug(config.url)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("data", exist_ok=True)
app.mount("/data", StaticFiles(directory="data"), name="data")


@app.get("/")
def root():
    return "/docs for more information"


@logger.catch()
@app.post(f"{config.endpoint}")
def video_generation(request: Text2VideoRequest):
    logger.info("Generating Video")
    logger.debug(request)
    try:
        filename = generate_video_main(
            request.prompt,
        )
        video_path = f"data/{filename}.mp4"
        with open(video_path, "rb") as f:
            base64_video = base64.b64encode(f.read()).decode("utf-8")
        return JSONResponse(
            content={
                "video": base64_video,
                "video_filename": filename,
                "gif_filename": filename,
                "image_filename": filename,
            },
            status_code=200,
        )

    except HTTPException as e:
        logger.exception(e)
        return JSONResponse({"error": str(e)}, status_code=500)


@logger.catch()
@app.post(f"{config.endpoint}/image")
def video_from_image(request: Image2VideoRequest):
    if not request.image:
        raise ValueError("No image provided")
    image = request.image
    image_path = "image.png"
    decoded_image = from_base64(image)
    with open(image_path, "wb") as f:
        f.write(decoded_image)
    logger.info("Generating Video")
    logger.debug(request)
    try:
        filename = generate_video_main(request.prompt, image_file=image_path)
        video_path = f"data/{filename}.mp4"
        with open(video_path, "rb") as f:
            base64_video = base64.b64encode(f.read()).decode("utf-8")
        video_response = {
            "video": base64_video,
            "video_filename": filename,
            "gif_filename": filename,
            "image_filename": filename,
        }
        return JSONResponse(
            content=video_response,
            status_code=200,
        )

    except HTTPException as e:
        logger.exception(e)
        return JSONResponse({"error": str(e)}, status_code=500)


def from_base64(base64_string):
    return base64.b64decode(base64_string)


@logger.catch()
def to_base64(file):
    return base64.b64encode(open(file, "rb").read()).decode("utf-8")


if __name__ == "__main__":
    print(
        f"""
Starting API on {config.url}
"""
    )
    uvicorn.run("api:app", host=config.host, port=int(config.port), reload=True)