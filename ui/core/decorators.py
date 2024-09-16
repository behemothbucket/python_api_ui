import time


def wait_until(wait_time=10, period=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            total_time = time.time() + wait_time
            while time.time() < total_time:
                if func(*args, **kwargs):
                    return True
                time.sleep(period)
            raise Exception(f"В течение {wait_time} секунд ничего не произошло.")

        return wrapper

    return decorator
