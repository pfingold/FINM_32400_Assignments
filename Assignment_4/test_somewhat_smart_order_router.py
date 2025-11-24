"""
Assignment 4, Task 3:

This file contains the required unit tests for Assignment 4 
(a normal order and a corner case) as well as an additional
test to check that an invalid order side raises ValueError

These tests should be runnable via the pytest tool

Classmates Cited: Annie Reynolds
"""
import pytest
from somewhat_smart_order_router import best_price_improvement

def test_best_price_improvement_normal():
    """Test that a normal order returns an exchange (str)
    and price improvement (float)"""

    test_exchange, test_price = best_price_improvement(
        symbol='NVDA',
        side='B',
        quantity=100,
        limit_price=1000,
        bid_price=999,
        ask_price=1001,
        bid_size=500,
        ask_size=300)

    assert isinstance(test_exchange, str) and isinstance(test_price, float)

def test_best_price_improvement_corner_case():
    """Test zero spread case, where bid_price = ask_price = limit_price. Model
    should still return an exchange (str) and price improvement (float)"""

    test_exchange, test_price = best_price_improvement(
        symbol='NVDA',
        side='B',
        quantity=100,
        limit_price=1000,
        bid_price=1000,
        ask_price=1000,
        bid_size=500,
        ask_size=300)

    assert isinstance(test_exchange, str) and isinstance(test_price, float)

def test_best_price_improvement_invalid_side():
    """Test that an order with an invalid side
    (not 'B' or 'S') raises a ValueError"""

    with pytest.raises(ValueError):
        best_price_improvement(
            symbol='NVDA',
            side='Q',
            quantity=100,
            limit_price=1000,
            bid_price=999,
            ask_price=1001,
            bid_size=500,
            ask_size=300)
