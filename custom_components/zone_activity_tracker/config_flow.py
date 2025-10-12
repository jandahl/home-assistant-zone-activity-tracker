"""Config flow for Zone Activity Tracker."""
import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers import selector

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ZoneActivityTrackerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zone Activity Tracker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        _LOGGER.info("User input: %s", user_input)
        if user_input is not None:
            person_name = user_input["person_entity"].split('.')[1].replace("_", " ").title()
            zone_name = user_input["zone_entity"].split('.')[1].replace("_", " ").title()
            return self.async_create_entry(title=f"Zone Activity: {person_name} in {zone_name}", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required("person_entity"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="person"),
                ),
                vol.Required("zone_entity"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="zone"),
                ),
                vol.Required("calendar_entity"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="calendar"),
                ),
                vol.Required("reset_time", default="04:00:00"): selector.TimeSelector(),
                vol.Required("minutes_in_zone", default=5): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=1440, mode="box"),
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema
        )
