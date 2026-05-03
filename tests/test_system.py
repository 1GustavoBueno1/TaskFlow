from Services.system import System
def test_login():
    s = System()
    ok, msg = s.login("a@b.com", "123")
    assert ok is False
