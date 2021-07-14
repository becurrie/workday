from subprocess import (
    call,
)

from rumps import (
    Window,
    notification,
)

from src.parse import (
    RepositoryParser,
)
from src.external.outlook import (
    outlook_manager,
)

from src.conf.conf import (
    USER_DATA_DIR,
)
from src.conf.config import (
    config,
    data,
)
from src.utilities import (
    wait_for_result,
)
from src.validators import (
    validate_directory,
    validate_repository,
    validate_repository_duplicate,
)


def click_add_repository_cb(sender):
    """Handle the use case where a user clicks on the ``Add Repository`` menu item available.

    We'll present a prompt to the user, allowing them to enter a directory, if the directory
    is a valid git repository, we'll add it to the list of tracked repositories available.
    """
    window = Window(
        title="Add Repository",
        message="Add the path of a repository to begin tracking it.",
        cancel=True,
    )
    result = wait_for_result(
        window=window,
        validators=[
            validate_directory,
            validate_repository,
            validate_repository_duplicate,
        ],
    )

    if result is not None:
        # Valid repository, update user configuration for local state
        # updated, etc...
        config.update(
            repositories=config.repositories + [result],
        )
        notification(
            title="Repository Added",
            subtitle="New Repository Added Successfully",
            message=f"The repository: {result} was successfully added to your list of tracked repositories.",
        )


def click_parse_repositories_cb(sender, manual=True):
    """Handle the user case where a user clicks on the ``Parse Repositories`` menu item available.
    """
    for repository in config.repositories:
        result = RepositoryParser(repository).parse()
        if manual:
            notification(
                title="Repository Parsed",
                subtitle="Repository Parsed Successfully",
                message=f"The repository: {repository} was successfully parsed.",
            )


def click_generate_report_cb(sender):
    """Handle the use case where a user clicks on the ``Generate Report`` menu item available.
    """
    if outlook_manager.authenticate():
        outlook_manager.generate_itinerary(
            itinerary=RepositoryParser(sender.repository).generate(),
            itinerary_type=config.itinerary_type,
        )
        notification(
            title="Generate Report",
            subtitle="Workday Report Generated",
            message="Workday report has been generated successfully.",
        )


def click_stop_tracking_cb(sender):
    """Handle the user case where a user clicks on the ``Stop Tracking`` menu item available.
    """
    repositories = config.repositories
    repositories.pop(repositories.index(sender.repository))

    config.update(
        repositories=repositories,
    )
    notification(
        title="Stop Tracking",
        subtitle="Stop Tracking Repository",
        message=f"No longer tracking repository: \"{sender.repository}\".",
    )


def click_view_local_data_cb(sender):
    """Handle the use where where a user clicks on the ``View Local Data`` menu item available.
    """
    call([
        "open",
        USER_DATA_DIR,
    ])


def click_delete_local_data_cb(sender):
    """Handle the use case where a user clicks on the ``Reset Data`` menu item available.
    """
    config.update(**config.defaults)
    data.update(**data.defaults)
    notification(
        title="Local Data Deleted",
        subtitle="Local Data Deleted Successfully",
        message="Your local data has been deleted successfully.",
    )


def click_grant_authentication_cb(sender):
    """Handle the use case where a user clicks on the ``Grant Authentication`` menu item available.
    """
    outlook_manager.authenticate()


def click_configure_jira_url_cb(sender):
    """Handle the use case where a user clicks on the ``Configure Jira Url`` menu item available.
    """
    window = Window(
        title="Configure Jira Url",
        message="Enter the jira server url that you currently use.",
        dimensions=(320, 50),
        cancel=True,
    )
    result = wait_for_result(
        window=window,
    )

    if result is not None:
        config.update(
            jira_url=result,
        )
        notification(
            title="Configure Jira Url",
            subtitle="Jira Url Configured Successfully",
            message=f"Jira url has been set to \"{result}\".",
        )


def click_configure_jira_username_cb(sender):
    """Handle the use case where a user clicks on the ``Configure Jira Username`` menu item available.
    """
    window = Window(
        title="Configure Jira Username",
        message="Enter your jira username.",
        dimensions=(320, 50),
        cancel=True,
    )
    result = wait_for_result(
        window=window,
    )

    if result is not None:
        config.update(
            jira_username=result,
        )
        notification(
            title="Configure Jira Username",
            subtitle="Jira Username Configured Successfully",
            message=f"Jira username has been set to \"{result}\".",
        )


def click_configure_jira_token_cb(sender):
    """Handle the use case where a user clicks on the ``Configure Jira Token`` menu item available.
    """
    window = Window(
        title="Configure Jira Token",
        message=(
            "Enter your jira token. This is an api token that is "
            "generated manually by you through the jira settings page.\n\n"
            "You can use this link to generate a new token: "
            "https://id.atlassian.com/manage-profile/security/api-tokens"
        ),
        dimensions=(320, 50),
        cancel=True,
    )
    result = wait_for_result(
        window=window,
    )

    if result is not None:
        config.update(
            jira_token=result,
        )
        notification(
            title="Configure Jira Token",
            subtitle="Jira Token Configured Successfully",
            message=f"Jira token has been set to \"{result}\".",
        )


def generate_config_callback(**kwargs):
    """Generate a callback function to update a specified config value.
    """
    def callback(sender):
        config.update(
            **kwargs,
        )
    return callback
