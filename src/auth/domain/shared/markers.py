from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    """Маркер уведомления событий."""
