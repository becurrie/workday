from requests.exceptions import (
    HTTPError,
)

from atlassian import (
    Jira,
)

from src.conf.config import (
    config,
)


class JiraManager:
    def __init__(self):
        """Initialize a new JiraManager, exposing valid utilities used by the Workday
        app. Authentication is handled by collecting information from the user about
        their current Jira setup.
        """
        self._issues = {}

    @property
    def _jira(self):
        """Utility method to generate the jira instance using the currently
        configured local jira settings set by the user.
        """
        return Jira(
            url=config.jira_url,
            username=config.jira_username,
            password=config.jira_token,
        )

    def _get_issue(self, issue):
        """Retrieve an issue from Jira.
        """
        if issue not in self._issues:
            try:
                self._issues[issue] = self._jira.issue(
                    key=issue,
                )
            except HTTPError:
                # An HTTPError in this case means the issue either does
                # not exist, or we don't permission to retrieve it's information.
                return None

        return self._issues[issue]

    def issue_exists(self, issue):
        """Check to see if an issue exists in the Jira system available.

        If one does exist, it is also cached on the manager for use again
        to prevent lots of api requests.
        """
        if self._get_issue(issue=issue):
            return True
        return False

    def issue_summary(self, issue):
        """Retrieve an issue title.
        """
        return self._get_issue(issue=issue)["fields"]["summary"]

    def issue_description(self, issue):
        """Retrieve an issue description.
        """
        return self._get_issue(issue=issue)["fields"]["description"]


jira_manager = JiraManager()
