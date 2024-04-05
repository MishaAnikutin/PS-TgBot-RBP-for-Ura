from dataclasses import dataclass
from ..file_handlers.document import BaseFile
from ..payment import paymentFactory


@dataclass
class FileModel:
    filename: str
    file_bytes: bytes 
    document: BaseFile
    # Количество страниц в файле
    num_pages: int


@dataclass
class UserData:
    uid: int
    username: str
    file_data: FileModel
    num_copies: int | None = None 
    payment_id: str | None = None 
    value: int | None = None
    payment_action: paymentFactory | None = None 
    