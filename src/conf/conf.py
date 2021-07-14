import os

from appdirs import (
    user_data_dir,
    user_log_dir,
)

APP_ICON = "_AppIcon.png"

APP_NAME = "Workday"
APP_AUTHOR = "becurrie"
APP_VERSION = "0.0.1"


USER_DATA_DIR = user_data_dir(
    appname=APP_NAME,
    appauthor=APP_AUTHOR,
)
USER_LOG_DIR = user_log_dir(
    appname=APP_NAME,
    appauthor=APP_AUTHOR,
)

# The config file is used when our ``config.py`` instance is imported
# within our module, defaults are handled gracefully.
USER_CONFIG_FILE = "%(user_data_dir)s%(sep)s%(config_file)s" % {
    "user_data_dir": USER_DATA_DIR,
    "sep": os.sep,
    "config_file": "config.json",
}
# The data file used when our ``config.py`` instance is imported
# within our module, defaults are handled gracefully.
USER_DATA_FILE = "%(user_data_dir)s%(sep)s%(data_file)s" % {
    "user_data_dir": USER_DATA_DIR,
    "sep": os.sep,
    "data_file": "data.json",
}

# Some of the constants that we use to represent configurations or settings
# that are persisted through the app can be stored here and used throughout.
REPOSITORIES = "Repositories"
ADD_REPOSITORY = "Add Repository"
PARSE_REPOSITORIES = "Parse Repositories"

GENERATE_REPORT = "Generate Report"
STOP_TRACKING = "Stop Tracking"

TOOLS = "Tools"
VIEW_LOCAL_DATA = "View Local Data"
DELETE_LOCAL_DATA = "Delete Local Data"

OPTIONS = "Options"
ITINERARY_TYPE = "Itinerary Type"
MULTIPLE_EVENTS = "Multiple Events"
SINGLE_EVENT = "Single Event"
MINIMUM_EVENT_DURATION = "Minimum Event Duration"
FIVE_MINUTES = "5 Minutes"
TEN_MINUTES = "10 Minutes"
FIFTEEN_MINUTES = "15 Minutes"
THIRTY_MINUTES = "30 Minutes"
NONE = "None"
HARDCODED_START_TIME = "Hardcoded Start Time"
SIX_AM = "6:00 AM"
SEVEN_AM = "7:00 AM"
EIGHT_AM = "8:00 AM"
HARDCODED_END_TIME = "Hardcoded End Time"
THREE_PM = "3:00 PM"
FOUR_PM = "4:00 PM"
FIVE_PM = "5:00 PM"
OUTLOOK_CALENDAR = "Outlook Calendar"
DEFAULT_CALENDAR = "Default Calendar"
DEBUG_MODE = "Debug Mode"
ON = "On"
OFF = "Off"

OUTLOOK = "Outlook"
GRANT_AUTHENTICATION = "Grant Authentication"
REVOKE_AUTHENTICATION = "Revoke Authentication"

JIRA = "Jira"
ENABLE_JIRA_SYNC = "Enable Jira Sync"
DISABLE_JIRA_SYNC = "Disable Jira Sync"
CONFIGURE_JIRA_URL = "Configure Jira Url"
CONFIGURE_JIRA_USERNAME = "Configure Jira Username"
CONFIGURE_JIRA_TOKEN = "Configure Jira Token"

ABOUT = "About"

# Any additional constants or maps can be placed here that make
# use of or transform the constants above.
DURATION_MAP = {
    FIVE_MINUTES: 5,
    TEN_MINUTES: 10,
    FIFTEEN_MINUTES: 15,
    THIRTY_MINUTES: 30,
}
HOUR_MAP = {
    "6:00 AM": 6,
    "7:00 AM": 7,
    "8:00 AM": 8,
    "3:00 PM": 15,
    "4:00 PM": 16,
    "5:00 PM": 17,
}
