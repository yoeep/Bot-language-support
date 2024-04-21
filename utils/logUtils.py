import logging
import sys
from datetime import datetime

def setup_logger(log_file=None):
    """设置日志记录器"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)


    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger

def info(msg):
    logger = setup_logger()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stack = sys._getframe(0)

    info_msg = f"[INFO] {timestamp} - {stack.f_code.co_filename}:{sys._getframe(0).f_lineno} {msg}"
    logger.info(info_msg)

def error(msg):
    logger = setup_logger()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stack = sys._getframe(0)

    info_msg = f"[ERROR] {timestamp} - {stack.f_code.co_filename}:{sys._getframe(0).f_lineno} {msg}"
    logger.error(info_msg)

def dubug(msg):
    logger = setup_logger()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stack = sys._getframe(0)

    info_msg = f"[DEBUG] {timestamp} - {stack.f_code.co_filename}:{sys._getframe(0).f_lineno} {msg}"
    logger.debug(info_msg)

if __name__ == "__main__":
    info("info")
