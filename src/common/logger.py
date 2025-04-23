import os
import sys
from loguru import logger
from conf.config import settings


# 日志文件路径
log_path = settings.LOG_PATH
if not os.path.exists(log_path):
    os.mkdir(log_path)

# 日志文件
log_file = os.path.join(log_path, "{time:YYYY-MM-DD}.log")

# 配置日志
logger.remove()  # 移除默认处理器

# 添加控制台输出
logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL,  # 默认使用 DEBUG 级别
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
)

# 添加文件输出
logger.add(
    log_file,
    level=settings.LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="00:00",  # 每天零点创建新文件
    retention="30 days",  # 保留30天的日志
    compression="zip",  # 压缩历史日志
    encoding="utf-8",
)

# 确保导出 logger 对象
__all__ = ["logger"] 