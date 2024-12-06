from uuid import UUID

from loguru import logger
from omoide_client.api.exif import api_delete_exif_v1_exif_item_uuid_delete
from omoide_client.api.items import api_delete_item_v1_items_item_uuid_delete
from omoide_client.client import AuthenticatedClient

LOG = logger


class Cleaner:
    """Class that removes objects after tests."""

    def __init__(
        self,
        client: AuthenticatedClient,
        items: list[UUID] | None = None,
        exif: list[UUID] | None = None,
    ) -> None:
        """Initialize instance."""
        self.client = client
        self.items = items or []
        self.exif = exif or []

    @staticmethod
    def _add_uuid(uuid: str | UUID, given_list: list[UUID]) -> None:
        """Add UUID to given collection."""
        if isinstance(uuid, str):
            uuid = UUID(uuid)
        given_list.append(uuid)

    @staticmethod
    def _drop_uuid(uuid: str | UUID, given_list: list[UUID]) -> bool:
        """Remove UUID from the list, return True if deleted."""
        try:
            given_list.remove(uuid)
        except ValueError:
            return False
        return True

    def add_item(self, item_uuid: UUID | str) -> None:
        """Store reference."""
        self._add_uuid(item_uuid, self.items)

    def add_exif(self, item_uuid: UUID | str) -> None:
        """Store reference."""
        self._add_uuid(item_uuid, self.exif)

    def skip_item(self, item_uuid: UUID | str) -> None:
        """Remove reference."""
        self._drop_uuid(item_uuid, self.items)

    def skip_exif(self, item_uuid: UUID | str) -> None:
        """Remove reference."""
        self._drop_uuid(item_uuid, self.exif)

    def clean_all(self) -> None:
        """Remove all resources."""
        with self.client as client:
            self.clean_items(client)
            self.clean_exif(client)

    def clean_items(self, client: AuthenticatedClient) -> None:
        """Remove items."""
        for item_uuid in self.items:
            response = api_delete_item_v1_items_item_uuid_delete.sync(item_uuid, client=client)
            if response is not None:
                LOG.info('Cleaned item {}', item_uuid)

    def clean_exif(self, client: AuthenticatedClient) -> None:
        """Remove EXIF."""
        for item_uuid in self.exif:
            response = api_delete_exif_v1_exif_item_uuid_delete.sync(item_uuid, client=client)
            if response is not None:
                LOG.info('Cleaned EXIF for item {}', item_uuid)
