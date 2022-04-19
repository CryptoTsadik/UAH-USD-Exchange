import json

with open('balance.json', 'r') as f:
    total_balance = json.loads(f.read())


def command_check() -> str:
    while True:
        commands = input(f"{menu} \nВведите комнаду из списка: ").upper()
        if commands == "COURSE" or commands == "EXCHANGE" or commands == "STOP":
            return commands
        else:
            print("Введите одну из доступных команд: 'COURSE', 'EXCHANGE', 'STOP'")


def currency_check(currencies: dict, command: str) -> str | None:
    while True:
        currency_search = input("Введите название Вашей валюты: ").upper()
        for currency in currencies.keys():
            if currency_search in currencies.keys() and command == "COURSE":
                message_course = f"RATE: {total_balance[currency_search]['exchange_rate']}, " \
                                 f"AVAILABLE: {total_balance[currency_search]['balance']}"
                return message_course
            elif currency_search in currencies.keys() and command == "EXCHANGE":
                return currency_search
            else:
                message_error = str(f"INVALID CURRENCY {currency_search}")
                return message_error


def digits_check(currencies_balances: dict) -> float:
    while True:
        try:
            amount_to_exchange = int(input("Введите количество валюты для обмена:"))
            return float(amount_to_exchange)
        except ValueError as e:
            print(e)


def proper_balance_and_exchange(quote: str, quote_amount: float, currencies_balances: dict):
    if quote == "USD":
        base = "UAH"
        base_amount = quote_amount * currencies_balances[base]["exchange_rate"]
    elif quote == "UAH":
        base = "USD"
        base_amount = quote_amount / currencies_balances[base]["exchange_rate"]
    else:
        return "Какая-то ошибка"
    if currencies_balances[base]["balance"] >= base_amount:
        currencies_balances[quote]["balance"] += quote_amount
        currencies_balances[base]["balance"] -= base_amount
        return print(base, base_amount, "RATE: ", currencies_balances[base]["exchange_rate"])
    else:
        return print(
            f'UNAVAILABLE, REQUIRED BALANCE, {base}: {base_amount}, AVAILABLE: {currencies_balances[base]["balance"]}')


menu = """
1. COURSE USD( UAH) (Получение курса и остатков);
2. EXCHANGE UAH (USD) (обмен)
3. STOP (остановка сервиса)
"""
while True:
    command = command_check()
    if command == "COURSE":
        currency_search = currency_check(total_balance, command = "COURSE")
        print(currency_search)

    elif command == "EXCHANGE":
        currency_to_exchange = currency_check(total_balance, command = "EXCHANGE")
        if not currency_to_exchange.startswith("INVALID CURRENCY"):
            for currency, values in total_balance.items():
                amount_to_exchange = digits_check(total_balance)
                proper_balance_and_exchange(currency_to_exchange, amount_to_exchange, total_balance)
                break
            j_str = json.dumps(total_balance)
            with open('balance.json', 'w') as f:
                f.write(j_str)
        else:
            print(currency_to_exchange)
            continue

    elif command == "STOP":
        exit("Программа остановлена")
