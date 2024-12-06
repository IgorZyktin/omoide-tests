import os
from pathlib import Path

import cfg
import cleaner as cleaner_module
from httpx import BasicAuth
from omoide_client.api.info import api_get_myself_v1_info_whoami_get
from omoide_client.api.users import api_get_all_users_v1_users_get
from omoide_client.client import AuthenticatedClient
from omoide_client.client import Client
import pytest


@pytest.fixture(scope='session')
def config() -> cfg.Config:
    """Create and return config instance."""
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
    """Return user with UUID set and with authenticated client."""
    client = AuthenticatedClient(
        base_url=config.api_url,
        httpx_args={
            'auth': BasicAuth(username=user.login, password=user.password),
        },
        token='',
    )
    with client as client:
        me_response = api_get_myself_v1_info_whoami_get.sync(client=client).to_dict()
        user.uuid = me_response['uuid']

        users_response = api_get_all_users_v1_users_get.sync(client=client).to_dict()

        for each in users_response['users']:
            if each['uuid'] == str(user.uuid):
                user.root_item_uuid = each['extras']['root_item_uuid']
                return user

    msg = f'Failed to get all required infor for user {user}'
    raise RuntimeError(msg)


def _new_client(config: cfg.Config, user: cfg.User) -> tuple[AuthenticatedClient, cfg.User]:
    """Create and return authenticated client instance."""
    client = AuthenticatedClient(
        base_url=config.api_url,
        httpx_args={
            'auth': BasicAuth(username=user.login, password=user.password),
        },
        token='',
    )

    return client, user


@pytest.fixture
def api_client(config):
    """Create and return client instance."""
    return Client(base_url=config.api_url)


@pytest.fixture(scope='session')
def raw_admin_1(config):
    """Return raw admin 1."""
    return config.admins[0]


@pytest.fixture(scope='session')
def raw_admin_2(config):
    """Return raw admin 2."""
    return config.admins[1]


@pytest.fixture(scope='session')
def raw_user_1(config):
    """Return raw user 1."""
    return config.users[0]


@pytest.fixture(scope='session')
def raw_user_2(config):
    """Return raw user 2."""
    return config.users[1]


@pytest.fixture(scope='session')
def raw_user_3(config):
    """Return raw user 3."""
    return config.users[2]


@pytest.fixture(scope='session')
def admin_1(config):
    """Return admin 1."""
    user = config.admins[0]
    return _init_user(config, user)


@pytest.fixture(scope='session')
def admin_2(config):
    """Return admin 2."""
    user = config.admins[1]
    return _init_user(config, user)


@pytest.fixture(scope='session')
def user_1(config):
    """Return user 1."""
    user = config.users[0]
    return _init_user(config, user)


@pytest.fixture(scope='session')
def user_2(config):
    """Return user 2."""
    user = config.users[1]
    return _init_user(config, user)


@pytest.fixture(scope='session')
def user_3(config):
    """Return user 3."""
    user = config.users[2]
    return _init_user(config, user)


@pytest.fixture(scope='session')
def client_and_admin_1(config, admin_1):
    """Return client + admin 1."""
    return _new_client(config, admin_1)


@pytest.fixture(scope='session')
def client_and_admin_2(config, admin_2):
    """Return client + admin 2."""
    return _new_client(config, admin_2)


@pytest.fixture(scope='session')
def client_and_user_1(config, user_1):
    """Return client + user 1."""
    return _new_client(config, user_1)


@pytest.fixture(scope='session')
def client_and_user_2(config, user_2):
    """Return client + user 2."""
    return _new_client(config, user_2)


@pytest.fixture(scope='session')
def client_and_user_3(config, user_3):
    """Return client + user 3."""
    return _new_client(config, user_3)


@pytest.fixture(scope='session')
def cleaner(config, admin_1):
    """Remove all newly created resources."""
    _client = AuthenticatedClient(
        base_url=config.api_url,
        httpx_args={
            'auth': BasicAuth(username=admin_1.login, password=admin_1.password),
        },
        token='',
    )
    instance = cleaner_module.Cleaner(_client)
    yield instance
    instance.clean_all()
