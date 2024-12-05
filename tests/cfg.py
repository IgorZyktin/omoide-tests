from dataclasses import dataclass
from pathlib import Path
import tomllib
from uuid import UUID


@dataclass
class User:
    """Simple DTO that represents user."""

    def __init__(self, login: str, password: str, name: str | None = None) -> None:
        """Initialize instance."""
        self.login = login
        self.password = password
        self.name = name
        self._uuid = None

    def __str__(self) -> str:
        """Return textual representation."""
        return f'User<{self.login}>'

    @property
    def uuid(self) -> UUID:
        """Return UUID of the user."""
        if self._uuid is None:
            msg = f'User {self} is not yet initiated'
            raise RuntimeError(msg)
        return self._uuid

    @uuid.setter
    def uuid(self, uuid: str) -> None:
        """Set UUID of the user."""
        if self._uuid is not None:
            msg = f'User {self} is already initiated'
            raise RuntimeError(msg)
        self._uuid = UUID(uuid)


@dataclass
class Config:
    """Config class that holds parameters for tests."""

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
        users=[User(**user) for user in data['users']],
    )
