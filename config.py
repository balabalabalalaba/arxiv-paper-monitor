import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 邮箱配置
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
    
    # === 新增：时间限制变量 ===
    # 优先从环境变量读取，默认为 1 天。如果设为 0 则表示无时间限制。
    FETCH_DAYS = int(os.getenv("FETCH_DAYS", 1))
    
    # Arxiv配置
    _env_keywords = os.getenv("SEARCH_KEYWORDS")
    if _env_keywords:
        SEARCH_KEYWORDS = [kw.strip().strip('"').strip("'") for kw in _env_keywords.split(",")]
    else:
        SEARCH_KEYWORDS = [
            "Rydberg atom",
            "magneto-optical trap",
            "optical tweezers",
            "nanophotonics"
        ]
        
    MAX_RESULTS = int(os.getenv("MAX_RESULTS", 50))

    # arXiv 分区过滤，逗号分隔，留空表示不限制分区
    _env_categories = os.getenv("SEARCH_CATEGORIES")
    if _env_categories:
        SEARCH_CATEGORIES = [cat.strip() for cat in _env_categories.split(",") if cat.strip()]
    else:
        SEARCH_CATEGORIES = []
    
    # 定时任务配置
    SCHEDULE_TIME = "09:00"  
    TEST_MODE = False  
    
    # 日志配置
    LOG_FILE = "logs/arxiv_digest.log"
    
    @classmethod
    def validate(cls):
        if not cls.EMAIL_SENDER or not cls.EMAIL_PASSWORD:
            raise ValueError("邮箱配置不完整，请检查 .env 文件或 GitHub Secrets")
        return True
