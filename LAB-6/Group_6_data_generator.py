import random
import matplotlib.pyplot as plt

class SensorSimulator:
    def __init__(self, min_value=0, max_value=500, seed=None):
        """
        Initializing the sensor simulator with optional min and max values, and an optional random seed.
        
        :param min_value: Minimum value of the sensor range.
        :param max_value: Maximum value of the sensor range.
        :param seed: Seed for the random number generator.
        """
        self.min_value = min_value
        self.max_value = max_value
        if seed is not None:
            random.seed(seed)
    
    def _generate_normalized_value(self):
        """
        Private method to generate a normalized random value between 0 and 1.
        
        :return: Normalized random value.
        """
        return random.random()
    
    @property
    def value(self):
        """
        Public property to get a sensor value within the specified range.
        
        :return: Random sensor value within the specified range.
        """
        normalized_value = self._generate_normalized_value()
        return self.min_value + (self.max_value - self.min_value) * normalized_value
    
    def generate_values(self, num_values=100):
        """
        Generate a list of sensor values.
        
        :param num_values: Number of values to generate.
        :return: List of generated sensor values.
        """
        return [self.value for _ in range(num_values)]
    
    def plot_values(self, values):
        """
        Plotting the sensor values using Matplotlib.
        
        :param values: List of sensor values to plot.
        """
        plt.figure(figsize=(10, 5))
        plt.plot(values, label='Sensor Value')
        plt.xlabel('Sample Number')
        plt.ylabel('Sensor Value')
        plt.title('Sensor Values Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

# Example usage
sensor = SensorSimulator(min_value=18, max_value=21)  # Simulating a temperature sensor
values = sensor.generate_values(200)  # Generating 600 sensor values
sensor.plot_values(values)  # Plotting the generated sensor values
