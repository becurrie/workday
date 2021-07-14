from rumps import (
    separator,
)

from src.external.outlook import (
    outlook_manager,
)

from src.conf.conf import (
    ADD_REPOSITORY,
    PARSE_REPOSITORIES,
    GENERATE_REPORT,
    STOP_TRACKING,
    VIEW_LOCAL_DATA,
    DELETE_LOCAL_DATA,
    AUTO_GENERATE_REPORT_DAILY,
    ENABLE,
    DISABLE,
    HELP,
    ITINERARY_TYPE,
    MULTIPLE_EVENTS,
    SINGLE_EVENT,
    MINIMUM_EVENT_DURATION,
    FIVE_MINUTES,
    TEN_MINUTES,
    FIFTEEN_MINUTES,
    THIRTY_MINUTES,
    NONE,
    HARDCODED_START_TIME,
    SIX_AM,
    SEVEN_AM,
    EIGHT_AM,
    HARDCODED_END_TIME,
    THREE_PM,
    FOUR_PM,
    FIVE_PM,
    OUTLOOK_CALENDAR,
    DEBUG_MODE,
    ON,
    OFF,
    GRANT_AUTHENTICATION,
    REVOKE_AUTHENTICATION,
    ENABLE_JIRA_SYNC,
    DISABLE_JIRA_SYNC,
    CONFIGURE_JIRA_URL,
    CONFIGURE_JIRA_USERNAME,
    CONFIGURE_JIRA_TOKEN,
)
from src.conf.config import (
    config,
)

from src.app.callbacks import (
    click_add_repository_cb,
    click_parse_repositories_cb,
    click_generate_report_cb,
    click_stop_tracking_cb,
    click_view_local_data_cb,
    click_delete_local_data_cb,
    click_grant_authentication_cb,
    click_configure_jira_url_cb,
    click_configure_jira_username_cb,
    click_configure_jira_token_cb,
    click_enable_auto_generate_cb,
    click_auto_generate_help_cb,
    generate_config_callback,
)


def generate_options_spec():
    """Generate the options spec used to build the menu that houses all toggleable
    and configurable options within the system menu.

    [
        {
            "menu": <MENU_NAME>,
            "config": <CONFIGURATION_KEY>,
            "choices": [
                (<MENU_NAME>, <CALLBACK_FUNCTION>),
            ],
        },

        OR

        <separator>
    ]
    """
    return [
        {
            "menu": AUTO_GENERATE_REPORT_DAILY,
            "config": "generate_daily",
            "choices": [
                (ENABLE, click_enable_auto_generate_cb),
                (DISABLE, generate_config_callback(generate_daily=DISABLE, generate_daily_time=None)),
                separator,
                (HELP, click_auto_generate_help_cb),
            ],
        },
        separator,
        {
            "menu": ITINERARY_TYPE,
            "config": "itinerary_type",
            "choices": [
                (MULTIPLE_EVENTS, generate_config_callback(itinerary_type=MULTIPLE_EVENTS)),
                (SINGLE_EVENT, generate_config_callback(itinerary_type=SINGLE_EVENT)),
            ],
        },
        {
            "menu": MINIMUM_EVENT_DURATION,
            "config": "minimum_event_duration",
            "choices": [
                (FIVE_MINUTES, generate_config_callback(minimum_event_duration=FIVE_MINUTES)),
                (TEN_MINUTES, generate_config_callback(minimum_event_duration=TEN_MINUTES)),
                (FIFTEEN_MINUTES, generate_config_callback(minimum_event_duration=FIFTEEN_MINUTES)),
                (THIRTY_MINUTES, generate_config_callback(minimum_event_duration=THIRTY_MINUTES)),
            ],
        },
        {
            "menu": HARDCODED_START_TIME,
            "config": "hardcoded_start_time",
            "choices": [
                (NONE, generate_config_callback(hardcoded_start_time=NONE)),
                (SIX_AM, generate_config_callback(hardcoded_start_time=SIX_AM)),
                (SEVEN_AM, generate_config_callback(hardcoded_start_time=SEVEN_AM)),
                (EIGHT_AM, generate_config_callback(hardcoded_start_time=EIGHT_AM)),
            ],
        },
        {
            "menu": HARDCODED_END_TIME,
            "config": "hardcoded_end_time",
            "choices": [
                (NONE, generate_config_callback(hardcoded_end_time=NONE)),
                (THREE_PM, generate_config_callback(hardcoded_end_time=THREE_PM)),
                (FOUR_PM, generate_config_callback(hardcoded_end_time=FOUR_PM)),
                (FIVE_PM, generate_config_callback(hardcoded_end_time=FIVE_PM)),
            ],
        },
        separator,
        {
            "menu": OUTLOOK_CALENDAR,
            "config": "outlook_calendar",
            "choices": [
                (choice, generate_config_callback(outlook_calendar=choice))
                for choice in outlook_manager.calendar_choices
            ],
        },
        separator,
        {
            "menu": DEBUG_MODE,
            "config": "debug_mode",
            "choices": (
                (ON, generate_config_callback(debug_mode=ON)),
                (OFF, generate_config_callback(debug_mode=OFF)),
            ),
        },
    ]


def generate_repos_spec():
    """Generate the repos spec used to build the menu that houses all of the repositories
    that are currently tracked, and the options for each tracked repository.

    [
        {
            "menu": <MENU_NAME>,
            "callback": <CALLBACK_FUNCTION>,
        },

        OR

        <separator>

        OR

        {
            "menu": {
                "loop": <LOOP ITERABLE>,
                "sub_menus": [
                    {
                        "menu": <MENU_NAME>,
                        "callback": <CALLBACK_FUNCTION>,
                        "append": <APPEND LOOPED LOOP INSTANCE TO SUB MENU>,
                    },
                ],
            },
        },
    ]

    Notable Caveats:

    - The ``append`` key associated with a dynamic looped spec instance should
      be a string that represents the name of the attribute added to the sub menu
      being generated. For example, if we're looping over the tracked repositories,
      and append is set to "repository", then SubMenuItem.repository will be set to
      the repository in the loop being setup.

    - The ``separator`` instanced shown in the example above is usually just imported
      from the rumps module, it's a sentinel object used by rumps to determine when
      a separator instance should be added to the system tray menu.
    """
    return [
        {
            "menu": ADD_REPOSITORY,
            "callback": click_add_repository_cb,
        },
        {
            "menu": PARSE_REPOSITORIES,
            "callback": click_parse_repositories_cb,
        },
        separator,
        {
            "menu": {
                "loop": config.repositories,
                "sub_menus": [
                    {
                        "menu": GENERATE_REPORT,
                        "callback": click_generate_report_cb,
                        "append": "repository",
                    },
                    {
                        "menu": STOP_TRACKING,
                        "callback": click_stop_tracking_cb,
                        "append": "repository",
                    },
                ],
            },
        },
    ]


def generate_tools_spec():
    """Generate the tools spec used to build the menu that houses all of the tools
    available to be used by a user.

    [
        {
            "menu": <MENU_NAME>,
            "callback": <CALLBACK_FUNCTION>,
        },
    ]
    """
    return [
        {
            "menu": VIEW_LOCAL_DATA,
            "callback": click_view_local_data_cb,
        },
        {
            "menu": DELETE_LOCAL_DATA,
            "callback": click_delete_local_data_cb,
        },
    ]


def generate_outlook_spec():
    """Generate the outlook spec used to build the menu that houses all of the Outlook
    options available to be used by a user.

    [
        {
            "menu": <MENU_NAME>,
            "callback": <CALLBACK_FUNCTION>,
        },
    ]
    """
    return [
        {
            "menu": GRANT_AUTHENTICATION,
            "callback": click_grant_authentication_cb if not outlook_manager.authenticated else None,
        },
        {
            "menu": REVOKE_AUTHENTICATION,
            "callback": generate_config_callback(outlook_token=None) if outlook_manager.authenticated else None,
        },
    ]


def generate_jira_spec():
    """Generate the jira spec used to build the menu that houses all of the Jira
    options available to be used by a user.
    """
    return [
        {
            "menu": ENABLE_JIRA_SYNC,
            "callback": generate_config_callback(jira_enabled=True) if not config.jira_enabled else None,
        },
        {
            "menu": DISABLE_JIRA_SYNC,
            "callback": generate_config_callback(jira_enabled=False) if config.jira_enabled else None,
        },
        separator,
        {
            "menu": CONFIGURE_JIRA_URL,
            "callback": click_configure_jira_url_cb,
        },
        {
            "menu": CONFIGURE_JIRA_USERNAME,
            "callback": click_configure_jira_username_cb,
        },
        {
            "menu": CONFIGURE_JIRA_TOKEN,
            "callback": click_configure_jira_token_cb,
        },
    ]
