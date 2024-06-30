from pydantic import BaseModel

class Users(BaseModel):
    peer_id: int
    name: str
    surname: str
    last_name: str
    rule: int

class Rules(BaseModel):
    id_rule: int
    name: str
    functional: str

class Groups(BaseModel):
    peer_ids: int
    group_number: str
    route: int
    course: int

class Routes(BaseModel):
    id_route: int
    name: str