from colorama import Fore


def cprint(color: str, txt: str):
    if color == 'GREEN':
        print(Fore.GREEN + txt)
    elif color == 'RED':
        print(Fore.RED + txt)
    elif color == 'YELLOW':
        print(Fore.YELLOW + txt)
    else:
        print(txt)
