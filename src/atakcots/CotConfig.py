from typing import Optional, Union, List
from pydantic import BaseModel, Field, field_validator

import json


class CotConfig(BaseModel):
    """
    Config model which defines cursor on target information and attachments

    For more CoT schema information, see
        https://www.mitre.org/sites/default/files/pdf/09_4937.pdf    
    """
    
    uid: str = Field(description="") # TODO: use uuid4 and validator, use callsign in examples
    latitude: float = Field(description="Latitude referred to the WGS 84 ellipsoid in degrees")
    longitude: float = Field(description="Longitude referred to the WGS 84 in degrees")
    altitude: float = Field(default= 0.0, description="Height above the WGS ellipsoid in meters")

    stale_duration: int = Field(default=600, description="Number of seconds before cot message becomes stale")

    callsign: str = Field(default="default_callsign", description="Callsign of event described by cot")
    attitude: str = Field(default="x", description="Attitude of cot type field")
    dimension: str = Field(default="G", description="Dimension of cot type field")
    how: str = Field(default="m-g", description="Gives a hint about how the coordinates were generated")

    sender_callsign: str = Field(default="", description="Callsign of the entity sendering the cot")
    sender_uid: str = Field(default="default_sender_uid", description="Unique identifier of the entity sendering the cot")

    package_name: str = Field(default="data_package", description="Name of data package which contains attachments")
    attachment_paths: List[str] = Field(default=[], description="Paths to files to be attached to the cot. Can either be a string, a list of strings, or None")
    

    @field_validator("attachment_paths", mode="before")
    def force_list(cls, value: Optional[Union[str, List[str]]]) -> List[str]:
        if value is None:
            return []
        
        if isinstance(value, str):
            return [value]
        
        return value


    def __hash__(self) -> int:
        dict_repr = self.model_dump(mode="json")
        str_repr = json.dumps(dict_repr)
        return hash(str_repr)
