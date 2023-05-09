# Ledger.py

A simple implementation of [ledger-cli](https://github.com/ledger/ledger). This
implementation only covers a few commands of the original ledger-cli. This
project is only for educational purposes. It does not provide any advantages
over the original project.

# Usage

You can use this program as if it was the original **ledger-cli**, but with a
selected group of flags and commands:
```
./ledger.py [-h] [-v] [-S value-expression] [--price-db FILE] [-f FILE] Action [Action ...]
```

- `-h`: Displays the usage and description of the program.
- `-v`: Displays the current version of the program.
- `-S` or `--sort`: Sorts the entries. See the [`--sort` section](#sort) for
  more details.
- `--price-db`: Currently it has no purpose. See the [`--price-db`
  section](#price-db) for more details.
- `-f` or `--file`: Use the specified file as an input.
- `Action`: The first word will be our *verb*. The *verb* describes what our
  program will output. It currently can be `register`, `balance` or `print`.

  The following words will be our *filters* for which accounts we'll work with.
  See the [filters section](#filters) for more details.

Let's see this commands in more detail.


# Filters

Filters can be applied to just see a subset of all of our accounts. To use
filters, we'll start by describing our keywords:

### And

```
{x} and {y}
```

This way, we can filter accounts if they have the text `{x}` and `{y}` in them.

> Examples:
> 
> ```
> Expenses and Amazon
> ```
> ```
> Income and Job and Encora
> ```

### Or

```
{x} or {y}
```
```
{x} {y}
```

Both ways work. We can filter accounts if they have either `{x}` or `{y}`.

> Examples:
> ```
> Assets Liabilities
> ```
> ```
> Assets and (Bank or Wallet)
> ```

### Not

```
not {x}
```

Filter accounts that DO NOT have `{x}` in them.

> Examples:
> ```
> (Liabilities and not Rent) or Expenses
> ```
> ```
> Expenses and not (Drinks or Food)
> ```

### Regex

As you've just read. Every word is treated as a regex. For this project, we are
using [Python's regex](https://docs.python.org/3/library/re.html). Feel free to
experiment with this function. The only restriction is to not use spaces, as
they are our limiters for keywords and such.

> Examples:
> ```
> Income and [^:]+:[^:]+:[^:]+
> ```
> ```
> ^Expenses and not .*tion$
> ```

~~Sorry for my poor examples. I don't know about finances. ;-;~~


# `--file`

This flag can be used multiple times. It indicates the ledger file(s) we will be
working on. ~~If no file is specified, the program will read from standard input
(`stdin`).~~ ***NOT YET IMPLEMENTED.***


# `--sort`

**The `--sort` flag will always sort in ascending order.** We can sort our
entries in two different ways:

- `date` or `d`: Sort every entry given the date of the transaction.
- `amount` or `a`: Sort given the amount of the transaction. **This breaks
  entries into individual transactions.**

## It doesn't work on `balance`

The `--sort` flag will only make changes on the outputs of `register` and
`print`. The verb `balance` will **always** print in alphabetical order.


# `--price-db`

It points to the file that contains our prices history.

## It doesn't work well alone

The original flag for `--price-db` is commonly used alongside other flags such
as `-V` or `--market`, that uses the prices history to convert all amounts into
our default currency. That's why currently this command doesn't have any
function to it. It's yet to know how we will work with this flag.


# Examples

```
$ ./ledger.py -f index.ledger -S d register Bank  
11-Nov-21 Payment for hard.. Bank:Paypal                  $350.00      $350.00
12-Jul-01 Partial payment .. Bank:Paypal                  $100.00      $450.00
12-Nov-16 Sold some bitcoins Bank:Paypal                   $42.21      $492.21
12-Nov-29 Purchased bitcoins Bank:Paypal                 $-300.00      $192.21
```

```
$ ./ledger.py -f index.ledger --sort a print .\*coin  # In ZSH, the `*` must be escaped.
2013/02/20 Purchased reddit gold for the year
    Asset:Bitcoin Wallet                  -10.00 BTC

2012/11/16 Sold some bitcoins
    Asset:Bitcoin Wallet                   -3.50 BTC

2012/11/29 Purchased bitcoins
    Asset:Bitcoin Wallet                   15.00 BTC
```

```
$ ./ledger.py --file index.ledger bal Bank: Expense:
             $192.21  Bank:Paypal
           10.00 BTC
              $10.00  Expense
              $10.00    Favor
           10.00 BTC    Web Services:Reddit
--------------------
           10.00 BTC
             $202.21
```
