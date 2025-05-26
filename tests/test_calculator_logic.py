import sys
import os

# Adjust the path to import calculator.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculator import calculator

def test_add_positive():
    result = calculator(215, 90, ['add'])
    assert result['add'] > 0, "Add result should be positive"

def test_subtract_positive():
    result = calculator(100, 70, ['subtract'])
    assert result['subtract'] > 0, "Subtract result should be positive"

def test_divide_greater_equal_one():
    result = calculator(60, 20, ['divide'])
    assert isinstance(result['divide'], (int, float)), "Divide result should be a number"
    assert result['divide'] >= 1, "Divide result should be >= 1"

if __name__ == "__main__":
    test_add_positive()
    test_subtract_positive()
    test_divide_greater_equal_one()
    print("All tests passed!")
