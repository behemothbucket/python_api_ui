from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from settings.base import base_settings

driver_settings = base_settings.driver


class DriverConfig(BaseSettings):
    """
    Конфигурация драйвера.

    Атрибуты:
        headless_mode (bool): Режим безголового браузера.
        mobile_mode (bool): Мобильный режим.
        desktop_device (str): Устройство для десктопа.
        mobile_device (str): Устройство для мобильного.
    """

    headless_mode: bool = driver_settings.headless_enabled
    mobile_mode: bool = driver_settings.mobile_mode
    desktop_device: str = "Desktop Chrome"
    mobile_device: str = "Iphone 14"  # TODO сделать больше


class LoggingConfig(BaseSettings):
    """
    Конфигурация логирования.

    Атрибуты:
        screenshots_enabled (bool): Включены ли скриншоты.
        screenshots_dir (str): Директория для скриншотов.
    """

    screenshots_enabled: bool = driver_settings.screenshots_enabled
    screenshots_dir: str = driver_settings.screenshots_dir


class ViewportConfig(BaseModel):
    """
    Конфигурация области просмотра.

    Атрибуты:
        width (int): Ширина области просмотра.
        height (int): Высота области просмотра.
    """

    width: int = 1920
    height: int = 1080


class UIConfig(BaseSettings):
    """
    Конфигурация пользовательского интерфейса.

    Атрибуты:
        driver (DriverConfig): Конфигурация драйвера.
        logging (LoggingConfig): Конфигурация логирования.
        viewport (ViewportConfig): Конфигурация области просмотра.
    """

    driver: DriverConfig = DriverConfig()
    logging: LoggingConfig = LoggingConfig()
    viewport: ViewportConfig = ViewportConfig()


@lru_cache()
def get_ui_config() -> UIConfig:
    """
    Получить конфигурацию пользовательского интерфейса с использованием кэша.

    Возвращает:
        UIConfig: Конфигурация пользовательского интерфейса.
    """
    return UIConfig()
