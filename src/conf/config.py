import pathlib
from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    # 基本配置
    DESC: str = "RPA API 服务"
    VERSION: str = "0.1.0"
    LOG_LEVEL: str = "DEBUG"
    PORT: int = 5000  # 默认端口

    # 项目路径
    PROJECT_PATH: pathlib.Path = pathlib.Path(__file__).parent.parent
    LOG_PATH: pathlib.Path = PROJECT_PATH / "logs"  # 日志路径

    # 静态文件
    STATIC_FILE: bool = True
    STATIC_PATH: pathlib.Path = PROJECT_PATH / "static"

    # MySQL配置
    MYSQL_ENGINE: str = "mysql"
    MYSQL_ECHO: bool = True  # 是否显示SQL语句
    MYSQL_HOST: str = "192.168.24.132"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "db@24132"
    MYSQL_DATABASE: str = "fd_plateform"
    MYSQL_ENCODING: str = 'utf8mb4'
    MYSQL_ADD_EXCEPTION_HANDLERS: bool = True  # 是否添加异常处理器

    # ORM
    GENERATE_SCHEMAS: bool = False # 是否生成数据库架构, 生产环境关闭
    
    # Redis配置
    REDIS_HOST: str = "172.19.188.206"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["*"]  # 允许的跨域请求来源，默认允许所有来源
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )

@lru_cache
def get_settings():
    """ 缓存配置 """
    return Settings()


settings = Settings()