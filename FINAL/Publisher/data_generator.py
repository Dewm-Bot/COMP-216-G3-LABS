import random

class SensorSimulator:
    def __init__(self, min_value=18, max_value=21, seed=None):
        """
        Initializes the SensorSimulator with optional minimum and maximum values,
        and an optional random seed.
        :param min_value: Minimum value for the sensor data.
        :param max_value: Maximum value for the sensor data.
        :param seed: Seed for the random number generator (optional).
        """
        self.min_value = min_value
        self.max_value = max_value
        if seed is not None:
            random.seed(seed)

    def generate_value(self):
        """
        Generates a random sensor value within the specified range.
        :return: A float representing the sensor value.
        """
        return random.uniform(self.min_value, self.max_value)
