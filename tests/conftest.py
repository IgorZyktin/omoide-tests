import os
from pathlib import Path
from uuid import UUID

import cfg
from httpx import BasicAuth
from omoide_client import AuthenticatedClient
from omoide_client import Client
from omoide_client.api.info import api_get_myself_v1_info_whoami_get
import pytest


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


def _init_user(config: cfg.Config, user: cfg.User) -> cfg.User:
    client = AuthenticatedClient(
        base_url=config.api_url,
        httpx_args={
            'auth': BasicAuth(username=user.login, password=user.password),
        },
        token='',
    )
    with client as client:
        response = api_get_myself_v1_info_whoami_get.sync(client=client).to_dict()

    user.uuid = UUID(response['uuid'])
    return user


@pytest.fixture
def client(config):
    return Client(base_url=config.api_url)


@pytest.fixture(scope='session')
def raw_admin_1(config):
    return config.admins[0]


@pytest.fixture(scope='session')
def raw_admin_2(config):
    return config.admins[1]


@pytest.fixture(scope='session')
def raw_user_1(config):
    return config.users[0]


@pytest.fixture(scope='session')
def raw_user_2(config):
    return config.users[1]


@pytest.fixture(scope='session')
def raw_user_3(config):
    return config.users[2]


@pytest.fixture(scope='session')
def admin_1(config):
    user = config.admins[0]
    return _init_user(config, user)


@pytest.fixture(scope='session')
def admin_2(config):
    user = config.admins[1]
    return _init_user(config, user)


@pytest.fixture(scope='session')
def user_1(config):
    user = config.users[0]
    return _init_user(config, user)


@pytest.fixture(scope='session')
def user_2(config):
    user = config.users[1]
    return _init_user(config, user)


@pytest.fixture(scope='session')
def user_3(config):
    user = config.users[2]
    return _init_user(config, user)
