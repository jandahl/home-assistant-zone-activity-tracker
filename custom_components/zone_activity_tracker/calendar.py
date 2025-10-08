"""Calendar platform for Zone Activity Tracker."""
from __future__ import annotations

from homeassistant.components.local_calendar import LocalCalendarEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the calendar platform."""
    async_add_entities([ZoneActivityCalendar(hass, entry)])


class ZoneActivityCalendar(LocalCalendarEntity):
    """Representation of a Zone Activity calendar."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the calendar."""
        super().__init__(hass, f"zone_activity_log_{entry.data['person_entity'].split('.')[1]}_{entry.data['zone_entity'].split('.')[1]}.ics")
        self.entry = entry
        self._attr_unique_id = f"zone_activity_log_{entry.data['person_entity'].split('.')[1]}_{entry.data['zone_entity'].split('.')[1]}"
        self._attr_name = f"Zone Activity Log: {entry.data['person_entity'].split('.')[1].replace("_", " ").title()} in {entry.data['zone_entity'].split('.')[1].replace("_", " ").title()}"
