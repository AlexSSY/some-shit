from typing import TypedDict


Email = str


class User(TypedDict):
    id: int
    email: Email
    first_name: str
    last_name: str
    is_active: bool
