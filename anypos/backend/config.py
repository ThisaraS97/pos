import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App Config
    APP_NAME: str = os.getenv("APP_NAME", "AnyPos")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./anypos.db"
    )
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # Company Info (for branding)
    COMPANY_NAME: str = "AnyPos"
    COMPANY_ADDRESS: str = ""
    COMPANY_PHONE: str = ""
    COMPANY_EMAIL: str = ""
    COMPANY_TAX_ID: str = ""
    
    # Cash Drawer Settings
    AUTO_OPEN_CASH_DRAWER: bool = os.getenv("AUTO_OPEN_CASH_DRAWER", "True") == "True"
    OPEN_DRAWER_FOR_CASH_ONLY: bool = os.getenv("OPEN_DRAWER_FOR_CASH_ONLY", "True") == "True"

settings = Settings()
