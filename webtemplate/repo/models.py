from dataclasses import dataclass
from typing import Optional


@dataclass
class Model:
    pass


@dataclass
class User(Model):

    ident: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]