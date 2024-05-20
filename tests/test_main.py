import pytest
from main import mask_card_number, mask_account_number

def test_mask_card_number():
    assert mask_card_number("1234567812345678") == "1234 56** **** 5678"

def test_mask_account_number():
    assert mask_account_number("12345678") == "**5678"