from pydantic import BaseModel


class LaunchFile(BaseModel):
    path: str
