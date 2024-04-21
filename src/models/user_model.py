from dataclasses import dataclass
from typing import Union, Optional

from ..file_handlers.base import BasePhoto, BaseFile
from ..payment import paymentFactory


@dataclass
class FileModel:
    filename: str
    file_bytes: bytes 
    document: BaseFile
    num_pages: int      # Количество страниц в файле


@dataclass
class PhotoModel:
    filename: str
    document: list[BasePhoto]
    num_pages: int


@dataclass
class UserData:
    uid: int
    username: str
    file_data: Union[FileModel, PhotoModel]
    num_copies: Optional[int] = None 
    payment_id: Optional[str] = None 
    value: Optional[int] = None
    payment_action: Optional[paymentFactory] = None 
