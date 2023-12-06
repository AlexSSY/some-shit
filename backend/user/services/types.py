from typing import TypedDict


Email = str


class UserDict(TypedDict):
    id: int
    email: Email
    first_name: str
    last_name: str
    is_active: bool
