import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    api_url: str
    cred_path: Path


def get_config(api_url: str, cred_path: Path) -> Config:
    """Create Config instance."""
    path = Path(cred_path)

    with open(path, mode='rb') as file:
        data = tomllib.load(file)

        print(data)

    return Config(
        api_url=api_url,
        cred_path=cred_path,
    )
