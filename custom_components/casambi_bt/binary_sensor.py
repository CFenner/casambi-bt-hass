"""Binary Sensor implementation for Casambi"""
import logging

from typing import Final

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass, BinarySensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_OFF, STATE_ON, EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from CasambiBt import Unit as CasambiUnit, UnitControlType

from . import DOMAIN, CasambiApi
from .entities import CasambiEntity

CASA_LIGHT_CTRL_TYPES: Final[list[UnitControlType]] = [
    UnitControlType.DIMMER,
    UnitControlType.RGB,
    UnitControlType.WHITE,
]

_LOGGER = logging.getLogger(__name__)

NETWORK_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="status",
        name="Status",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)

UNIT_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="status",
        name="Status",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Support unloading of entry
    """
    return True

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setting up binary sensor"""
    _LOGGER.debug(f"Setting up binary sensor entities. config_entry:{config_entry}")
    api: CasambiApi = hass.data[DOMAIN][config_entry.entry_id]
    binary_sensors = []

    # create network sensors
    for description in NETWORK_SENSORS:
        _LOGGER.debug("Adding CasambiBinarySensorEntity for network...")
        binary_sensors.append(CasambiBinarySensorEntity(api, None, description))

    # create unit sensors
    for unit in api.get_units(CASA_LIGHT_CTRL_TYPES):
        _LOGGER.debug("Adding CasambiBinarySensorEntity for units...")
        for description in UNIT_SENSORS:
            binary_sensors.append(CasambiBinarySensorEntity(api, unit, description))

    if binary_sensors:
        _LOGGER.debug("Adding binary sensor entities...")
        async_add_entities(binary_sensors)
    else:
        _LOGGER.debug("No binary sensor entities available.")

    return True


class CasambiBinarySensorEntity(BinarySensorEntity, CasambiEntity):
    """Defines a Casambi Binary Sensor Entity."""

    _attr_is_on = False
    entity_description: BinarySensorEntityDescription

    def __init__(self, api: CasambiApi, unit: CasambiUnit, description: BinarySensorEntityDescription):
        super().__init__(api, unit, description)
        self.entity_description = description

    @property
    def state(self):
        """Getter for state."""
        if self._obj is None:
            return STATE_ON if super().available else STATE_OFF
        return STATE_ON if super().available and self._obj.online else STATE_OFF

    @callback
    def change_callback(self, unit: CasambiUnit) -> None:
        _LOGGER.debug("Handling state change for unit %i", unit.deviceId)
        if hasattr(self, "_obj") and self._obj is not None:
            if unit.state:
                self._obj = unit
            else:
                self._obj.online = unit.online
        return super().change_callback(unit)

    async def async_added_to_hass(self) -> None:
        if self._obj is not None:
            self._api.register_unit_updates(self._obj, self.change_callback)

    async def async_will_remove_from_hass(self) -> None:
        if self._obj is not None:
            self._api.unregister_unit_updates(self._obj, self.change_callback)
