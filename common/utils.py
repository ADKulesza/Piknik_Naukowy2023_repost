def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        nonlocal instances  # nonlocal is not required here!
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
