# Zone Activity Tracker

This is a Home Assistant custom integration that tracks when a person enters a specific zone and logs this activity to a persistent calendar.

## Installation

This integration is not yet part of the default HACS store. You can install it as a custom repository.

1.  Go to your HACS page in Home Assistant.
2.  Click on the three dots in the top right corner and select "Custom repositories".
3.  In the dialog, paste the following URL into the "Repository" field:
    ```
    https://github.com/jandahl/home-assistant-zone-activity-tracker
    ```
4.  Select "Integration" as the category and click "Add".
5.  The "Zone Activity Tracker" card will now appear. Click "Install" and proceed with the installation.
6.  Restart Home Assistant.
7.  Go to **Settings > Devices & Services > Add Integration** and search for **Zone Activity Tracker**.

## Configuration

-   **Person to Track**: Select the person entity to track.
-   **Trigger Zone**: Select the zone entity that triggers the activity.
-   **Target Calendar**: Select the calendar entity where the activity log will be created.
-   **Reset Time**: Set the time for the daily reset (defaults to 04:00:00).
