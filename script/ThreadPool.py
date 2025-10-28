from __future__ import annotations
import threading
from typing import List, Any, Tuple, Dict
import copy
import queue

class ThreadPool:
    class Result:
        def __init__(self):
            self.__result     : Any = None
            self.__is_finished: bool = False
            self.__error      : Exception = None

        def isFinished(self) -> bool:
            return self.__is_finished
        
        def getError(self) -> Exception:
            return copy.copy(self.__error)
        
        def getResult(self) -> Any:
            return copy.copy(self.__result)

    class Info:
        def __init__(self, target: object, result: ThreadPool.Result, *args, **kwargs):
            self.target: object            = target
            self.result: ThreadPool.Result = result
            self.args  : Tuple             = args
            self.kwargs: Dict              = kwargs

    def __init__(self, max_thread_num: int = 2):
        self.max_thread_num           : int = max_thread_num
        self.__is_running             : bool = True
        self.__threads                : List[str] = []
        self.__call_wait_function_lock: threading.Lock = threading.Lock()
        self.__wait_function_infos    : queue.Queue = queue.Queue()

    def start(self):
        self.__is_running = True

    def stop(self):
        self.__is_running = False

    def isRunning(self) -> bool:
        return self.__is_running

    def isActive(self) -> bool:
        return len(self.__threads) > 0

    def getActiveThreadNum(self) -> int:
        return len(self.__threads)
    
    def getWaitThreadNum(self) -> int:
        return self.__wait_function_infos.qsize()

    def submit(self, target: object, *args, **kwargs) -> ThreadPool.Result:
        result = ThreadPool.Result()
        self.__wait_function_infos.put(ThreadPool.Info(target, result, *args, **kwargs))
        self.__callWaitFunction()
        return result

    def __executeFunction(self, info: ThreadPool.Info):
        try                  : info.result.__result = info.target(*info.args, **info.kwargs)
        except Exception as e: info.result.__error = e
        info.result.__is_finished = True
        self.__threads.remove(threading.current_thread())
        self.__callWaitFunction()

    def __callWaitFunction(self):
        ### 待機中の関数実行
        with self.__call_wait_function_lock:
            if threading.main_thread().is_alive() and self.isRunning() and len(self.__threads) < self.max_thread_num and self.__wait_function_infos.qsize() > 0:
                thread = threading.Thread(target=self.__executeFunction, args=[self.__wait_function_infos.get()])
                self.__threads.append(thread)
                thread.start()

if __name__ == "__main__":
    def func():
        print(threading.current_thread().name)

    thread_pool = ThreadPool(5)
    thread_pool.submit(func)
    thread_pool.submit(func)
    thread_pool.submit(func)
    thread_pool.submit(func)
    thread_pool.submit(func)
