from unittest.mock import patch

with patch('Services.system.UserRepository'), \
    patch('Services.system.Interface'), \
    patch('Services.system.SaveLog'):
    from Services.system import System
s =  System()

def test_valid_gmail():
    assert s.check_gmail("Usuario@gmail.com") == "Usuario@gmail.com"
def test_not_gmail():
    assert s.check_gmail("notgmail@hotmail.com") is False
def test_invalid_gmail():
    assert s.check_gmail("not.com@gmail") is False
def test_empyt_gmail():
    assert s.check_gmail("") is False
