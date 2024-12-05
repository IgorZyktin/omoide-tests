from uuid import UUID

from omoide_client.api.items import api_create_item_v1_items_post
from omoide_client.api.items import api_delete_item_v1_items_item_uuid_delete
from omoide_client.api.users import api_get_all_users_v1_users_get
from omoide_client.models import ItemInput


def test_item_create(client_and_user_1, cleaner):
    """Test item creation."""
    # arrange
    client, user = client_and_user_1

    # 1. Get user extras
    users_response = api_get_all_users_v1_users_get.sync(client=client).to_dict()
    assert len(users_response['users']) == 1
    user_response = users_response['users'][0]

    # 2. Create item
    item_body = ItemInput(
        parent_uuid=UUID(user_response['extras']['root_item_uuid']),
        name='item-for-item-creation-test',
    )
    response = api_create_item_v1_items_post.sync(client=client, body=item_body)
    assert response is not None
    assert UUID(str(response.item.uuid))
    assert response.item.owner_uuid == user.uuid
    item_uuid = response.item.uuid

    # 3. Delete item
    delete_response = api_delete_item_v1_items_item_uuid_delete.sync(item_uuid, client=client)
    assert delete_response is not None
    cleaner.skip_item(item_uuid)
