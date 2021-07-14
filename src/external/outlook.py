import webbrowser

from rumps import (
    Window,
    alert,
    notification,
)

from O365 import (
    Account,
)
from O365.utils import (
    BaseTokenBackend,
)

from src.external.jira import (
    jira_manager,
)

from src.conf.conf import (
    MULTIPLE_EVENTS,
    SINGLE_EVENT,
    DEFAULT_CALENDAR,
)
from src.conf.config import (
    config,
)
from src.utilities import (
    wait_for_result,
    strfdelta,
)

CLIENT_ID = "006bcaaa-d41f-47b5-a1e9-4c4035933190"
AUTH_TYPE = "public"
SCOPES = [
    "offline_access",
    "calendar_all",
]


class WorkdayTokenBackend(BaseTokenBackend):
    def delete_token(self):
        """Deletes the token from the configuration available.
        """
        config.update(outlook_token=None)

    def check_token(self):
        """Checks if the token exists in the configuration available.
        """
        return config.outlook_token is not None

    def load_token(self):
        """Retrieves the token from the configuration available.
        """
        token = None

        if config.outlook_token:
            token = self.token_constructor(config.outlook_token)

        return token

    def save_token(self):
        """Saves the token dictionary in the configuration available.
        """
        if self.token is None:
            raise ValueError(
                "You must set the \"token\" first."
            )

        config.update(
            outlook_token=self.token,
        )

        return True


class OutlookManager:
    def __init__(self):
        """Initialize a new OutlookManager, ensuring scopes, clients and
        credentials are set up correctly. We also create the ``account`` object here
        and handle the custom TokenBackend before any authentication takes place.
        """
        self._calendars = {}
        self._scopes = SCOPES
        self._client_id = CLIENT_ID
        self._auth_type = AUTH_TYPE
        self._credentials = (
            self._client_id,
        )
        self.account = Account(
            credentials=self._credentials,
            auth_flow_type=self._auth_type,
            token_backend=WorkdayTokenBackend(),
        )
        self.itinerary_map = {
            MULTIPLE_EVENTS: self.generate_itinerary_multiple_events,
            SINGLE_EVENT: self.generate_itinerary_single_event,
        }

    @property
    def authenticated(self):
        """Return a boolean representing if the Outlook account is authenticated.
        """
        self.account = Account(
            credentials=self._credentials,
            auth_flow_type=self._auth_type,
            token_backend=WorkdayTokenBackend(),
        )
        return self.account.is_authenticated

    @property
    def calendar_choices(self):
        """Return a list of all available Calendars within the Outlook account.
        """
        if not self._calendars:
            if self.authenticated:
                default = self.account.schedule().get_default_calendar()
                # {
                #     "default" : <DEFAULT_CALENDAR>,
                #     "<CALENDAR_NAME>: <CALENDAR>,
                #     ...
                # }
                self._calendars = {
                    DEFAULT_CALENDAR: default,
                    **{
                        c.name: c
                        for c in self.account.schedule().list_calendars() if c.name != default.name
                    }
                }

        return self._calendars

    def _calendar(self):
        """Retrieve the currently configured calendar, this can be either the "Default Calendar",
        or one of the dynamically available calendars available within a users account.
        """
        schedule = self.account.schedule()
        calendar = self._calendars[config.outlook_calendar]

        return calendar

    @staticmethod
    def handle_consent_cb(consent_url):
        """When handling an authentication flow with consent, we use this callback to capture
        the consented url when a user logs into their Outlook account and grants access.
        """
        webbrowser.open_new_tab(
            url=consent_url,
        )

        # Create a window that we can use to allow the user to enter back
        # the resulting url after logging into outlook and granting access.
        window = Window(
            title="Enter Authentication Url",
            message=(
                "After logging into Outlook and granting access, please paste back the resulting url "
                "here to allow Workday access to your Outlook Account.\n\n"
                "The Workday app is limited to only accessing your Calendar data to add and remove "
                "events in your calendar."
            ),
            cancel=True,
        )

        result = wait_for_result(
            window=window,
        )
        if result is None:
            # Authentication aborted...
            notification(
                title="Authentication",
                subtitle="Authentication Aborted",
                message="The authentication flow has been aborted.",
            )
        return result

    def authenticate(self):
        """Authenticate the user if an existing authentication token doesn't already exist
        in the users token backend.
        """
        if not self.account.is_authenticated:
            result = alert(
                title="Outlook Authentication Required",
                message=(
                    "Outlook authentication is required to allow calendar updates. "
                    "Please press the \"Ok\" button to begin Outlook authentication."
                ),
                cancel=True,
            )
            # result == 1: "Ok"
            # result == 0: "Cancel"
            if result == 0:
                return False

            if not self.account.authenticate(
                scopes=self._scopes,
                handle_consent=self.handle_consent_cb,
            ):
                return False
            notification(
                title="Authentication",
                subtitle="Authentication Successful",
                message="Your Outlook Account has been successfully authenticated.",
            )
        return True

    @staticmethod
    def generate_event_subject(instance, single_event=False):
        """Generate the event subject for a given ``instance``. The instance should
        be an object that represents an event generated by our repository parser.
        """
        if single_event:
            cnt = len(instance["branches"])
            duration = instance["end"] - instance["start"]
            # Single event subject should just use a simple
            # summary with information about what was worked on.
            return (
                f"{cnt} Issues Worked On ({strfdelta(duration)})"
            )
        else:
            branch = instance["branch"]
            issue = instance["issue"]
            duration = instance["end"] - instance["start"]
            # Otherwise, we're generating the subject for a single issue.
            # Using Jira to find the subject.
            if config.jira_enabled:
                if jira_manager.issue_exists(issue=issue):
                    summary = jira_manager.issue_summary(issue=issue)
                    return (
                        f"{branch} - {summary} - {strfdelta(duration)}"
                    )
            # The issue does not exist OR the Jira configurations
            # are invalid OR Jira is disabled, we'll just default
            # to a basic summary.
            return (
                f"{branch}"
            )

    @staticmethod
    def generate_event_body(instance, single_event=False):
        """Generate the event body for a given ``instance``. The instance should
        be an object that represents an event generated by our repository parser.
        """
        if single_event:
            branches = instance["branches"]
            issues = instance["issues"]
            durations = instance["durations"]
            descriptions = {}
            # Single event body should use a more complex lookup
            # to find each issues description to include.
            for issue in issues:
                if config.jira_enabled:
                    if jira_manager.issue_exists(issue=issue):
                        descriptions[issue] = jira_manager.issue_description(issue=issue)

            pieces = []

            for issue, branch in zip(issues, branches):
                body = (
                    f"<strong>{branch} ({strfdelta(durations[branch])})</strong>"
                )
                if issue in descriptions:
                    body += (
                        f"<br />{descriptions[issue]}<br />"
                    )
                pieces.append(body)

            pieces = "<br /><br />".join(pieces)
            pieces += "<br /><br />Generated By Workday."

            return pieces
        else:
            branch = instance["branch"]
            issue = instance["issue"]
            duration = instance["duration"]
            # Otherwise, we're generating the body for a single issue.
            # Using Jira to find the description.
            body = (
                f"{branch} ({strfdelta(duration)})"
            )
            if config.jira_enabled:
                if jira_manager.issue_exists(issue=issue):
                    description = jira_manager.issue_description(issue=issue)
                    body += (
                        f"<br />{description}<br />"
                    )
            # The issue does not exist OR the Jira configurations
            # are invalid OR Jira is disabled, we'll just default
            # to a basic description.
            return body + "<br /><br />Generated By Workday."

    def generate_itinerary_multiple_events(self, calendar, itinerary):
        """Generate Outlook Events that represent the specified itinerary.
        """
        for instance in itinerary:
            event = calendar.new_event()
            event.subject = self.generate_event_subject(instance=instance)
            event.body = self.generate_event_body(instance=instance)
            event.start = instance["start"]
            event.end = instance["end"]
            event.save()

    def generate_itinerary_single_event(self, calendar, itinerary):
        """Generate Outlook Event that represents the specified itinerary.
        """
        branches = set(instance["branch"] for instance in itinerary)
        issues = [b.split("/")[-1] if "/" in b else b for b in branches]
        single_itinerary = {
            "start": itinerary[0]["start"],
            "end": itinerary[-1]["end"],
            "branches": branches,
            "issues": issues,
            "durations": {},
        }

        for instance in itinerary:
            if instance["branch"] not in single_itinerary["durations"]:
                single_itinerary["durations"][instance["branch"]] = instance["duration"]
            else:
                single_itinerary["durations"][instance["branch"]] += instance["duration"]

        event = calendar.new_event()
        event.start = single_itinerary["start"]
        event.end = single_itinerary["end"]
        event.subject = self.generate_event_subject(instance=single_itinerary, single_event=True)
        event.body = self.generate_event_body(instance=single_itinerary, single_event=True)

        event.save()

    def generate_itinerary(self, itinerary, itinerary_type):
        """Generate Outlook Event(s) that represent the itinerary available.

        The ``itinerary_type`` specified is used to determine how the ``itinerary`` itself
        is transformed into an Outlook instance.
        """
        if not self.account.is_authenticated:
            raise ValueError(
                "Validation has failed, only call functionality that makes use of the "
                "O365 API once access/consent has been granted to the application."
            )

        calendar = self._calendar()

        if itinerary_type not in self.itinerary_map:
            raise ValueError(
                f"``itinerary_type``: \"{itinerary_type}\" is not currently supported."
            )

        itinerary_func = self.itinerary_map[itinerary_type]
        itinerary_func(
            calendar=calendar,
            itinerary=itinerary,
        )


outlook_manager = OutlookManager()
