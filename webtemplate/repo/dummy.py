
from typing import Optional
from webtemplate.repo.base import AbstractRepository, ConnectionAPI


class DummyRepository(AbstractRepository):

    def __init__(self, repository_url: dict, reason: Optional[str] = None):
        super().__init__(repository_url)
        self._reason = reason

    def can_connect(self) -> bool:
        return True

    def initialize(self) -> bool:
        return True

    def create(self) -> ConnectionAPI:
        return ConnectionAPI()