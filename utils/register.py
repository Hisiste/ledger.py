from utils.read_file import entry
from typing import List, Iterator

import re
import shutil
import colorama

def date_f(text: str):
    return text

def comment_f(text: str):
    return colorama.Style.BRIGHT + text + colorama.Style.RESET_ALL

def account_f(text: str):
    return colorama.Fore.BLUE + text + colorama.Style.RESET_ALL

def price_f(text: str):
    if '-' in text:
        return colorama.Fore.RED + text + colorama.Style.RESET_ALL
    else:
        return text


class currencies:
    """
    Store various currencies and add or subtract them.
    """
    def __init__(self) -> None:
        # The keys of the dictionary will be the currency symbol. The value of
        # the dictionary will be a float number, representing the amount.
        self.money = dict()


    def __retrieve_number(self, price: str) -> float:
        """
        Given a string, extract the number from it. The number is defined by a
        consecutive string of digits, with maybe a dot in between or end of it.
        """
        result = re.findall(r'\d+(?:\.\d*)?', price)[0]
        result = float(result)

        # If it has the minus symbol (-), it must be a negative value.
        if '-' in price:
            return -result
        else:
            return result

    def __retrieve_currency(self, price: str) -> str:
        """
        Given a string, remove the number and maybe a negative symbol from it.
        The resulting string is most likely the currency symbol.
        """
        number = re.findall(r'\d+(?:\.\d*)?', price)[0]
        result = price.replace(number, '')
        result = result.replace('-', '')

        return result.strip()

    
    def add_money(self, price: str) -> None:
        """
        Add money to our "wallet." If it is a currency we already have, sum the
        values. If the currency is new, create the entry on our dictionary and
        assign the amount to it.

        On the other hand, if the amount is equal to 0, delete the currency
        entry.
        """
        number = self.__retrieve_number(price)
        currency = self.__retrieve_currency(price)

        if currency in self.money:
            self.money[currency] += number
        else:
            self.money[currency] = number

        if self.money[currency] == 0:
            del self.money[currency]

    
    def __iter__(self) -> Iterator[str]:
        """
        When iterating through our currencies, yield the already formatted
        currencies. If there are not currencies, just return a 0.
        """
        if not self.money:
            yield '0'
        for currency, amount in self.money.items():
            if len(currency) == 1:
                yield f'{currency}{amount:.02f}'
            else:
                yield f'{amount:.02f} {currency}'


    # What to do if we do "-currencies"?
    def __neg__(self):
        negated = currencies()
        for currency, number in self.money.items():
            negated.add_money(f'{currency} {-number}')

        return negated


    def __lt__(self, other):
        if len(self.money.values()) != 1 or len(other.money.values()) != 1:
            raise Exception('Cannot compare multiple currencies at once!')

        for amount_left in self.money.values():
            break
        for amount_right in other.money.values():
            break

        return amount_left < amount_right


    def __str__(self) -> str:
        if len(self.money.items()) != 1:
            raise Exception('Cannot convert to string more than one currency!')

        for currency, amount in self.money.items():
            if len(currency) == 1:
                return f'{currency}{amount:.02f}'
            else:
                return f'{amount:.02f} {currency}'


def complete_prices(my_entry: entry):
    """
    Transform all string of prices to the class `currencies`. If there is an
    entry that has no price, balance the transaction so the sum is equal to 0.
    """
    idx_not_complete = -1
    money_to_bal = currencies()

    for idx in range(len(my_entry.transactions)):
        if (len(my_entry.transactions[idx]) == 1):
            idx_not_complete = idx
        else:
            _, price = my_entry.transactions[idx]
            money_to_bal.add_money(price)

            new_price_format = currencies()
            new_price_format.add_money(price)
            my_entry.transactions[idx][1] = new_price_format

    if idx_not_complete != -1:
        my_entry.transactions[idx_not_complete].append(
            -money_to_bal
        )


def print_register(entries: List[entry]):
    width_term, _ = shutil.get_terminal_size(fallback=(80, 24))
    # We will divide the terminal width in the following way:
    # - Date and Comment: 37/100 parts of the terminal width.
    # - Account name: 31/100 parts of the terminal width.
    # - First price column: 16/100 parts of the terminal width.
    # - Second price column: 16/100 parts of the terminal width.
    # NOTE: We reserve 3 spaces of the terminal width to help separate the
    # columns.
    d_c_len = int((width_term - 3) * 37 / 100); d_c_len = max(d_c_len, 15)
    acc_len = int((width_term - 3) * 31 / 100); acc_len = max(acc_len, 6)
    p_1_len = int((width_term - 3) * 16 / 100)
    p_2_len = int((width_term - 3) * 16 / 100)

    result = ''
    current_money = currencies()

    for ent in entries:
        complete_prices(ent)

        date = date_f(ent.date.strftime('%y-%b-%d '))
        result += date

        comment = ent.comment
        if len(date) + len(comment) > d_c_len:
            comment = comment[:d_c_len - len(date) - 2] + '..'

        result += comment_f(f'{comment:<{d_c_len - len(date)}} ')

        for trans in ent.transactions:
            account = trans[0]
            if len(account) > acc_len:
                account = '..' + account[-(acc_len - 2):]

            result += account_f(f'{account:<{acc_len}} ')

            for price in trans[1]:
                result += price_f(f'{price:>{p_1_len}} ')

                current_money.add_money(price)
                for curr_price in current_money:
                    result += price_f(f'{curr_price:>{p_2_len}}') + '\n'
                    result += ' ' * (d_c_len + 1 + acc_len + 1 + p_1_len + 1)

                result = result.rstrip() + '\n'
                result += ' ' * (d_c_len + 1 + acc_len + 1)

            result = result.rstrip() + '\n'
            result += ' ' * (d_c_len + 1)

        result = result.rstrip() + '\n'

    print(result.rstrip())
