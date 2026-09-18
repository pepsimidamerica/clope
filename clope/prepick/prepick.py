"""
Modules containing prepick data processing functions.

https://qacore.mycantaloupe.com/SyncPrepickAutomation.Demo/Service.svc
"""

from zeep import AsyncClient

# Note: demo URL, change to production URL
WSDL_URL = (
    "https://qacore.mycantaloupe.com/SYNCPREPICKAUTOMATION.DEMO/SERVICE.SVC?singleWsdl"
)


class PrepickClient:
    """
    Client for interacting with the SOAP interface for prepick operations.
    """

    def __init__(self, wsdl_url: str = WSDL_URL):
        self.client = AsyncClient(wsdl=wsdl_url)

    async def load_items(self):
        """
        Returns list of items and packs.
        """
        items = await self.client.service.LoadItems()
        return items

    async def load_item_categories(self):
        """
        Returns list of item categories.
        """
        categories = await self.client.service.LoadItemCategories()
        return categories

    async def load_picked_machines(self):
        """
        Returns list of picks that have already been picked for that date.
        """
        machines = await self.client.service.LoadAlreadyPickedMchines()
        return machines

    async def load_machine_classes(self):
        """
        Returns list of machine classes.
        """
        classes = await self.client.service.LoadMachineClasses()
        return classes

    async def load_prepick(self):
        """
        Returns list of prepicks by item pack for each machine/delivery point for the specified date and route (optional).
        """
        prepick = await self.client.service.LoadPrepick()
        return prepick

    async def load_routes(self):
        """
        Returns list of routes.
        """
        routes = await self.client.service.LoadRoutes()
        return routes

    async def load_warehouses(self):
        """
        Returns list of warehouses.
        """
        warehouses = await self.client.service.LoadWarehouses()
        return warehouses


# TODO Soap Actions
# CreateWarehouseTransferTransaction
# FinishPrepickUpdate
# UpdatePrepick
