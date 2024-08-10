import random
import time
import json

start_id = 111

def create_data():
    global start_id
    data = {
        'id': start_id,
        'patient': f'Patient_{start_id}',
        'time': time.asctime(),
        'heart_rate': int(random.gauss(80, 1)),
        'respiratory_rate': int(random.gauss(12, 2)),
        'heart_rate_variability': 65,
        'body_temperature': random.gauss(99, 0.5),
        'blood_pressure': {
            'systolic': int(random.gauss(105, 2)),
            'diastolic': int(random.gauss(70, 1))
        },
        'activity': 'Walking'
    }
    start_id += 1
    return data

def print_data(data):
    try:
        print(f"\nID: {data['id']}")
        print(f"Patient: {data['patient']}")
        print(f"Time: {data['time']}")
        print(f"Heart Rate: {data['heart_rate']}")
        print(f"Respiratory Rate: {data['respiratory_rate']}")
        print(f"Heart Rate Variability: {data['heart_rate_variability']}")
        print(f"Body Temperature: {data['body_temperature']}")
        print(f"Blood Pressure: {data['blood_pressure']['systolic']}/{data['blood_pressure']['diastolic']}")
        print(f"Activity: {data['activity']}")
    except KeyError as e:
        print(f"Missing data in the record: {e}")

# Example usage:
if __name__ == "__main__":
    data = create_data()
    print_data(data)

