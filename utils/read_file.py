from datetime import date, datetime
import re
import os


VALID_DATES_FORMAT = r'\d{4}[-./]\d{1,2}[-./]\d{1,2}'
VALID_DATES_SEP = '[-./]'


class entry:
    def __init__(self, date: str, comment: str, transactions: list) -> None:
        self.date = self.__date_from_str(date)
        self.comment = comment
        self.transactions = transactions


    def __date_from_str(self, date_str: str):
        """
        Searches for a valid date on a string and transforms it into ISO
        format. (YYYY-MM-DD)
        """
        my_date = re.findall(VALID_DATES_FORMAT, date_str)[0]
        year, month, day = re.split(VALID_DATES_SEP, my_date)

        return datetime.fromisoformat(f'{int(year)}-{int(month):02}-{int(day):02}')

    
    def __str_to_price_format(self, price: str):
        # Find the first instance of a number. A string of digits that may have
        # a dot and more digits after.
        price_nu = re.findall(r'\d+(?:\.\d*)?', price)[0]
        # For the currency symbol, we get rid of the number.
        price_sy = price.replace(price_nu, '')

        if '-' in price:
            # If there was a minus (-), add it to the number and delete it from
            # the currency symbol.
            price_nu = f"-{price_nu}"
            price_sy = price_sy.replace('-', '')

        # Remove the whitespace around the currency symbol.
        price_sy = price_sy.strip()

        # If the symbol is 1 character long, write it on the left.
        if len(price_sy) == 1:
            return f"{price_sy}{float(price_nu):.02f}"
        # If it is longer than 1 character, write it on the right.
        else:
            return f"{float(price_nu):.02f} {price_sy}"


    def __str__(self) -> str:
        result = self.date.strftime('%Y/%m/%d')
        result += " " + self.comment + "\n"

        for trans in self.transactions:
            if len(trans) == 2:
                account, price = trans
                price = self.__str_to_price_format(price)
            else:
                account = trans[0]
                price = ""

            result += f"    {account:<35} {price:>12}\n"

        return result


def give_me_file_contents(path: str):
    line_comments = ";#%|*"
    try:
        with open(path, 'r', encoding='utf8') as fp:
            result = fp.readlines()

            for line in result:
                # If line is just empty spaces or empty, ignore it.
                if len(line.lstrip()) == 0:
                    continue

                # If first character of line is a line comment, ignore it.
                first_char = line.lstrip()[0]
                if first_char in line_comments:
                    continue

                yield line.strip()
    
    except:
        raise Exception(f"Error while trying to read {path} file.")


def is_new_entry(line: str):
    """
    Returns `True` if the line contains at least one valid date. This means
    we're looking at a new transaction.
    """
    return re.search(VALID_DATES_FORMAT, line) is not None


def read_ledger(path: str):
    files_to_read = [path]
    date = None
    comment = None
    transactions = None

    results = []

    while files_to_read:
        current_file = files_to_read.pop()

        for line in give_me_file_contents(current_file):
            if line.startswith('!include'):
                file_path = line.split()[-1]
                base_dir = os.path.dirname(current_file)
                files_to_read.insert(0,
                    os.path.join(base_dir, file_path)
                )

                continue

            if is_new_entry(line) and date is not None:
                results.append(
                    entry(date, comment, transactions)
                )

            if is_new_entry(line):
                date, comment = line.split(maxsplit=1)
                transactions = []
            else:
                # The line is a new transaction
                tabs_to_spaces = line.replace('\t', '    ')
                transactions.append(
                    re.split(r'\s{2,}', tabs_to_spaces)
                )

        if date is not None:
            results.append(
                entry(date, comment, transactions)
            )
            date = None
            comment = None
            transactions = None

    return results
