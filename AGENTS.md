Project Brief
This file contains the complete, detailed project specifications. You can reuse this for future reference or other projects.

<immersive type="text/markdown" download_filename="GEMINI.md">

Project Brief: Home Assistant 'Zone Activity Tracker' Custom Integration
1. Project Goal
The primary goal of this project is to create a HACS-compliant custom integration for Home Assistant named "Zone Activity Tracker". This integration will encapsulate the logic for tracking when a person enters a specific geographical zone and logging this activity to a persistent calendar. It is intended to replace a series of manual YAML automations and helpers with a clean, reusable, and UI-configurable integration.

2. User Story
As a Home Assistant user, I want to easily track and log my daily activities, such as using public transit or arriving at work. I want to:

Install a single integration via HACS.

Configure it through the UI by selecting the person I want to track, the zone that represents the activity, and a daily reset time.

Have the integration automatically create a binary sensor that shows if I have entered the zone "today".

Have the integration automatically create a local calendar that permanently logs every day the activity occurred.

All of this should work reliably in the background without me needing to write any YAML code.

3. Core Functional Requirements
3.1. UI-Based Configuration (Config Flow)
The integration must be configurable entirely through the Home Assistant UI (Settings > Devices & Services > Add Integration). The setup wizard (Config Flow) must prompt the user for the following:

Person to Track: A dropdown list of all person entities.

Trigger Zone: A dropdown list of all zone entities.

Reset Time: A time input for the daily reset. This should default to "04:00:00".

3.2. Automatic Entity Creation
Upon successful configuration, the integration must create and manage two new entities:

binary_sensor: This entity will represent the daily state. It will be on if the tracked person has entered the trigger zone within the 24-hour cycle (defined by the reset time) and off otherwise.

calendar: This entity will serve as the permanent, long-term log. It will store an all-day event for each day that the activity occurred.

3.3. Internal Logic
All detection and logging logic must be handled internally by the integration's Python code, using event listeners.

Detection Logic: The integration must listen for state changes of the configured person entity. When the person's state changes to the friendly name of the configured zone (indicating they have entered the zone), the integration's binary_sensor must be turned on.

Daily Log & Reset Logic: The integration must listen for the specified daily reset time. At this time, it will:

Check if its binary_sensor is on.

If on, it must create a new all-day event in its calendar entity for the previous day. (e.g., a 4:00 AM trigger on May 26th logs an event for May 25th).

After the check, it must turn its binary_sensor off to prepare for the new day.

4. Technical & Architectural Requirements
HACS Compliance: The file structure must be 100% compliant for distribution via HACS, following the custom_components/integration_domain/ structure.

Asynchronous Code: All Home Assistant API calls and setup procedures must be asynchronous, using async and await.

Data Persistence: The calendar log must be permanent and not subject to the recorder's purge_keep_days setting. This will be achieved by having the calendar entity inherit from homeassistant.components.local_calendar.LocalCalendarEntity, which stores its data in a separate .ics file.

Code Quality: The code must be well-commented, follow PEP 8 standards, and be logically organized into the correct files.

5. File Structure & Content Specification
The integration domain shall be zone_activity_tracker. The following file structure must be generated:

/custom_components/zone_activity_tracker/
├── __init__.py
├── manifest.json
├── const.py
├── config_flow.py
├── binary_sensor.py
└── calendar.py
File Content Details:
const.py:

Define the integration DOMAIN as "zone_activity_tracker".

manifest.json:

Create a valid manifest file including domain, name ("Zone Activity Tracker"), version ("1.0.0"), documentation and issue_tracker (placeholder URLs), codeowners (placeholder username), and iot_class ("local_polling").

__init__.py:

Implement async_setup_entry to forward the setup to the binary_sensor and calendar platforms.

Implement async_unload_entry to handle the unloading of the platforms.

config_flow.py:

Create a ZoneActivityTrackerConfigFlow class inheriting from config_entries.ConfigFlow.

Implement the async_step_user method.

Use voluptuous to define a schema with selector.EntitySelector for person_entity and zone_entity, and selector.TimeSelector for reset_time (defaulting to "04:00:00").

On submission, create the config entry via self.async_create_entry().

binary_sensor.py:

Implement async_setup_entry to create the sensor entity.

Create a ZoneActivityBinarySensor class inheriting from BinarySensorEntity.

In async_added_to_hass, set up two listeners:

State Listener: Use async_track_state_change_event to monitor the configured person entity. The callback must check if event.data.get("new_state").state matches the friendly name of the configured zone entity. If it matches, set the sensor's state to True.

Time Listener: Use event.async_track_time_change to trigger at the configured reset_time. The callback will:

Check if self.is_on.

If True, call the calendar.create_event service. CRITICAL: The event must be an all-day event for the previous day. The start_date should be (now() - timedelta(days=1)).strftime('%Y-%m-%d') and the end_date should be now().strftime('%Y-%m-%d').

Set the sensor's state to False.

calendar.py:

Implement async_setup_entry.

Create a ZoneActivityCalendar class that inherits from homeassistant.components.local_calendar.LocalCalendarEntity. This is the key to achieving persistent .ics file storage.

The entity should have a clear name and unique ID derived from the config entry.

