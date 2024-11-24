import os
from dataclasses import dataclass

import pytest
from omoide_client import Client


@dataclass
class Config:
    api_url: str


@pytest.fixture(scope='session')
def config() -> Config:
    env_var = 'OMOIDE_TESTS__API_URL'
    api_url = os.environ.get(env_var, 'http://127.0.0.1:8080/api')

    if api_url is None:
        msg = f'You have to set environment variable {env_var}'
        raise RuntimeError(msg)

    return Config(api_url=api_url)


@pytest.fixture
def client(config):
    return Client(base_url=config.api_url)
