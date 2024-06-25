from pydantic import BaseModel

class User(BaseModel):
    peer_id: int
    name: str
    surname: str
    last_name: str
    rule: int

class rules(BaseModel):
    id_rule: int
    name: str
    functional: str

class groups(BaseModel):
    peer_ids: int
    group_number: str
    route: int
    kurs: str

class routes(BaseModel):
    id_route: int
    name: str