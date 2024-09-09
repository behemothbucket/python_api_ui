from pydantic_settings import BaseSettings, SettingsConfigDict


class Driver(BaseSettings):
    headless_enabled: bool = True
    mobile_mode: bool = False
    screenshots_enabled: bool = True
    screenshots_dir: str = ""
    default_timeout: int = 0


class Api(BaseSettings):
    base_url_client_interface: str = ""
    base_url_emulator: str = ""
    base_url_jd_api: str = ""


class TestUser(BaseSettings):
    phone: str = ""
    otp_code: str = ""
    recovery_phone: str = ""
    new_password: str = ""
    sms_code: str = ""
    asp_code: str = ""
    min_age: int = 0
    max_age: int = 0
    min_salary_expenses: int = 0
    max_salary_expenses: int = 0
    max_salary_ie_expenses: int = 0


class Acquiring(BaseSettings):
    default_provider: str = ""
    approve_emulation: str = ""
    alfa_card_pan: str = ""
    tkb_card_pans: str = ""


class Database(BaseSettings):
    host_jm: str = ""
    database_jm: str = ""
    user_jm: str = ""
    password_jm: str = ""
    port_jm: int = 0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="."
    )

    driver: Driver = Driver()
    api: Api = Api()
    acquiring: Acquiring = Acquiring()
    test_user: TestUser = TestUser()
    database: Database = Database()


base_settings = Settings()
