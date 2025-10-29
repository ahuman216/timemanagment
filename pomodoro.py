import time
import threading

_lock = threading.Lock()

_is_running = False
_is_paused = False
_remaining_seconds = 0
_cycle = 0  
_phase = "idle" 
_thread = None


WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
CYCLES_BEFORE_LONG_BREAK = 4


def _run_pomodoro():
    global _is_running, _is_paused, _remaining_seconds, _cycle, _phase
    while _is_running:
        
        with _lock:
            _phase = "Work"
            _remaining_seconds = WORK_MIN * 60
        _countdown()

        if not _is_running:
            break

        _cycle += 1
        
        if _cycle % CYCLES_BEFORE_LONG_BREAK == 0:
            with _lock:
                _phase = "Long Break"
                _remaining_seconds = LONG_BREAK_MIN * 60
        else:
            with _lock:
                _phase = "Short Break"
                _remaining_seconds = SHORT_BREAK_MIN * 60
        _countdown()


def _countdown():
    global _remaining_seconds, _is_running
    while _is_running and _remaining_seconds > 0:
        time.sleep(1)
        with _lock:
            _remaining_seconds -= 1


def start():
    
    global _is_running, _thread
    with _lock:
        if _is_running:
            return
        _is_running = True
    _thread = threading.Thread(target=_run_pomodoro, daemon=True)
    _thread.start()


def stop():
    
    global _is_running, _remaining_seconds, _phase, _cycle
    with _lock:
        _is_running = False
        _remaining_seconds = 0
        _phase = "idle"
        _cycle = 0


def get_state():
    
    with _lock:
        return _phase, _is_running, _remaining_seconds, _cycle