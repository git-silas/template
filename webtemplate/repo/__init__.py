from typing import Dict, Type

from webtemplate.repo.base import AbstractRepository
from webtemplate.repo.postgres import PostgresRepository
from webtemplate.repo.dummy import DummyRepository


REPOSITORY_DIRECTORY: Dict[str, Type[AbstractRepository]] = {
    "postgres": PostgresRepository,
}


def create_repository(repo_url: dict) -> AbstractRepository:

    db_type = repo_url["type"]

    try:
        repository = REPOSITORY_DIRECTORY[db_type](repo_url)
    except KeyError:
        repository = DummyRepository(
            "dummy:", f"Unknown repository scheme '{db_type}'"
        )

    if not repository.can_connect():
        repository = DummyRepository(
            "dummy:", f"Cannot connect to {repository.url}"
        )

    if not repository.initialize():
        repository = DummyRepository(
            "dummy:", f"Cannot initialize repository {repository.url}"
        )

    return repository