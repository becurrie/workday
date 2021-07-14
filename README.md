# Workday

[![Version](https://img.shields.io/github/v/release/becurrie/workday?include_prereleases&logo=github)](https://github.com/becurrie/workday/releases/latest)
[![Issues](https://img.shields.io/github/issues/becurrie/workday?label=issues&logo=github)](https://github.com/becurrie/workday/issues)

Workday is a python application that tracks git repositories and allows users
to generate reports for the current day, syncing all worked on branches with
an Outlook calendar.

## Requirements

- Python 3.9+
- MacOS

## How It Works

Workday works by using the `reflog` associated with a repository, this essentially keeps
track of all the commands that have been run against a repository. With this information,
workday is able to generate and parse the data from this command into an itinerary view
that shows how long you've spent on each branch throughout the day.

When a report is generated by a user, the Outlook API is used to sync the available events
with a calendar chosen by the user.

- An additional configuration is available to sync report generation with Jira, allowing issue
  summaries and descriptions to be included in the events synced with Outlook.

### Outlook Authentication

Outlook authentication can be handled through the Outlook menu available in the system-tray
application manually, or authentication will be handled during report generation if it hasn't
already been configured.

Outlook authentication is handled through an OAuth2 flow that asks you to sign in on the web,
and copy and paste the resulting url into a prompt. All of your authentication information is stored
locally, and you only ever need to sign in once (unless you manually revoke Outlook access).

### Jira Authentication

Jira authentication is a separate, optional setting that can be enabled/disabled through the
system-tray application. Jira authentication requires the following settings to be configured manually
before additional branch information/context is included when generating reports:

| Jira Configuration | Description                                                                                               |
|--------------------|----------------------------------------------------------------------------------------------------------|
| Jira Url           | Your current Jira url, usually similar to: https://organization.atlassian.net/                           |
| Jira Username      | Your current Jira username/email.                                                                        |
| Jira Token         | Your current Jira token, generated manually, https://id.atlassian.com/manage-profile/security/api-tokens  |

If you're Jira options are set up correctly, and you have enabled Jira Sync, additional information
is used when generating a daily report, the `Subject` line of an event will also include the `Summary`
taken from the associated Jira issue, and the `Body` of an event will include the `Description` of the 
associated Jira issue.

## Installation

- You can also just download the latest executable from [here](https://github.com/becurrie/workday/releases/latest) 
  instead of pulling down the source code and setting up a development environment.

If you plan on setting up a development environment, use the instructions below:

- Clone or download the source code available on the latest `main` branch.
- Install the requirements taken from the `requirements.txt` file.

```bash
pip install -r requirements/requirements.txt
```

## Usage

> If you're using the latest executable available, you can just launch the application
> directly and ignore the instructions below.

- Run `src/workday.py` to launch the application from within a development environment.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to 
discuss what you would like to change or add.
