"""The Zone Activity Tracker integration."""
import logging
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["binary_sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Zone Activity Tracker from a config entry."""
    _LOGGER.info("Setting up Zone Activity Tracker from a config entry.")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Zone Activity Tracker.")
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
