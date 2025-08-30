from typing import TypedDict

from auth.domain.session.session_id import SessionId
from auth.domain.user.value_objects import UserId


class UserSpecifications(TypedDict, total=False):
    user_id: UserId
    exists_session_id: SessionId
