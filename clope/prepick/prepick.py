"""
Client for Cantaloupe's Prepick SOAP interface.

The SOAP operations and their payloads are defined by the bundled WSDL
(SERVICE.SVC.xml), which is a downloaded copy of the demo endpoint's
?singleWsdl output. It is kept alongside this module so the client can be
built without contacting the endpoint at construction time.
"""

import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from zeep import AsyncClient
from zeep.wsse import UsernameToken

logger = logging.getLogger(__name__)

# Note: demo URL, change to production URL when ready.
WSDL_URL = (
    "https://qacore.mycantaloupe.com/SYNCPREPICKAUTOMATION.DEMO/SERVICE.SVC?singleWsdl"
)
WSDL_PATH = Path(__file__).with_name("SERVICE.SVC.xml")


@dataclass
class PrepickCoilUpdate:
    """
    A single coil quantity update for the UpdatePrepick operation.

    :param schedule_id: The schedule identifier for the pick.
    :type schedule_id: int
    :param machine_id: The machine identifier.
    :type machine_id: int
    :param item_id: The item identifier.
    :type item_id: int
    :param prepick_quantity: The quantity to prepick.
    :type prepick_quantity: int
    :param coil_name: Optional coil name (e.g. "A1").
    :type coil_name: str, optional
    """

    schedule_id: int
    machine_id: int
    item_id: int
    prepick_quantity: int
    coil_name: str | None = None

    def to_soap(self) -> dict:
        """
        Serialize the update into the shape expected by the WSDL.

        :return: Dict keyed by the WSDL element names.
        :rtype: dict
        """
        payload = {
            "ScheduleId": self.schedule_id,
            "MachineId": self.machine_id,
            "ItemId": self.item_id,
            "PrepickQuantity": self.prepick_quantity,
        }
        if self.coil_name is not None:
            payload["CoilName"] = self.coil_name
        return payload


@dataclass
class WarehouseTransactionPack:
    """
    A pack and quantity for a warehouse transfer transaction.

    :param pack_id: The pack identifier.
    :type pack_id: int
    :param quantity: The quantity to transfer.
    :type quantity: int
    """

    pack_id: int
    quantity: int

    def to_soap(self) -> dict:
        """
        Serialize the pack into the shape expected by the WSDL.

        :return: Dict keyed by the WSDL element names.
        :rtype: dict
        """
        return {"PackId": self.pack_id, "Quantity": self.quantity}


class PrepickClient:
    """
    Client for interacting with the SOAP interface for prepick operations.
    """

    def __init__(
        self,
        wsdl: str | Path | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """
        Create a PrepickClient.

        Credentials default to the PREPICK_USERNAME and
        PREPICK_PASSWORD environment variables and can be overridden with
        the username / password arguments.

        :param wsdl: WSDL URL or local path. When omitted (or a URL is given
            and cannot be loaded), the client falls back to the bundled
            SERVICE.SVC.xml.
        :type wsdl: str | pathlib.Path, optional
        :param username: SOAP username.
        :type username: str, optional
        :param password: SOAP password.
        :type password: str, optional
        :raises OSError: If no username/password can be resolved.
        """
        username = username or os.environ.get("PREPICK_USERNAME")
        password = password or os.environ.get("PREPICK_PASSWORD")
        if not username or not password:
            raise OSError(
                "PREPICK_USERNAME and PREPICK_PASSWORD environment variables "
                "must be set, or username/password must be provided"
            )

        self.client = self._build_client(wsdl, UsernameToken(username, password))

    def _build_client(
        self, wsdl: str | Path | None, wsse: UsernameToken
    ) -> AsyncClient:
        """
        Build the zeep client, falling back to the bundled WSDL on failure.

        :param wsdl: WSDL URL or local path.
        :type wsdl: str | pathlib.Path, optional
        :param wsse: WSSE username token used to sign requests.
        :type wsse: zeep.wsse.UsernameToken
        :return: The configured zeep async client.
        :rtype: zeep.AsyncClient
        """
        if wsdl is not None and not str(wsdl).startswith(("http://", "https://")):
            return AsyncClient(wsdl=str(wsdl), wsse=wsse)

        source = str(wsdl) if wsdl is not None else WSDL_URL
        try:
            return AsyncClient(wsdl=source, wsse=wsse)
        except Exception as exc:
            logger.warning(
                "Could not load WSDL from %s: %s. Using bundled WSDL instead.",
                source,
                exc,
            )
            return AsyncClient(wsdl=str(WSDL_PATH), wsse=wsse)

    async def load_routes(self) -> list[Any]:
        """
        Return the list of routes.

        :return: List of Route objects.
        :rtype: list
        """
        return await self.client.service.LoadRoutes()

    async def load_items(self) -> list[Any]:
        """
        Return the list of items and their packs.

        Each item has the following fields:
        - Id: the Seed internal ID for the item.
        - ItemCategoryId: the Seed internal ID for the item's category. Use
          load_item_categories to look up the category name.
        - Name: the item name.
        - ProductCode: the operator-entered reference code shown in Seed.
          Labeled "UPC" in Seed but not typically a barcode.
        - Size: a user-populated field.
        - Packs: a list of pack objects, each with:

            - Barcodes: barcodes for this item in this pack type.
            - Id: the Seed internal ID for the item-pack (referenced in
              LoadPrepick data).
            - ItemsCount: the number of eaches in the pack. Cantaloupe's
              docs refer to this as "ItemCount".
            - Name: the pack name ("Each", "Box", "Case", etc).

        :return: List of Item objects.
        :rtype: list
        """
        return await self.client.service.LoadItems()

    async def load_item_categories(self) -> list[Any]:
        """
        Return the list of item categories.

        :return: List of ItemCategory objects.
        :rtype: list
        """
        return await self.client.service.LoadItemCategories()

    async def load_machine_classes(self) -> list[Any]:
        """
        Return the list of machine classes.

        :return: List of MachineClass objects.
        :rtype: list
        """
        return await self.client.service.LoadMachineClasses()

    async def load_warehouses(self) -> list[Any]:
        """
        Return the list of warehouses.

        :return: List of Warehouse objects.
        :rtype: list
        """
        return await self.client.service.LoadWarehouses()

    async def load_prepick(
        self, schedule_date: datetime, route_id: int | None = None
    ) -> list[Any]:
        """
        Return the prepick orders for a schedule date and optional route.

        Each result is a prepick machine entry with the following fields:
        - AssetId: manually populated asset identifier (not the internal
          primary ID).
        - Coils: list of coil entries; each PackId identifies the
          product to pick and Quantity is the amount required.
        - CustomerName: the customer the asset is associated with.
        - LocationName: the location the asset is associated with.
        - Place: where the asset is found at the location (e.g. Kitchen,
          Breakroom).
        - MachineClassId: machine type lookup distinguishing assets that
          are picked differently (e.g. snack vs beverage vs delivery point).
        - ScheduleId: the route this asset is scheduled for.

        :param schedule_date: The schedule date to load prepick orders for.
        :type schedule_date: datetime
        :param route_id: Optional route identifier to restrict the result.
        :type route_id: int, optional
        :return: List of PrepickMachine objects.
        :rtype: list
        """
        return await self.client.service.LoadPrepick(
            scheduleDate=schedule_date,
            routeId=route_id,
        )

    async def load_picked_machines(self, schedule_date: datetime) -> list[Any]:
        """
        Return the machines already picked for a schedule date.

        :param schedule_date: The schedule date to load.
        :type schedule_date: datetime
        :return: List of Machine objects.
        :rtype: list
        """
        return await self.client.service.LoadAlreadyPickedMachines(
            scheduleDate=schedule_date,
        )

    async def update_prepick(self, coil_updates: list[PrepickCoilUpdate]) -> None:
        """
        Used to update Seed with details of actual pick quantities.

        :param coil_updates: The coil updates to send.
        :type coil_updates: list[PrepickCoilUpdate]
        """
        payload = [update.to_soap() for update in coil_updates]
        await self.client.service.UpdatePrepick(prepickCoilUpdates=payload)

    async def finish_prepick_update(self, schedule_id: int) -> None:
        """
        Indicates that all picks are complete for the specified route.

        :param schedule_id: The schedule identifier to finish.
        :type schedule_id: int
        """
        await self.client.service.FinishPrepickUpdate(scheduleId=schedule_id)

    async def create_warehouse_transfer_transaction(
        self,
        from_warehouse_id: int,
        to_warehouse_id: int,
        packs: list[WarehouseTransactionPack],
    ) -> None:
        """
        Used to create a warehouse-to-warehouse product move transaction in Seed.

        :param from_warehouse_id: The source warehouse identifier.
        :type from_warehouse_id: int
        :param to_warehouse_id: The destination warehouse identifier.
        :type to_warehouse_id: int
        :param packs: The packs and quantities to transfer.
        :type packs: list[WarehouseTransactionPack]
        """
        payload = [pack.to_soap() for pack in packs]
        await self.client.service.CreateWarehouseTransferTransaction(
            fromWarehouseId=from_warehouse_id,
            toWarehouseId=to_warehouse_id,
            packs=payload,
        )
