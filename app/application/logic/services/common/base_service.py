from typing import Generic, TypeVar


TRepo = TypeVar('TRepo')

class BaseService(Generic[TRepo]):
    def __init__(self, repo: TRepo):
        self._repo = repo
