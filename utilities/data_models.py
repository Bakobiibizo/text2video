from pydantic import BaseModel
from typing import Optional

class Text2VideoRequest(BaseModel):
    prompt: Optional[str] = None
    fps: Optional[int] = 129


class Image2VideoRequest(BaseModel):
    image: Optional[str] = None
    prompt: Optional[str] = None
    fps: Optional[int] = 129
