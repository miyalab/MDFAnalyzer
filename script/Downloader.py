import time
import threading
import shutil
from typing import List
from enum import IntEnum, auto

import ThreadPool

class DownloadStatus(IntEnum):
    NoCopy      = auto()
    Downloading = auto()
    Complete    = auto()

class DownloadPath:
    def __init__(self, src: str, dst: str, status: DownloadStatus):
        self.src = src
        self.dst = dst
        self.status = status

### ダウンロード関数
def __downloadFile(paths: DownloadPath):
    paths.status = DownloadStatus.Downloading
    shutil.copy(paths.src, paths.dst)
    paths.status = DownloadStatus.Complete

def downloadFiles(download_paths: List[DownloadPath], parallel_download_num: int = 1):
    ### スレッド管理
    main_thread = threading.main_thread()
    thread_pool = ThreadPool.ThreadPool(parallel_download_num)

    ### ダウンロードファイル登録
    [thread_pool.submit(__downloadFile, paths) for paths in download_paths]

    ### ダウンロード終了まで待機
    while thread_pool.isActive():
        ### メインスレッドが機能しなくなったときはダウンロード停止
        if not main_thread.is_alive():
            thread_pool.stop()
        time.sleep(1)
    
