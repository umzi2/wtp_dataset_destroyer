from numpy.random import default_rng


class SafeRNG:
    def __init__(self, seed: int = None):
        self.rng = default_rng(seed)

    def safe_uniform(self, rand_list: list[float] | float) -> float:
        if not isinstance(rand_list, list):
            return rand_list
        if len(rand_list) == 1 or rand_list[0] >= rand_list[1]:
            return rand_list[0]
        return self.rng.uniform(rand_list[0], rand_list[1])

    def safe_randint(self, rand_list: list[int] | int) -> int:
        if not isinstance(rand_list, list):
            return rand_list
        if len(rand_list) == 1 or rand_list[0] >= rand_list[1]:
            return rand_list[0]
        return int(self.rng.integers(rand_list[0], rand_list[1]))

    def __getattr__(self, name):
        return getattr(self.rng, name)
