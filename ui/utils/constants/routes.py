from enum import Enum


class UIRoutes(str, Enum):
    BASE_URL = "***"
    LOGIN_PAGE = "***"
    LK_PAGE = "***"
    PROFILE_PAGE = "***"
    PASSPORT_PAGE = "***"
    JOB_PAGE = "***"
    RECOVERY_PAGE_BASE = "***"

    def __str__(self) -> str:
        return self.value
