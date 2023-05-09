from typing import List
from utils.read_file import entry
from utils.register import complete_prices
import re

RE_NOT = r'not ((?:[^()\s]+)|(?:\(.+\)))'
RE_AND = r'((?:[^()\s]+)|(?:\(.+\))) and ((?:[^()\s]+)|(?:\(.+\)))'
RE_OR = r'((?:[^()\s]+)|(?:\(.+\))) or ((?:[^()\s]+)|(?:\(.+\)))'


def clean_pattern(pattern: str):
    pattern = pattern.strip()

    if pattern[0] == '(' and pattern[-1] == ')':
        pattern = pattern[1:-1]

    return pattern


def create_ors(string: str):
    splitted = string.split()
    result = ''

    for left, right in zip(splitted[:-1], splitted[1:]):
        if left not in ['not', 'and', 'or'] and right not in ['and', 'or']:
            result += f'{left} or '
        else:
            result += f'{left} '

    result += splitted[-1]

    return result


def find_logic_patt(pattern: str):
    # First search for the pattern "not {text}"
    patt = re.findall(RE_NOT, pattern)
    if patt:
        return ('not', patt[0])

    # If there wasn't a "not" pattern, try searching for "{text 1} or {text 2}"
    patt = re.findall(RE_OR, pattern)
    if patt:
        return ('or', patt[0])

    # Lastly, try searching for "{text 1} and {text 2}" pattern.
    patt = re.findall(RE_AND, pattern)
    if patt:
        return ('and', patt[0])

    # If there wasn't any pattern, return None.
    return (None, None)


def re_ledger(pattern: str, account_name: str):
    pattern = clean_pattern(pattern)

    if ' ' not in pattern:
        if pattern == '{False}':
            return False
        elif pattern == '{True}':
            return True
        elif re.search(pattern, account_name) is None:
            return False
        else:
            return True
        
    pattern = create_ors(pattern)
    key, patt = find_logic_patt(pattern)

    while key is not None:
        if key == 'not':
            meets_criteria = not re_ledger(patt, account_name)
            pattern = pattern.replace(f'not {patt}', f'{{{meets_criteria}}}')

        elif key == 'or':
            meets_criteria = re_ledger(patt[0], account_name) or re_ledger(patt[1], account_name)
            pattern = pattern.replace(f'{patt[0]} or {patt[1]}', f'{{{meets_criteria}}}')

        elif key == 'and':
            meets_criteria = re_ledger(patt[0], account_name) and re_ledger(patt[1], account_name)
            pattern = pattern.replace(f'{patt[0]} and {patt[1]}', f'{{{meets_criteria}}}')


        key, patt = find_logic_patt(pattern)

    return re_ledger(pattern, account_name)


def filter_accounts(arguments: List[str], my_entries: List[entry]):
    pattern = ' '.join(arguments)
    result = []

    for ent in my_entries:
        complete_prices(ent)

        for trans in ent.transactions:
            if re_ledger(pattern, trans[0]):
                result.append(entry(
                    date=ent.date.strftime('%Y-%m-%d'),
                    comment=ent.comment,
                    transactions=[[trans[0], str(trans[1])]]
                ))

    return result
