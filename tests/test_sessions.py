from core.session_manager import create_session, is_session_active

def test_session():
    create_session("AA:BB:CC:DD:EE:FF", "0712345678", 60)
    assert is_session_active("AA:BB:CC:DD:EE:FF") == True