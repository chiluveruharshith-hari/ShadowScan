from pydantic import BaseModel

class SMSRequest(BaseModel):
    text: str