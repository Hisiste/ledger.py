import colorama


def date_f(text: str) -> str:
    """Format of the date."""
    return text

def comment_f(text: str) -> str:
    """Format of the transaction's comment."""
    return colorama.Style.BRIGHT + text + colorama.Style.RESET_ALL

def account_f(text: str) -> str:
    """Format of the account's name."""
    return colorama.Fore.BLUE + text + colorama.Style.RESET_ALL

def price_f(text: str) -> str:
    """Format of the price."""
    if '-' in text:
        return colorama.Fore.RED + text + colorama.Style.RESET_ALL
    else:
        return text
