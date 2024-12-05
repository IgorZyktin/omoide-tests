from uuid import UUID

from omoide_client.api.items import api_create_item_v1_items_post
from omoide_client.api.items import api_delete_item_v1_items_item_uuid_delete
from omoide_client.api.items import api_read_item_v1_items_item_uuid_get
from omoide_client.models import ItemInput


def test_item_delete_root_item(client_and_user_1, client_and_user_2, client_and_user_3):
    """Test that root item cannot be deleted."""
    # arrange
    for client, user in [client_and_user_1, client_and_user_2, client_and_user_3]:
        # 1. Verify that item exists
        item_response_1 = api_read_item_v1_items_item_uuid_get.sync(
            item_uuid=user.root_item_uuid,
            client=client,
        )
        assert item_response_1.item.uuid == user.root_item_uuid

        # 2. Try to delete it
        delete_response = api_delete_item_v1_items_item_uuid_delete.sync(
            item_uuid=user.root_item_uuid,
            client=client,
        )
        assert delete_response is None

        # 3. Verify that item still exists
        item_response_2 = api_read_item_v1_items_item_uuid_get.sync(
            item_uuid=user.root_item_uuid,
            client=client,
        )
        assert item_response_2.item.uuid == user.root_item_uuid


def test_item_create(client_and_user_1, cleaner):
    """Test item creation."""
    # arrange
    client, user = client_and_user_1

    # 1. Create item
    item_body = ItemInput(
        parent_uuid=user.root_item_uuid,
        name='item-for-item-creation-test',
    )
    response = api_create_item_v1_items_post.sync(client=client, body=item_body)
    assert response is not None
    item_uuid = response.item.uuid

    item = response.item
    assert UUID(str(item.uuid))
    assert item.parent_uuid == user.root_item_uuid
    assert response.item.owner_uuid == user.uuid
    assert item.status == 'created'
    # TODO - bug 206, item must have some number
    # assert item.number > 0
    assert not item.is_collection
    assert item.content_ext is None
    assert item.preview_ext is None
    assert item.thumbnail_ext is None
    assert len(item.tags) == 0
    assert len(item.permissions) == 0
    assert item.extras.to_dict() == {}

    # 2. Delete item
    delete_response = api_delete_item_v1_items_item_uuid_delete.sync(item_uuid, client=client)
    assert delete_response is not None
    cleaner.skip_item(item_uuid)
