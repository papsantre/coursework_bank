import pytest
from main import mask_card_number, mask_account_number, read_operations, get_executed_operations, get_sorted_operations, mask_payment_info
from pathlib import Path
from datetime import datetime

def test_mask_card_number():
    assert mask_card_number("Visa Platinum 7000790061236361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_card_number("MasterCard Gold 1111222233334444") == "MasterCard Gold 1111 22** **** 4444"

def test_mask_account_number():
    assert mask_account_number("96385678") == "Счет **5678"
    assert mask_account_number("87654321") == "Счет **4321"

def test_read_operations():
    json_path = Path(__file__).parent.parent / 'json' / 'operations.json'
    operations = read_operations(json_path)
    assert isinstance(operations, list)
    assert len(operations) > 0

def test_get_executed_operations():
    json_path = Path(__file__).parent.parent / 'json' / 'operations.json'
    operations = read_operations(json_path)
    executed_operations = get_executed_operations(operations)
    assert all(op.get('state') == 'EXECUTED' for op in executed_operations)

def test_get_sorted_operations():
    json_path = Path(__file__).parent.parent / 'json' / 'operations.json'
    operations = read_operations(json_path)
    sorted_operations = get_sorted_operations(operations)
    dates = [datetime.strptime(op['date'], '%Y-%m-%dT%H:%M:%S.%f') for op in sorted_operations]
    assert dates == sorted(dates, reverse=True)

def test_mask_payment_info():
    operation = {
        "date": "2023-05-21T12:34:56.789000",
        "description": "Test transaction",
        "from": "Visa Platinum 7000790061236361",
        "to": "Account 96385678",
        "operationAmount": {
            "amount": "1234.56",
            "currency": {
                "name": "руб."
            }
        }
    }
    masked_info = mask_payment_info(operation)
    expected_info = "21.05.2023 Test transaction\nVisa Platinum 7000 79** **** 6361 -> Счет **5678\n1234.56 руб.\n"
    assert masked_info == expected_info
