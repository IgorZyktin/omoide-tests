from uuid import UUID

from omoide_client.api.exif import api_create_exif_v1_exif_item_uuid_post
from omoide_client.api.exif import api_delete_exif_v1_exif_item_uuid_delete
from omoide_client.api.exif import api_read_exif_v1_exif_item_uuid_get
from omoide_client.api.exif import api_update_exif_v1_exif_item_uuid_put
from omoide_client.api.items import api_create_item_v1_items_post
from omoide_client.api.items import api_delete_item_v1_items_item_uuid_delete
from omoide_client.api.users import api_get_all_users_v1_users_get
from omoide_client.models import EXIFModel
from omoide_client.models import EXIFModelExif
from omoide_client.models import ItemInput


def test_exif_crud(client_and_user_1, cleaner):
    """Test full lifecycle of EXIF records."""
    # arrange
    client, user = client_and_user_1

    # 1. Get user extras
    users_response = api_get_all_users_v1_users_get.sync(client=client).to_dict()
    assert len(users_response['users']) == 1
    user_response = users_response['users'][0]

    # 2. Create item
    item_body = ItemInput(
        parent_uuid=UUID(user_response['extras']['root_item_uuid']),
        name='item-for-exif-test',
    )
    item_response = api_create_item_v1_items_post.sync(client=client, body=item_body)
    item_uuid = item_response.item.uuid
    cleaner.add_item(item_uuid)

    # 3. Verify that item has no EXIF
    exif_response_1 = api_read_exif_v1_exif_item_uuid_get.sync(item_uuid, client=client)
    assert exif_response_1 is None

    # 4. Create EXIF
    cleaner.add_exif(item_uuid)
    exif_1 = {
        'hello': 'world',
        'also': {
            'hello': {
                'world': 1,
            }
        },
    }
    body_1 = EXIFModel(exif=EXIFModelExif.from_dict(exif_1))
    exif_response_2 = api_create_exif_v1_exif_item_uuid_post.sync(
        item_uuid, client=client, body=body_1
    )
    assert exif_response_2['result'] == 'created exif'
    assert exif_response_2['item_uuid'] == str(item_uuid)

    # 5. Verify that item has EXIF
    exif_response_3 = api_read_exif_v1_exif_item_uuid_get.sync(item_uuid, client=client)
    assert exif_response_3 is not None
    assert exif_response_3.exif.to_dict() == exif_1

    # 6. Update EXIF
    exif_2 = {
        'why': {
            'not': {
                'I should': 'change it',
            }
        }
    }
    body_2 = EXIFModel(exif=EXIFModelExif.from_dict(exif_2))
    exif_response_4 = api_update_exif_v1_exif_item_uuid_put.sync(
        item_uuid, client=client, body=body_2
    )
    assert exif_response_4 is not None
    assert exif_response_4['result'] == 'updated exif'
    assert exif_response_4['item_uuid'] == str(item_uuid)

    # 7. Verify that EXIF has changed
    exif_response_5 = api_read_exif_v1_exif_item_uuid_get.sync(item_uuid, client=client)
    assert exif_response_5 is not None
    assert exif_response_5.exif.to_dict() != exif_1
    assert exif_response_5.exif.to_dict() == exif_2

    # 8. Delete EXIF
    exif_response_6 = api_delete_exif_v1_exif_item_uuid_delete.sync(item_uuid, client=client)
    assert exif_response_6 is not None
    assert exif_response_6['result'] == 'deleted exif'

    # 9. Verify that item has no EXIF
    exif_response_7 = api_read_exif_v1_exif_item_uuid_get.sync(item_uuid, client=client)
    assert exif_response_7 is None

    # 10. Cleanup
    cleaner.skip_item(item_uuid)
    cleaner.skip_exif(item_uuid)
    delete_response = api_delete_item_v1_items_item_uuid_delete.sync(item_uuid, client=client)
    assert delete_response is not None
