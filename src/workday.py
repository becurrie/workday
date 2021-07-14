from src.conf.conf import (
    APP_ICON,
    APP_NAME,
    ON,
)
from src.conf.config import (
    config,
)

from src.app.menus import (
    generate_menu,
)
from src.app.app import (
    WorkDayApp,
)

if __name__ == "__main__":
    app = WorkDayApp(
        icon=APP_ICON,
        name=APP_NAME,
        menu=generate_menu(),
    )
    app.run(
        debug=config.debug_mode == ON,
    )
