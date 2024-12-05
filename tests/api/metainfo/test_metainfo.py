from omoide_client.api.items import api_create_item_v1_items_post
from omoide_client.api.items import api_delete_item_v1_items_item_uuid_delete
from omoide_client.api.metainfo import api_read_metainfo_v1_metainfo_item_uuid_get
from omoide_client.models import ItemInput


def test_metainfo_update(client_and_user_2, cleaner):
    """Test full lifecycle of metainfo records."""
    # arrange
    client, user = client_and_user_2

    # 1. Create item
    item_body = ItemInput(
        parent_uuid=user.root_item_uuid,
        name='item-for-metainfo-test',
    )
    item_response = api_create_item_v1_items_post.sync(client=client, body=item_body)
    item_uuid = item_response.item.uuid
    cleaner.add_item(item_uuid)

    # 2. Verify that item has metainfo
    meta_response_1 = api_read_metainfo_v1_metainfo_item_uuid_get.sync(item_uuid, client=client)

    assert meta_response_1 is not None
    assert meta_response_1.created_at is not None
    assert meta_response_1.updated_at is not None
    assert meta_response_1.deleted_at is None
    assert meta_response_1.user_time is None

    assert meta_response_1.content_type is None

    assert meta_response_1.content_size is None
    assert meta_response_1.content_width is None
    assert meta_response_1.content_height is None

    assert meta_response_1.preview_size is None
    assert meta_response_1.preview_width is None
    assert meta_response_1.preview_height is None

    assert meta_response_1.thumbnail_size is None
    assert meta_response_1.thumbnail_width is None
    assert meta_response_1.thumbnail_height is None

    # 3. Delete item
    delete_response = api_delete_item_v1_items_item_uuid_delete.sync(item_uuid, client=client)
    assert delete_response is not None
    cleaner.skip_item(item_uuid)

    # 4. Verify that item has no metainfo
    meta_response_2 = api_read_metainfo_v1_metainfo_item_uuid_get.sync(item_uuid, client=client)
    assert meta_response_2 is None
