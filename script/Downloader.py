import threading
import shutil
from typing import List
from enum import IntEnum, auto

class DownloadStatus(IntEnum):
    NoCopy = auto()
    Downloading = auto()
    Complete = auto()

class DownloadPath:
    def __init__(self, src: str, dst: str, status: DownloadStatus):
        self.src = src
        self.dst = dst
        self.status = status

def downloadFiles(download_paths: List[DownloadPath]):
    ### MDFをコピー
    main_thread = threading.main_thread()

    for paths in download_paths:
        ### ダウンロード処理
        paths.status = DownloadStatus.Downloading
        shutil.copy(paths.src, paths.dst)
        paths.status = DownloadStatus.Complete

        ### メインスレッド終了時には中断して終了
        if not main_thread.is_alive(): break