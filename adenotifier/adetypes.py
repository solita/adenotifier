from pydantic import BaseModel
from typing import List, Optional


class Ade_manifest_attributes(BaseModel):
    """
    Represents the attributes of an ADE manifest.
    """
    ade_source_system: str
    ade_source_entity: str
    batch_from_file_path_regex: Optional[str] = None
    path_replace: Optional[str] = None
    path_replace_with: Optional[str] = None
    single_file_manifest: Optional[str] = None
    max_files_in_manifest: Optional[int] = 1000


class Ade_manifest_parameters(BaseModel):
    """
    Represents the parameters of an ADE manifest.
    """
    columns: Optional[List[str]]
    compression: Optional[str] = None
    delim: Optional[str] = None
    format: str
    fullscanned: Optional[bool] = None
    skiph: Optional[int] = None


class Ade_Datasource(BaseModel):
    """
    Represents an ADE datasource.
    """
    id: str
    attributes: Ade_manifest_attributes
    manifest_parameters: Ade_manifest_parameters
