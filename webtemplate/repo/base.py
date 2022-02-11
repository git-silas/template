
class ConnectionAPI:

    def close(self) -> None:
        raise NotImplementedError("Connection.close")


class AbstractRepository:
    
    def __init__(self, repository_url: dict):
        self.repo_url = repository_url
    
    @property
    def url(self) -> dict:
        return self.repo_url

    def can_connect(self) -> bool:
        raise NotImplementedError("Repository.can_connect.")

    def initialize(self) -> bool:
        raise NotImplementedError("Repository.initialize.")

    def create(self) -> ConnectionAPI:
        raise NotImplementedError("Repository.create")


