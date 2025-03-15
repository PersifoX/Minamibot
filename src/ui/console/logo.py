from colorama import Fore, Style
from pyfiglet import Figlet

logo = Figlet(font="5lineoblique", width=250)


def get_logo():
    return f'{Fore.GREEN}{logo.renderText("MinamiBot")}{Style.RESET_ALL}'
