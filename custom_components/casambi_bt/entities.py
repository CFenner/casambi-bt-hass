import logging

from typing import Final

from homeassistant.core import callback
from homeassistant.helpers import device_registry
from homeassistant.helpers.entity import DeviceInfo, Entity, EntityDescription

from CasambiBt import Unit as CasambiUnit

from . import DOMAIN, CasambiApi

_LOGGER: Final = logging.getLogger(__name__)


class CasambiEntity(Entity):
    """Defines a Casambi Entity."""

    entity_description: EntityDescription
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, api: CasambiApi, unit: CasambiUnit | None, description: EntityDescription):
        """Initialize Casambi Entity."""
        self.entity_description = description
        self._api = api
        self._unit = unit
        self._attr_name = description.name

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this entity."""
        name = f"{self._api.casa.networkId}"
        if self._unit is not None:
            name += f"_{self._unit.uuid}"
        if hasattr(self, "_attr_name"):
            name += f"_{self._attr_name}"
        return name.lower()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this Casambi entity."""
        if self._unit is None:
            # return device info for network
            return DeviceInfo(
                name=self._api.casa.networkName,
                manufacturer="Casambi",
                identifiers={(DOMAIN, self._api.casa.networkId)},
                connections={(device_registry.CONNECTION_BLUETOOTH, self._api.address)}
            )
        # return device info for unit
        return DeviceInfo(
            name=self._unit.name,
            manufacturer=self._unit.unitType.manufacturer,
            model=self._unit.unitType.model,
            sw_version=self._unit.firmwareVersion,
            identifiers={(DOMAIN, self._unit.uuid)},
            via_device=(DOMAIN, self._api.casa.networkId),
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._api.available

    @callback
    def change_callback(self, _unit: CasambiUnit) -> None:
        self.schedule_update_ha_state(False)
