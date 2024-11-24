import os
from pathlib import Path

import pytest
from omoide_client import Client

import cfg


@pytest.fixture(scope='session')
def config() -> cfg.Config:
    url_env_var = 'OMOIDE_TESTS__API_URL'
    api_url = os.environ.get(url_env_var, 'http://127.0.0.1:8080/api')

    if api_url is None:
        msg = f'You have to set environment variable {url_env_var}'
        raise RuntimeError(msg)

    cred_env_var = 'OMOIDE_TEST__CREDENTIALS_PATH'
    cred_path_str = os.environ.get(cred_env_var, './omoide_tests_credentials.toml')

    if cred_path_str is None:
        msg = f'You have to set environment variable {cred_env_var}'
        raise RuntimeError(msg)

    cred_path = Path(cred_path_str)

    if not cred_path.exists():
        msg = f'Credentials file "{cred_path.absolute()}" does not exist'
        raise RuntimeError(msg)

    return cfg.get_config(api_url, cred_path)


@pytest.fixture
def client(config):
    return Client(base_url=config.api_url)
