"""Binary sensor platform for Zone Activity Tracker."""
import logging
from __future__ import annotations

from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event, async_track_time_change, async_call_later
from homeassistant.util import dt as dt_util

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


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
        _LOGGER.info("Initializing ZoneActivityBinarySensor")
        self.hass = hass
        self.entry = entry
        self._attr_is_on = False
        self._attr_unique_id = f"zone_activity_tracker_{entry.data['person_entity'].split('.')[1]}_{entry.data['zone_entity'].split('.')[1]}"
        self._attr_name = f"Zone Activity: {entry.data['person_entity'].split('.')[1].replace('_', ' ').title()} in {entry.data['zone_entity'].split('.')[1].replace('_', ' ').title()}"
        self._minutes_in_zone = entry.data["minutes_in_zone"]


        self._timer_task = None


        self.person_entity = self.entry.data["person_entity"]


        self.zone_entity = self.entry.data["zone_entity"]


        self.calendar_entity = self.entry.data["calendar_entity"]


        self.reset_time_str = self.entry.data["reset_time"]


        self.reset_time = dt_util.parse_time(self.reset_time_str)


        self.zone_state = self.hass.states.get(self.zone_entity)


        self.zone_friendly_name = self.zone_state.attributes.get("friendly_name") if self.zone_state else ""





    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()
        _LOGGER.info("minutes_in_zone: %s", self._minutes_in_zone)





        async_track_state_change_event(


            self.hass, self.person_entity, self._state_change_listener


        )





        async_track_time_change(


            self.hass, self._time_change_listener, self.reset_time.hour, self.reset_time.minute, self.reset_time.second


        )





    @callback
    def _state_change_listener(self, event: Event) -> None:
        """Handle person state changes."""
        _LOGGER.info("Person state changed: %s", event.data.get("new_state"))


        new_state = event.data.get("new_state")


        if new_state and new_state.state == self.zone_friendly_name:


            if self._minutes_in_zone > 0:


                if self._timer_task:


                    self._timer_task.cancel()


                self._timer_task = self.async_on_remove(


                    async_call_later(self.hass, timedelta(minutes=self._minutes_in_zone), self._timer_callback)


                )


            else:


                # If minutes_in_zone is 0, create event immediately


                self.hass.async_create_task(self._create_calendar_event())





        else:


            if self._timer_task:


                self._timer_task.cancel()


                self._timer_task = None





    async def _create_calendar_event(self) -> None:
        """Create a calendar event for the activity."""
        _LOGGER.info("Creating calendar event")


        yesterday = (dt_util.now() - timedelta(days=1)).strftime('%Y-%m-%d')


        today = dt_util.now().strftime('%Y-%m-%d')





        await self.hass.services.async_call(


            "calendar",


            "create_event",


            {


                "entity_id": self.calendar_entity,


                "summary": f"{self._attr_name}",


                "start_date": yesterday,


                "end_date": today,


            },


        )





    @callback
    def _timer_callback(self, now) -> None:
        """Callback for when the timer expires."""
        _LOGGER.info("Timer expired, creating calendar event")


        self.hass.async_create_task(self._create_calendar_event())


        self._attr_is_on = True


        self.async_write_ha_state()


        self._timer_task = None





    @callback
    def _time_change_listener(self, now) -> None:
        """Handle daily reset."""
        _LOGGER.info("Daily reset triggered")


        if self._timer_task:


            self._timer_task.cancel()


            self._timer_task = None


        self._attr_is_on = False


        self.async_write_ha_state()



