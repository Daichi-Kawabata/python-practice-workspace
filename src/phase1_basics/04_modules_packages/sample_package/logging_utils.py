"""
logging_utils.py - ログ関連のユーティリティ

アプリケーションでのログ管理を簡単にするためのクラス
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum

class LogLevel(Enum):
    """ログレベル列挙型"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class Logger:
    """カスタムロガークラス"""
    
    def __init__(self, 
                 name: str,
                 level: LogLevel = LogLevel.INFO,
                 log_file: Optional[str] = None,
                 console_output: bool = True):
        """
        ロガーを初期化
        
        Args:
            name: ロガー名
            level: ログレベル
            log_file: ログファイルパス（Noneの場合はファイル出力なし）
            console_output: コンソール出力の有無
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level.value)
        
        # 既存のハンドラをクリア
        self.logger.handlers.clear()
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # コンソール出力
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # ファイル出力
        if log_file:
            # ログディレクトリを作成
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """デバッグログ"""
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """情報ログ"""
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """警告ログ"""
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """エラーログ"""
        self._log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """重大ログ"""
        self._log(LogLevel.CRITICAL, message, **kwargs)
    
    def _log(self, level: LogLevel, message: str, **kwargs: Any) -> None:
        """内部ログメソッド"""
        # 追加情報があれば含める
        if kwargs:
            extra_info = " | ".join(f"{k}={v}" for k, v in kwargs.items())
            message = f"{message} | {extra_info}"
        
        self.logger.log(level.value, message)
    
    def log_function_call(self, func_name: str, args: tuple = (), kwargs: Optional[dict] = None) -> None:
        """関数呼び出しをログに記録"""
        kwargs = kwargs or {}
        args_str = ", ".join(str(arg) for arg in args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        
        all_args = []
        if args_str:
            all_args.append(args_str)
        if kwargs_str:
            all_args.append(kwargs_str)
        
        args_display = "(" + ", ".join(all_args) + ")"
        self.info(f"Function called: {func_name}{args_display}")
    
    def log_performance(self, operation: str, duration: float, **kwargs: Any) -> None:
        """パフォーマンス情報をログに記録"""
        self.info(f"Performance: {operation} completed in {duration:.4f}s", **kwargs)

class PerformanceLogger:
    """パフォーマンス測定用のコンテキストマネージャー"""
    
    def __init__(self, logger: Logger, operation: str, **kwargs: Any):
        self.logger = logger
        self.operation = operation
        self.kwargs = kwargs
        self.start_time: Optional[float] = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        self.logger.debug(f"Starting operation: {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        if self.start_time:
            duration = time.time() - self.start_time
            if exc_type is None:
                self.logger.log_performance(self.operation, duration, **self.kwargs)
            else:
                self.logger.error(f"Operation failed: {self.operation} (duration: {duration:.4f}s)")
        return False

def get_default_logger(name: str = "app") -> Logger:
    """デフォルトロガーを取得"""
    return Logger(name)

def setup_application_logging(
    app_name: str,
    log_level: LogLevel = LogLevel.INFO,
    log_dir: str = "logs"
) -> Logger:
    """アプリケーション用のログ設定"""
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = f"{log_dir}/{app_name}_{timestamp}.log"
    
    return Logger(
        name=app_name,
        level=log_level,
        log_file=log_file,
        console_output=True
    )

# ログデコレータ
def logged(logger: Optional[Logger] = None):
    """関数呼び出しをログに記録するデコレータ"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = get_default_logger()
            
            logger.log_function_call(func.__name__, args, kwargs)
            
            try:
                with PerformanceLogger(logger, func.__name__):
                    result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Function {func.__name__} failed: {e}")
                raise
        
        return wrapper
    return decorator
