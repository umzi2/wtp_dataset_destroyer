import numpy as np

from src.process.utils import probability
from src.utils.registry import register_class, get_class


@register_class("and")
class AndOperator:
    def __init__(self, and_dict: dict):
        one_process = and_dict["one_process"]
        two_process = and_dict["two_process"]
        self.probability_one = and_dict.get("probability_one", 1.0)
        self.probability_two = and_dict.get("probability_two", 0.5)
        self.turn_one = []
        for process_dict in one_process:
            process_type = process_dict["type"]
            self.turn_one.append(get_class(process_type)(process_dict))
        self.turn_two = []
        for process_dict in two_process:
            process_type = process_dict["type"]
            self.turn_two.append(get_class(process_type)(process_dict))

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        if not probability(self.probability_one):
            for loss in self.turn_one:
                lq, hq = loss.run(lq, hq)
            if not probability(self.probability_two):
                for loss in self.turn_two:
                    lq, hq = loss.run(lq, hq)
        return lq, hq


@register_class("or")
class OrOperator:
    def __init__(self, or_dict: dict):
        one_process = or_dict["one_process"]
        two_process = or_dict["two_process"]
        self.probability_one = or_dict.get("probability_one", 0.5)
        self.probability_two = or_dict.get("probability_two", 0.5)
        self.turn_one = []
        for process_dict in one_process:
            process_type = process_dict["type"]
            self.turn_one.append(get_class(process_type)(process_dict))
        self.turn_two = []
        for process_dict in two_process:
            process_type = process_dict["type"]
            self.turn_two.append(get_class(process_type)(process_dict))

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        if probability(self.probability_one):
            if not probability(self.probability_two):
                for loss in self.turn_two:
                    lq, hq = loss.run(lq, hq)
            return lq, hq
        for loss in self.turn_one:
            lq, hq = loss.run(lq, hq)
        return lq, hq
