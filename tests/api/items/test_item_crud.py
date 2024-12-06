from uuid import UUID

from omoide_client.api.items import api_create_item_v1_items_post
from omoide_client.api.items import api_delete_item_v1_items_item_uuid_delete
from omoide_client.api.items import api_get_item_v1_items_item_uuid_get
from omoide_client.models import ItemInput


def test_item_delete_root_item(client_and_user_1, client_and_user_2, client_and_user_3):
    """Test that root item cannot be deleted."""
    # arrange
    for client, user in [client_and_user_1, client_and_user_2, client_and_user_3]:
        # 1. Verify that item exists
        item_response_1 = api_get_item_v1_items_item_uuid_get.sync(
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
        item_response_2 = api_get_item_v1_items_item_uuid_get.sync(
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
    cleaner.add_item(item_uuid)

    item = response.item
    assert UUID(str(item.uuid))
    assert item.parent_uuid == user.root_item_uuid
    assert response.item.owner_uuid == user.uuid
    assert item.status == 'created'
    # TODO - bug 206, item must have some number
    # assert item.number > 0
    assert item.name == 'item-for-item-creation-test'
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


def test_item_create_and_delete_parent(client_and_user_1, cleaner):
    """Test that item disappears when parent is deleted."""
    # arrange
    client, user = client_and_user_1

    # 1. Create parent
    item_body = ItemInput(
        parent_uuid=user.root_item_uuid,
        name='item-for-parent-deletion-test-parent',
    )
    item_response_1 = api_create_item_v1_items_post.sync(client=client, body=item_body)
    assert item_response_1 is not None
    parent = item_response_1.item
    parent_uuid = parent.uuid
    cleaner.add_item(parent_uuid)

    assert parent.parent_uuid == user.root_item_uuid
    assert parent.name == 'item-for-parent-deletion-test-parent'

    # 2. Create child
    item_body = ItemInput(
        parent_uuid=parent.uuid,
        name='item-for-parent-deletion-test-child',
    )
    item_response_2 = api_create_item_v1_items_post.sync(client=client, body=item_body)
    assert item_response_2 is not None
    child = item_response_2.item
    child_uuid = child.uuid
    cleaner.add_item(child_uuid)

    assert child.parent_uuid == parent.uuid
    assert child.name == 'item-for-parent-deletion-test-child'

    # 3. Delete parent
    delete_response_1 = api_delete_item_v1_items_item_uuid_delete.sync(parent_uuid, client=client)
    assert delete_response_1 is not None

    # 4. Verify that child is also absent
    item_response_3 = api_get_item_v1_items_item_uuid_get.sync(
        item_uuid=child_uuid,
        client=client,
    )
    assert item_response_3 is None

    # 5. Cleanup
    cleaner.skip_item(parent_uuid)
    cleaner.skip_item(child_uuid)
