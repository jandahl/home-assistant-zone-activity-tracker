# Zone Activity Tracker

This is a Home Assistant custom integration that tracks when a person enters a specific zone and logs this activity to a persistent calendar.

## Installation

1.  Install via [HACS](https://hacs.xyz/).
2.  Restart Home Assistant.
3.  Go to **Settings > Devices & Services > Add Integration** and search for **Zone Activity Tracker**.

## Configuration

-   **Person to Track**: Select the person entity to track.
-   **Trigger Zone**: Select the zone entity that triggers the activity.
-   **Reset Time**: Set the time for the daily reset (defaults to 04:00:00).
