from dataclasses import dataclass


@dataclass
class UserCRUDModel:
    uid: int 
    username: str | None 
    