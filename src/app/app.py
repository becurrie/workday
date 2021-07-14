from rumps import (
    App,
    alert,
    clicked,
    timer,
)

from src.conf.conf import (
    APP_ICON,
    APP_NAME,
    APP_VERSION,
    REPOSITORIES,
    TOOLS,
    OPTIONS,
    OUTLOOK,
    JIRA,
    ABOUT,
)

from src.app.menus import (
    build_tracked_repos_menu,
    build_options_menu,
    build_outlook_menu,
    build_jira_menu,
)


class WorkDayApp(App):
    @timer(5)
    def refresh_menu(self, sender):
        """Refresh the menu on a timer.

        Note: It'd be nice here to just run this whenever the menu is clicked on and shown,
              this is an issue slated within the rumps repository, if this becomes possible,
              update our menu with "dynamic" data on menu show. instead of on a timer.
        """
        for refresh_spec in [
            (REPOSITORIES, TOOLS, build_tracked_repos_menu, self.menu.insert_before),
            (OPTIONS, TOOLS, build_options_menu, self.menu.insert_after),
            (OUTLOOK, ABOUT, build_outlook_menu, self.menu.insert_before),
            (JIRA, OUTLOOK, build_jira_menu, self.menu.insert_after),
        ]:
            # (<menu>, <insert>, <menu_cb>, <insert_func>)
            self.menu.pop(refresh_spec[0])
            # Generating the refreshed menu for each
            # spec's refresh above.
            refresh_spec[3](
                refresh_spec[1],
                refresh_spec[2](),
            )

    @clicked(ABOUT)
    def about(self, sender):
        """Display a simple about page with some information about the application.
        """
        alert(
            icon_path=APP_ICON,
            title="%(app_name)s %(version)s" % {
                "app_name": APP_NAME,
                "version": APP_VERSION,
            },
            message=(
                "Workday allows users to track chosen git repositories to get a better idea of what "
                "issues/branches are being worked on throughout the day."
            ),
        )
