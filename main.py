import json
from datetime import datetime
from pathlib import Path


def read_operations(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_executed_operations(operations):
    return [op for op in operations if op.get('state') == 'EXECUTED']


def get_sorted_operations(operations):
    valid_operations = [op for op in operations if 'date' in op]
    return sorted(valid_operations, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)


def mask_card_number(card_info):
    card_name, card_number = card_info.rsplit(' ', 1)
    return f"{card_name} {card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def mask_account_number(account_number):
    return f"Счет **{account_number[-4:]}"


def mask_payment_info(operation):
    date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    description = operation['description']
    from_account = operation.get('from', '')
    to_account = operation.get('to', '')
    amount = f"{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}"

    if from_account and ('Visa' in from_account or 'MasterCard' in from_account):
        from_account = mask_card_number(from_account)
    elif from_account:
        from_account = mask_account_number(from_account)

    if to_account:
        to_account = mask_account_number(to_account)

    return f"{date} {description}\n{from_account} -> {to_account}\n{amount}\n"


def main():
    json_path = Path(__file__).parent / 'json' / 'operations.json'
    operations = read_operations(json_path)

    executed_operations = get_executed_operations(operations)
    sorted_operations = get_sorted_operations(executed_operations)

    if not sorted_operations:
        print("Нет выполненных операций для отображения.")
        return

    for operation in sorted_operations[:5]:
        payment_info = mask_payment_info(operation)
        print(payment_info)


if __name__ == "__main__":
    main()
