from auth.domain.shared.domain_event import DomainEventAdder
from auth.domain.shared.entity import Entity, EventTrackableEntity
from auth.domain.user.events import PasswordChanged, RoleChanged, UserHiddenOrRevealed
from auth.domain.user.role_enum import RoleEnum
from auth.domain.user.value_objects import Login, Role, UserId


class User(Entity[UserId], EventTrackableEntity):
    """Сущность пользователя."""

    def __init__(
        self,
        user_id: UserId,
        event_adder: DomainEventAdder,
        *,
        login: Login,
        hash_password: bytes,
        hidden: bool,
        role: Role,
        organization_name: str | None,
    ) -> None:
        Entity.__init__(self, entity_id=user_id)
        EventTrackableEntity.__init__(self, event_adder=event_adder)

        self._login = login
        self._hash_password = hash_password
        self._hidden = hidden
        self._role = role
        self._organization_name = organization_name

    def edit(self, role: Role) -> None:
        """Редактировать сущность пользователя."""
        if role.name == self.role_name and role.extended == self.role_extended:
            return
        self._role = role

        self.track_event(
            event=RoleChanged(
                user_id=self.entity_id,
                role_name=self.role_name,
                role_extended=self.role_extended,
            )
        )

    def change_password(self, hash_password: bytes) -> None:
        """Смена пароля у сущности пользователя."""
        self._hash_password = hash_password

        self.track_event(
            event=PasswordChanged(
                user_id=self.entity_id, hash_password=self._hash_password
            )
        )

    def hide_or_reveal(self, hidden: bool) -> None:
        """Скрыть (деактивировать) пользователя либо раскрыть его (активировать)."""
        if self.hidden == hidden:
            return
        self._hidden = hidden

        self.track_event(
            event=UserHiddenOrRevealed(user_id=self.entity_id, hidden=self._hidden)
        )

    @property
    def login_vo(self) -> Login:
        return self._login

    @property
    def hash_password(self) -> bytes:
        return self._hash_password

    @property
    def hidden(self) -> bool:
        return self._hidden

    @property
    def role_vo(self) -> Role:
        return self._role

    @property
    def role_name(self) -> str:
        return self._role.name

    @property
    def role_extended(self) -> bool:
        return self._role.extended

    @property
    def role_level(self) -> int:
        return RoleEnum[self.role_name].level

    @property
    def organization_name(self) -> str | None:
        return self._organization_name
