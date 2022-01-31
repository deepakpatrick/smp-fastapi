import pytest
from app.calculations import add, subtract, multiply, division, BankAccount, InsufficientFunds



@pytest.mark.parametrize("num1, num2, expected_value", [
    (3, 2, 5),
    (7,3,10),
    (12,4,16)
])
def test_add(num1, num2, expected_value):
    print('testing add function')    
    assert add(num1,num2) == expected_value

def test_subtract():
    print('testing subtract function')
    assert subtract(5,3) == 2

def test_multiply():
    print('testing multiply function')
    assert multiply(4,3) == 12

def test_division():
    print('testing divide function')
    assert round(division(7,3),2) == 2.33

def test_deposit():
    ba = BankAccount(100)
    ba.deposit(50)
    assert  ba.balance == 150

def test_withdraw():
    ba = BankAccount(50)
    ba.withdraw(20)
    assert ba.balance == 30

def test_collect_interest():
    ba = BankAccount(50)
    ba.collect_interest(.01)
    assert ba.balance == 50.5


@pytest.fixture
def bank_account():
    print('creating bank account')
    return BankAccount(50)

@pytest.fixture
def zero_bank_account():
    return BankAccount()

def test_deposit1(bank_account):    
    bank_account.deposit(150)
    assert  bank_account.balance == 200

def test_withdraw1(bank_account):
    
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_collect_interest1(bank_account):
    
    bank_account.collect_interest(.01)
    assert bank_account.balance == 50.5

@pytest.mark.parametrize("d,w,i,b",[
    (50,10,.05,42),
    (100,30,.01,70.7),
])
def test_transaction(zero_bank_account,d,w,i,b):
    zero_bank_account.deposit(d)
    zero_bank_account.withdraw(w)
    zero_bank_account.collect_interest(i)
    assert zero_bank_account.balance == b


def test_transaction_negative(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)