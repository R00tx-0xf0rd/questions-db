class Settings:
    db_name = "database.sqlite"
    db_url = f"sqlite+aiosqlite:///./{db_name}"


settings = Settings()
