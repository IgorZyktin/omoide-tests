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
