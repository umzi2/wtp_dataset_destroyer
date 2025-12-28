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
