from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    health_check: str | None = None
    Response: str | None = None

    class Config:
        schema_extra = {
            "example": {
            "health_check": "PASS",
            "Response": "<bound method BaseLLM.__str__ of OpenAI(...)>"
            }
        }