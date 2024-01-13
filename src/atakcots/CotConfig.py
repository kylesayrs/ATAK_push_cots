from typing import Optional, Union, List
from pydantic import BaseModel, Field, field_validator

import json


class CotConfig(BaseModel):
    """
    Config model which defines cursor on target information and attachments

    For more CoT schema information, see
        https://www.mitre.org/sites/default/files/pdf/09_4937.pdf    
    """
    
    uid: str = Field(description="")
    latitude: float = Field(description="TODO")
    longitude: float = Field(description="TODO")

    stale_duration: int = Field(default=600, description="Number of seconds before cot message becomes stale")

    callsign: str = Field(default="default callsign", description="TODO")
    attitude: str = Field(default="x", description="TODO")
    dimension: str = Field(default="G", description="TODO")
    how: str = Field(default="m-g", description="TODO")

    sender_callsign: str = Field(default="", description="TODO")
    sender_uid: str = Field(default="default_sender_uid", description="TODO")

    manifest_name: str = Field(default="manifest", description="TODO")  # TODO: check, but pretty sure this is totally irrelevant
    
    attachment_paths: List[str] = Field(default=[], description="TODO")
    

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
