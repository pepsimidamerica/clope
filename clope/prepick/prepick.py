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


# TODO Soap Actions

# CreateWarehouseTransferTransaction
# FinishPrepickUpdate
# LoadAlreadyPickedMchines
# LoadItemCategories
# LoadMachineClasses
# LoadPrepick
# LoadRoutes
# LoadWarehouses
# UpdatePrepick
