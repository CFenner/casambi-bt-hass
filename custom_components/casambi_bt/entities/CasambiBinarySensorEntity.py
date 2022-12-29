import logging

from homeassistant.components.binary_sensor import BinarySensorEntity

from CasambiBt import Unit

from .CasambiEntity import CasambiEntity
from .. import DOMAIN, CasambiApi

_LOGGER = logging.getLogger(__name__)


class CasambiBinarySensorEntity(BinarySensorEntity, CasambiEntity):
    def __init__(self, unit: Unit, api: CasambiApi, name: str = None, device_class = None, icon = None):
        _LOGGER.debug(f"Casambi {name} - init - start")

        BinarySensorEntity.__init__(self)
        CasambiEntity.__init__(self, unit, api, name)
        self._attr_is_on = False
        self._attr_device_class = device_class
        self._attr_icon = icon

        _LOGGER.debug(f"Casambi {name} - init - end")
