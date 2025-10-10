"""Binary sensor platform for Zone Activity Tracker."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event, async_track_time_change
from homeassistant.util import dt as dt_util

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    async_add_entities([ZoneActivityBinarySensor(hass, entry)])


class ZoneActivityBinarySensor(BinarySensorEntity):
    """Representation of a Zone Activity binary sensor."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the binary sensor."""
        self.hass = hass
        self.entry = entry
        self._attr_is_on = False
        self._attr_unique_id = f"zone_activity_tracker_{entry.data['person_entity'].split('.')[1]}_{entry.data['zone_entity'].split('.')[1]}"
        self._attr_name = f"Zone Activity: {entry.data['person_entity'].split('.')[1].replace("_", " ").title()} in {entry.data['zone_entity'].split('.')[1].replace("_", " ").title()}"
        self._minutes_in_zone = entry.data["minutes_in_zone"]
        self._timer_task = None

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        person_entity = self.entry.data["person_entity"]
        zone_entity = self.entry.data["zone_entity"]
        calendar_entity = self.entry.data["calendar_entity"]
        reset_time_str = self.entry.data["reset_time"]
        reset_time = dt_util.parse_time(reset_time_str)

        zone_friendly_name = self.hass.states.get(zone_entity).name

        @callback
        def state_change_listener(event: Event) -> None:
            """Handle person state changes."""
            new_state = event.data.get("new_state")
            if new_state and new_state.state == zone_friendly_name:
                self._attr_is_on = True
                self.async_write_ha_state()

        @callback
        def time_change_listener(now) -> None:
            """Handle daily reset."""
            if self.is_on:
                yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')
                today = now.strftime('%Y-%m-%d')

                self.hass.async_create_task(
                    self.hass.services.async_call(
                        "calendar",
                        "create_event",
                        {
                            "entity_id": calendar_entity,
                            "summary": f"{self._attr_name}",
                            "start_date": yesterday,
                            "end_date": today,
                        },
                    )
                )

            self._attr_is_on = False
            self.async_write_ha_state()

        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [person_entity], state_change_listener
            )
        )
        self.async_on_remove(
            async_track_time_change(
                self.hass, time_change_listener, hour=reset_time.hour, minute=reset_time.minute, second=reset_time.second
            )
        )
