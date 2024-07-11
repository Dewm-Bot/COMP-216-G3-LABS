import random
import matplotlib.pyplot as plt

class SensorDataGenerator:
    def __init__(self, min_value=18, max_value=21):
        self.min_value = min_value
        self.max_value = max_value

    def _generate_normalized_value(self):
        return random.random()

    @property
    def value(self):
        normalized_value = self._generate_normalized_value()
        return self.min_value + normalized_value * (self.max_value - self.min_value)
