import requests
import time

# Coordinates for Rehab Egypt and Madinaty Egypt
rehab_egypt = (30.0293, 31.1939)
madinaty_egypt = (30.1695, 31.5950)

# Hypothetical current location (North 90 Street, New Cairo)
current_location = (30.022593, 31.497494)

def navigate_to(destination):
    url = f"http://router.project-osrm.org/route/v1/walking/{current_location[1]},{current_location[0]};{destination[1]},{destination[0]}?overview=false"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error accessing routing service: {response.status_code}")
        return
    data = response.json()
    if 'routes' not in data or len(data['routes']) == 0:
        print("No routes found.")
        return
    # Extract steps from the response
    steps = data['routes'][0]['legs'][0]['steps']
    # Print navigation instructions
    print(f"Navigation to {destination}:")
    for index, step in enumerate(steps, start=1):
        instruction = step['maneuver']['instruction']
        print(f"Step {index}: {instruction}")
        # Simulate time taken for the step
        time.sleep(5)  # Simulating 5 seconds per step

try:
    print("Simulating navigation to Rehab Egypt:")
    navigate_to(rehab_egypt)
    print("Navigation to Rehab Egypt completed.")
    time.sleep(2)  # Add a pause between navigations
    print("Simulating navigation to Madinaty Egypt:")
    navigate_to(madinaty_egypt)
    print("Navigation to Madinaty Egypt completed.")

except KeyboardInterrupt:
    print("\nNavigation interrupted by user.")
