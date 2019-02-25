from .session import Session
from .asyncsession import AsyncSession


def create_session(host_address, handler=None, is_async=None):
    session_type = AsyncSession if is_async else Session
    session = session_type(host_address, auth_handler=handler)
    return session
