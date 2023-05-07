from utils.read_file import entry
from typing import List
from utils.register import complete_prices


def separate_currencies(my_entries: List[entry]):
    """
    Given a list of entries with just one transaction, group entries with
    respect to their currencies symbols.
    """
    seen_curr = set()
    list_curr = []

    # First search for every currency we can find in `my_entries`.
    for ent in my_entries:
        for trans in ent.transactions:
            wallet = trans[1]

            if len(wallet.money.keys()) != 1:
                raise Exception('Cannot compare more than one currency at a time.')

            for curr in wallet.money.keys():
                break

            if curr not in seen_curr:
                seen_curr.add(curr)
                list_curr.append(curr)

    # Now group each currency. Select a currency and append entries that have
    # that specific currency. Then select the next seen currency and so on.
    result = []
    for my_currency in list_curr:
        for ent in my_entries:
            wallet = ent.transactions[0][1]

            for curr in wallet.money.keys():
                break

            if my_currency == curr:
                result.append(ent)

    return result


def join_concurrent_entries(my_entries: List[entry]):
    result = []
    for ent in my_entries:
        if len(result) == 0:
            result.append(ent)

        elif ent.comment == result[-1].comment and ent.date == result[-1].date:
            result[-1].transactions.append(
                ent.transactions[0]
            )

        else:
            result.append(ent)

    return result


def sort_by_date(my_entries: List[entry]):
    my_entries.sort(key=lambda x: x.date)


def sort_by_amount(my_entries: List[entry]):
    """
    We have to break entries by their transactions. Then we can sort the
    entries by their amount in their unique transaction.
    """

    # Break entries for them to have only one transaction.
    result = []
    for ent in my_entries:
        complete_prices(ent)

        for trans in ent.transactions:
            result.append(
                entry(
                    date=ent.date.strftime('%Y/%m/%d'),
                    comment=ent.comment,
                    transactions=[trans]
                )
            )
    # Sort each transaction given the amount value.
    result.sort(key=lambda x: x.transactions[0][1])
    # Separate different currencies from each other.
    result = separate_currencies(result)
    # Join concurrent entries if they have the same comment and date.
    result = join_concurrent_entries(result)

    # Hacky way of modifying the original `my_entries` list.
    while my_entries:
        my_entries.pop()
    for item in result:
        my_entries.append(item)

    # Each transaction now has the `currencies` class format. Convert all of
    # them into strings.
    for ent in my_entries:
        for trans in ent.transactions:
            for price in trans[1]:
                break

            trans[1] = price


def sort_entries(my_entries: List[entry], rule: str) -> None:
    """
    Sort the list of entries in-place. This function returns None, the list
    given as a parameter will be modified.
    """
    # Sort by date.
    if rule.lower() in ['d', 'date']:
        sort_by_date(my_entries)
    # Sort by amount.
    if rule.lower() in ['a', 'amount']:
        sort_by_amount(my_entries)
