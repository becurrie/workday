from simple_config import (
    Config,
)

from src.conf.conf import (
    USER_CONFIG_FILE,
    USER_DATA_FILE,
    DISABLE,
    MULTIPLE_EVENTS,
    FIVE_MINUTES,
    DEFAULT_CALENDAR,
    OFF,
)


class ExtConfig(Config):
    def sync(self):
        """Sync up the specified configuration, ensuring any missing ``defaults`` are available and set
        on the instance.
        """
        for default, value in self.defaults.items():
            if default not in self.config:
                self.update(**{
                    default: value,
                })

        remove = []

        for existing, value in self.config.items():
            if existing not in self.defaults:
                remove.append(
                    existing,
                )
        if remove:
            for rem in remove:
                self.config.pop(rem)
            self.update()


config = ExtConfig(
    path=USER_CONFIG_FILE,
    defaults={
        "outlook_token": None,
        "outlook_calendar": DEFAULT_CALENDAR,
        "jira_enabled": False,
        "jira_url": None,
        "jira_username": None,
        "jira_token": None,
        "repositories": [],
        "generate_daily": DISABLE,
        "generate_daily_time": None,
        "itinerary_type": MULTIPLE_EVENTS,
        "minimum_event_duration": FIVE_MINUTES,
        "hardcoded_start_time": None,
        "hardcoded_end_time": None,
        "debug_mode": OFF,
    },
)

data = ExtConfig(
    path=USER_DATA_FILE,
    defaults={
        "tracked": {},
        "auto_handled": [],
    },
)

config.sync()
data.sync()
