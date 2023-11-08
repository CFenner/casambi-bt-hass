from CasambiBt import Unit as CasambiUnit, UnitControlType

from homeassistant.components.light import (
    COLOR_MODE_BRIGHTNESS,
    COLOR_MODE_ONOFF,
    COLOR_MODE_RGB,
    COLOR_MODE_RGBW,
    COLOR_MODE_COLOR_TEMP,
    COLOR_MODE_UNKNOWN,
    ColorMode,
)


def capabilities_helper(unit: CasambiUnit) -> set[str]:
    supported: set[str] = set()
    unit_modes = [uc.type for uc in unit.unitType.controls]

    if UnitControlType.RGB in unit_modes and UnitControlType.WHITE in unit_modes:
        supported.add(COLOR_MODE_RGBW)
    elif UnitControlType.RGB in unit_modes:
        supported.add(COLOR_MODE_RGB)

    if UnitControlType.DIMMER in unit_modes:
        supported.add(COLOR_MODE_BRIGHTNESS)
        supported.add(COLOR_MODE_ONOFF)
    elif UnitControlType.ONOFF in unit_modes:
        supported.add(COLOR_MODE_ONOFF)

    if UnitControlType.TEMPERATURE in unit_modes:
        supported.add(COLOR_MODE_COLOR_TEMP)

    if len(supported) == 0:
        supported.add(COLOR_MODE_UNKNOWN)

    return supported


def mode_helper(modes: set[ColorMode] | set[str] | None) -> str:
    if not modes:
        return COLOR_MODE_UNKNOWN

    if COLOR_MODE_RGBW in modes:
        return COLOR_MODE_RGBW
    elif COLOR_MODE_RGB in modes:
        return COLOR_MODE_RGB
    elif COLOR_MODE_COLOR_TEMP in modes:
        return COLOR_MODE_COLOR_TEMP
    elif COLOR_MODE_BRIGHTNESS in modes:
        return COLOR_MODE_BRIGHTNESS
    elif COLOR_MODE_ONOFF in modes:
        return COLOR_MODE_ONOFF
    else:
        return COLOR_MODE_UNKNOWN
