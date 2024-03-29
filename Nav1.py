import requests
import time

# Coordinates for Rehab Egypt
rehab_egypt = (29.9792, 31.1342)

# Hypothetical current location (North 90 Street, New Cairo)
current_location = (30.022593, 31.497494)

def navigate_to(destination):
    url = f"http://router.project-osrm.org/route/v1/walking/{current_location[1]},{current_location[0]};{destination[1]},{destination[0]}?overview=false"
    print(f"{url}")
    response = requests.get(url)
    data = response.json()

    # Handle potential errors in API response
    if 'routes' not in data:
        print("Error: Unable to retrieve navigation data.")
        return

    # Extract steps from the response
    steps = data['routes'][0]['legs'][0]['steps']

    # Print navigation instructions
    print(f"Navigation to {destination}:")
    for index, step in enumerate(steps, start=1):
        instruction = step['maneuver']['instruction']
        # Extract the first word(s) as a label (modify if needed)
        label = instruction.split()[0]
        print(f"{label}: {instruction}")
        time.sleep(1)  # Delay between instructions

  # Add a small delay between each instruction

# Simulate navigation by calling the function
navigate_to(rehab_egypt)

print("Navigation complete!")
