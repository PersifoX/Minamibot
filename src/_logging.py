import logging

from colorama import Fore, Style


class CustomFormatter(logging.Formatter):
    """Custom formatter for the logger"""

    format = "[{asctime}] [{levelname:<8}] {name}: {message} ({filename}:{lineno})"
    dt_fmt = "%Y-%m-%d %H:%M:%S"

    FORMATS = {
        logging.DEBUG: Fore.CYAN + format + Style.RESET_ALL,
        logging.INFO: Fore.BLUE + format + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + format + Style.RESET_ALL,
        logging.ERROR: Fore.RED + format + Style.RESET_ALL,
        logging.CRITICAL: Fore.LIGHTRED_EX + format + Style.RESET_ALL,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.dt_fmt, style="{")
        return formatter.format(record)


def get_logger(name, lvl=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(lvl)

    ch = logging.StreamHandler()
    ch.setLevel(lvl)

    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)

    return logger
