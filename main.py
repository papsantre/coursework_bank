import json
from datetime import datetime


# Функция для маскирования номера карты
def mask_card_number(card_number):
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


# Функция для маскирования номера счета
def mask_account_number(account_number):
    return f"**{account_number[-4:]}"


def main():
    # Чтение файла JSON
    with open('json/operations.json', 'r', encoding='utf-8') as file:
        operations = json.load(file)

    # Фильтрация и сортировка операций
    executed_operations = [op for op in operations if op.get('state') == 'EXECUTED']
    sorted_operations = sorted(executed_operations, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'),
                               reverse=True)

    # Вывод последних 5 операций
    for op in sorted_operations[:5]:
        date = datetime.strptime(op['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
        description = op['description']
        from_account = op.get('from', '')
        to_account = op.get('to', '')
        amount = f"{op['operationAmount']['amount']} {op['operationAmount']['currency']['name']}"

        if 'Visa' in from_account or 'MasterCard' in from_account:
            from_account = mask_card_number(from_account)
        elif from_account:
            from_account = mask_account_number(from_account)

        if to_account:
            to_account = mask_account_number(to_account)

        print(f"{date} {description}\n{from_account} -> {to_account}\n{amount}\n")

    # В случае отсутствия операций или других проблем выводим сообщение
    if not sorted_operations:
        print("Нет выполненных операций для отображения.")


if __name__ == "__main__":
    main()