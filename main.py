from typing import List, Optional, Tuple

from pydantic import BaseModel, validator

calificaciones: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]

queseyo: Tuple[int] = [1, 2, 3, 4, 5, 6, 7, 8]

def promedio(calif: List[int]) -> float:
    return sum(calif) / len(calif)


class User(BaseModel):
    username: str 
    password: str
    name: Optional[str]

    @validator('username')
    def username_validation_length():
        if len(username) < 3:
            raise ValueError('Nombre de usuario demasiado corto')
        elif len(username) > 50:
            raise ValueError('Nomrde demasiado largo')

        return username


user1 = User(
    username = 'fedeturi',
    password = 'elmaslokitoh'
)


user2 = User(
    username = 'fe',
    password = 'elmaslokitoh',
    name = 'Ricky'
)

