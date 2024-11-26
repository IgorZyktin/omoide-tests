from uuid import UUID

from omoide_client.api.items import api_create_item_v1_items_post
from omoide_client.api.users import api_get_all_users_v1_users_get
from omoide_client.models import ItemInput


def test_item_create(client_and_user_1, cleaner):
    # arrange
    client, user = client_and_user_1

    with client as client:
        # 1. Getting user extras
        users_response = api_get_all_users_v1_users_get.sync(client=client).to_dict()
        assert len(users_response['users']) == 1
        user_response = users_response['users'][0]

        # 2. Creating item
        item_body = ItemInput(
            parent_uuid=UUID(user_response['extras']['root_item_uuid']),
            name='item-for-item-creation-test',
        )
        response = api_create_item_v1_items_post.sync(client=client, body=item_body)
        assert response is not None
        assert UUID(str(response.item.uuid))
        assert response.item.owner_uuid == user.uuid
