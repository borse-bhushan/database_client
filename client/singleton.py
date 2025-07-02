import threading


class SingletonMeta(type):
    """
    Thread-safe Singleton metaclass.

    Any class using this metaclass will only have one instance.
    Subsequent instantiations will return the same instance.

    Example:
        class MyClass(metaclass=SingletonMeta):
            pass

        a = MyClass()
        b = MyClass()
        assert a is b

    Attributes:
        _instances (dict): Stores the singleton instances per class.
        _lock (threading.Lock): Ensures thread-safe instance creation.
    """

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        Returns the singleton instance for the class.
        Creates one if it doesn't exist.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
