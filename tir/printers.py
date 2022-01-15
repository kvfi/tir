from colorama import Fore


def cprint(color: str, txt: str):
    match color:
        case 'GREEN':
            print(Fore.GREEN + txt)
        case 'RED':
            print(Fore.RED + txt)
        case 'YELLOW':
            print(Fore.YELLOW + txt)
        case _:
            print(txt)
