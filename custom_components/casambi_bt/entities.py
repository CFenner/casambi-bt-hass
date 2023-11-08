import logging

from typing import Final

from homeassistant.core import callback
from homeassistant.helpers import device_registry
from homeassistant.helpers.entity import DeviceInfo, Entity, EntityDescription

from CasambiBt import Group as CasambiGroup, Unit as CasambiUnit, Scene as CasambiScene

from . import DOMAIN, CasambiApi

_LOGGER: Final = logging.getLogger(__name__)


class CasambiEntity(Entity):
    """Defines a Casambi Entity."""

    entity_description: EntityDescription
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, api: CasambiApi, object: CasambiUnit | CasambiScene | None, description: EntityDescription):
        """Initialize Casambi Entity."""
        self.entity_description = description
        self._api = api
        self._obj = object
        self._attr_name = description.name

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this entity."""
        name = f"{self._api.casa.networkId}"
        if self._obj is not None:
            if isinstance(self._obj, CasambiUnit):
                name += f"-unit-{self._obj.uuid}"
            elif isinstance(self._obj, CasambiGroup):
                name += f"-group-{self._obj.groudId}"
            elif isinstance(self._obj, CasambiScene):
                name += f"-scene-{self._obj.sceneId}"
        if hasattr(self, "_attr_name"):
            name += f"-{self._attr_name}"
        return name.lower()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this Casambi entity."""
        if self._obj is not None and isinstance(self._obj, CasambiUnit):
            # return device info for unit
            return DeviceInfo(
                name=self._obj.name,
                manufacturer=self._obj.unitType.manufacturer,
                model=self._obj.unitType.model,
                sw_version=self._obj.firmwareVersion,
                identifiers={(DOMAIN, self._obj.uuid)},
                via_device=(DOMAIN, self._api.casa.networkId),
            )
        # return device info for network, scene, group
        return DeviceInfo(
            name=self._api.casa.networkName,
            manufacturer="Casambi",
            identifiers={(DOMAIN, self._api.casa.networkId)},
            connections={(device_registry.CONNECTION_BLUETOOTH, self._api.address)}
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._api.available

    @callback
    def change_callback(self, _unit: CasambiUnit) -> None:
        self.schedule_update_ha_state(False)
