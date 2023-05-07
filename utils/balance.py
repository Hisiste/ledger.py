from typing import List

from utils.read_file import entry
from utils.register import currencies, complete_prices
from utils.colored_output import *


class tree:
    def __init__(self, name: str, value: currencies = None) -> None:
        self.name = name
        self.value = value
        self.children = []

    
    def compute_value(self):
        if self.value is not None:
            return

        self.value = currencies()
        for child in reversed(self.children):
            child.compute_value()
            for price in child.value:
                self.value.add_money(price)


    def add_child(self, name: str, value: currencies = None):
        self.children.append(tree(name, value))


    def add_value(self, price: str):
        if self.value is None:
            self.value = currencies()

        self.value.add_money(price)


    def get_child_with_name(self, name: str):
        for child in self.children:
            if name == child.name:
                return child

        return None


    def __contains__(self, name: str) -> bool:
        for child in self.children:
            if name == child.name:
                return True
            
        return False

    
    def __str__(self, level=0, ignore_level = False) -> str:
        result = ''
        if not ignore_level:
            for price in self.value:
                result += price_f(f'{price:>20}') + '\n'

            result = result.rstrip()
            result += '  ' + ' '*(2 * level)

        if len(self.children) == 1:
            result += account_f(self.name + ':')
            for child in self.children:
                result += child.__str__(level + 1, ignore_level = True)

        else:
            result += account_f(self.name) + '\n'
            for child in self.children:
                result += child.__str__(level + 1)

        return result


class accounts_tree:
    def __init__(self) -> None:
        self.my_accounts = tree(name='root')

    def add_transaction(self, name_acc: str, price: str):
        search = self.my_accounts

        for name in name_acc.split(':'):
            if name not in search:
                search.add_child(name)

            search = search.get_child_with_name(name)

        search.add_value(price)


    def __str__(self) -> str:
        self.my_accounts.compute_value()

        result = ''
        for child in self.my_accounts.children:
            result += str(child)

        result += '--------------------\n'
        for price in self.my_accounts.value:
            result += price_f(f'{price:>20}') + '\n'

        return result.rstrip()



def print_balance(my_entries: List[entry]):
    my_tree = accounts_tree()

    for ent in my_entries:
        complete_prices(ent)

        for trans in ent.transactions:
            my_tree.add_transaction(trans[0], str(trans[1]))

    print(my_tree)
