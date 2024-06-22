import logging

import betterlogging as bl


def setup_logging():
    logging.getLogger(__name__)
    bl.basic_colorized_config(level=logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
