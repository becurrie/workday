from rumps import (
    MenuItem,
    separator,
)

from src.conf.config import (
    config,
)
from src.conf.conf import (
    REPOSITORIES,
    TOOLS,
    OPTIONS,
    OUTLOOK,
    JIRA,
    ABOUT,
)

from src.app.specs import (
    generate_repos_spec,
    generate_tools_spec,
    generate_options_spec,
    generate_outlook_spec,
    generate_jira_spec,
)


def generate_menu():
    """Generate the menu used by our system tray application.
    """
    return [
        build_tracked_repos_menu(),
        build_tools_menu(),
        build_options_menu(),
        separator,
        build_outlook_menu(),
        build_jira_menu(),
        separator,
        ABOUT,
        separator,
    ]


def build_tracked_repos_menu():
    """Build the menu that contains the currently configured list of repositories
    that are being tracked by the src application.

    An option to add a new repository is provided always, and the currently available
    repositories are pulled from a local configuration and clicking on any of them
    will open the currently available audited src information that's stored.
    """
    menu = MenuItem(REPOSITORIES)

    for spec in generate_repos_spec():
        if isinstance(spec, dict):
            if isinstance(spec["menu"], str):
                # Just add a menu item with the callback available.
                # No additional work needed.
                menu.add(MenuItem(spec["menu"], callback=spec["callback"]))
            else:
                # Looping through the spec menu, else case here handles dynamic
                # loading of a menu through the ``loop`` variable.
                for loop in spec["menu"]["loop"]:
                    loop_menu = MenuItem(loop)
                    for sub in spec["menu"]["sub_menus"]:
                        sub_menu = MenuItem(sub["menu"], callback=sub["callback"])
                        if sub["append"]:
                            # If appending, append the dynamic loop value
                            # to the sub menu, usually aids in the callback
                            # being used with the dynamic menu option.
                            setattr(sub_menu, sub["append"], loop)
                        loop_menu.add(sub_menu)
                    menu.add(loop_menu)
        else:
            menu.add(spec)

    return menu


def build_tools_menu():
    """Build the menu that contains the currently configured tools that can be
    executed by a user upon clicking on any of the available tools.
    """
    menu = MenuItem(TOOLS)

    for spec in generate_tools_spec():
        menu.add(MenuItem(spec["menu"], callback=spec["callback"]))

    return menu


def build_options_menu():
    """Build the menu that contains the currently configured options that can be
     toggled by a user upon clicking on any of the available tools.
     """
    menu = MenuItem(OPTIONS)

    for spec in generate_options_spec():
        if isinstance(spec, dict):
            spec_menu = MenuItem(spec["menu"])
            for spec_choice in spec["choices"]:
                spec_choice_menu = MenuItem(spec_choice[0], callback=spec_choice[1])
                spec_choice_menu.state = int(config.config.get(spec["config"]) == spec_choice[0])
                spec_menu.add(spec_choice_menu)
            menu.add(spec_menu)
        else:
            menu.add(spec)

    return menu


def build_outlook_menu():
    """Build the menu that contains the currently configured outlook options that can be
    executed by a user upon clicking on any of the available tools.
    """
    menu = MenuItem(OUTLOOK)

    for spec in generate_outlook_spec():
        menu.add(MenuItem(spec["menu"], callback=spec["callback"]))

    return menu


def build_jira_menu():
    """Build the menu that contains the currently configured jira options that can be
    executed by a user upon clicking on any of the available tools.
    """
    menu = MenuItem(JIRA)

    for spec in generate_jira_spec():
        if isinstance(spec, dict):
            menu.add(MenuItem(spec["menu"], callback=spec["callback"]))
        else:
            menu.add(spec)

    return menu
