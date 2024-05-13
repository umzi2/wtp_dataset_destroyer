registered_classes = {}


def register_class(key):
    """
    Decorator function to register a class with a given key.

    Args:
        key (str): The key to associate with the registered class.

    Returns:
        callable: Decorator function.

    """

    def decorator(cls):
        """
        Decorator function to register a class with a given key.

        Args:
            cls (class): The class to be registered.

        Returns:
            class: The input class.

        """
        registered_classes[key] = cls
        return cls

    return decorator


def get_class(key):
    """
    Get a registered class by its key.

    Args:
        key (str): The key associated with the registered class.

    Returns:
        class or None: The registered class if found, otherwise None.

    """
    return registered_classes.get(key, None)
