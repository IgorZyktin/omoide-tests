import tomllib
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID


@dataclass
class User:

    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password
        self._uuid = None

    def __str__(self) -> str:
        return f'User<{self.login}>'

    @property
    def uuid(self) -> UUID:
        if self._uuid is None:
            msg = f'User {self} is not yet initiated'
            raise RuntimeError(msg)
        return self._uuid

    @uuid.setter
    def uuid(self, uuid: str) -> None:
        if self._uuid is not None:
            msg = f'User {self} is already initiated'
            raise RuntimeError(msg)
        self._uuid = UUID(uuid)


@dataclass
class Config:
    api_url: str
    cred_path: Path
    admins: list[User]
    users: list[User]


def get_config(api_url: str, cred_path: Path) -> Config:
    """Create Config instance."""
    path = Path(cred_path)

    with open(path, mode='rb') as file:
        data = tomllib.load(file)

    return Config(
        api_url=api_url,
        cred_path=cred_path,
        admins=[User(**admin) for admin in data['admins']],
        users=[User(**user) for user in data['admins']],
    )
