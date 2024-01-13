from typing import Optional, Union, List
from pydantic import BaseModel, Field, field_validator

import json
import hashlib


class CotConfig(BaseModel):
    uid: str = Field(description="")
    latitude: float = Field(default=None, description="")
    longitude: float = Field(default=None, description="")

    stale_duration: int = Field(default=600, description="Number of seconds before cot message becomes stale")

    callsign: str = Field(default="default callsign")
    attitude: str = Field(default="x")
    dimension: str = Field(default="G")
    how: str = Field(default="m-g")

    sender_callsign: str = Field(default="", )
    sender_uid: str = Field(default="default_sender_uid")

    manifest_name: str = Field(default="manifest")  # TODO: check, but pretty sure this is totally irrelevant
    
    attachment_paths: List[str] = Field(default=[], description="")
    

    @field_validator("attachment_paths", mode="before")
    def force_list(cls, value: Optional[Union[str, List[str]]]) -> List[str]:
        if value is None:
            return []
        
        if isinstance(value, str):
            return [value]
        
        return value


    def __hash__(self) -> bytes:
        dict_repr = self.model_dump(mode="json")
        str_repr = json.dumps(dict_repr)
        return hash(str_repr)
