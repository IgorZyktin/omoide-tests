from httpx import BasicAuth
from omoide_client import AuthenticatedClient
from omoide_client.api.info import api_get_myself_v1_info_whoami_get
from omoide_client.api.info import api_get_version_v1_info_version_get


def test_info_version(client):
    # act
    with client as client:
        response = api_get_version_v1_info_version_get.sync(client=client).to_dict()

    # assert
    assert 'version' in response
    assert isinstance(response['version'], str)


def test_info_whoami_anon(client):
    # act
    with client as client:
        response = api_get_myself_v1_info_whoami_get.sync(client=client).to_dict()

    # assert
    assert response['name'] == 'anon'
    assert response['uuid'] is None


def test_info_whoami_known(config, raw_admin_1, raw_admin_2, raw_user_1, raw_user_2, raw_user_3):
    # act
    for user in [raw_admin_1, raw_admin_2, raw_user_1, raw_user_2, raw_user_3]:
        client = AuthenticatedClient(
            base_url=config.api_url,
            httpx_args={
                'auth': BasicAuth(username=user.login, password=user.password),
            },
            token='',
        )
        with client as client:
            response = api_get_myself_v1_info_whoami_get.sync(client=client).to_dict()

        # assert
        assert response['name'] == user.name
