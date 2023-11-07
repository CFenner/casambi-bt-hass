"""Constants for the Casambi Bluetooth integration."""

from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "casambi_bt"

CONF_IMPORT_GROUPS: Final = "import_groups"

IDENTIFIER_NETWORK_ID: Final = "network-id"
IDENTIFIER_UUID: Final = "uuid"

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.LIGHT, 
    Platform.SCENE, 
]