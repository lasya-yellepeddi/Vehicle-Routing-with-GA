import tkinter as tk
from tkinter import messagebox
import numpy as np

def get_locations():
    global num_locations
    try:
        num_locations = int(loc_entry.get())
        if num_locations <= 1:
            raise ValueError
        create_locations_window(num_locations)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number of locations (greater than 1).")

def create_locations_window(num_locations):
    locations_window = tk.Toplevel(root)
    locations_window.title("Enter Locations")

    tk.Label(locations_window, text="Enter Location Names:").grid(row=0, columnspan=num_locations)
    
    location_entries = []
    for i in range(num_locations):
        entry = tk.Entry(locations_window)
        entry.grid(row=1, column=i)
        location_entries.append(entry)

    def save_locations():
        global locations
        locations = [entry.get() for entry in location_entries]
        if any(location == "" for location in locations):
            messagebox.showerror("Invalid input", "Please enter all location names.")
        else:
            create_distance_matrix_window(locations_window)

    save_button = tk.Button(locations_window, text="Save Locations", command=save_locations)
    save_button.grid(row=2, columnspan=num_locations)

def create_distance_matrix_window(locations_window):
    locations_window.destroy()
    distance_window = tk.Toplevel(root)
    distance_window.title("Enter Distances")

    matrix = []

    def validate_and_save_matrix():
        nonlocal matrix
        try:
            matrix = [[0 if i == j else float(entry.get()) for j, entry in enumerate(row)] for i, row in enumerate(entries)]
            np_matrix = np.array(matrix)
            display_best_route(np_matrix)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for distances.")
    
    # Creating grid of distance inputs
    entries = []
    for i in range(num_locations):
        row_entries = []
        for j in range(num_locations):
            entry = tk.Entry(distance_window, width=5)
            entry.grid(row=i + 1, column=j + 1)
            if i == j:
                entry.insert(0, "0")  # Distance to itself is 0
                entry.config(state='disabled')  # Disable entry for same location
            row_entries.append(entry)
        entries.append(row_entries)
    
    # Displaying location names as labels
    for i in range(num_locations):
        tk.Label(distance_window, text=locations[i]).grid(row=i + 1, column=0)
        tk.Label(distance_window, text=locations[i]).grid(row=0, column=i + 1)

    # Add Save button
    save_button = tk.Button(distance_window, text="Save Matrix", command=validate_and_save_matrix)
    save_button.grid(row=num_locations + 1, columnspan=num_locations + 1)

def display_best_route(matrix):
    # Simple greedy algorithm to find the shortest route
    def greedy_route(matrix):
        num_cities = len(matrix)
        visited = [False] * num_cities
        current_city = 0
        route = [current_city]
        visited[current_city] = True
        total_distance = 0

        while len(route) < num_cities:
            next_city = None
            shortest_distance = float('inf')
            for city in range(num_cities):
                if not visited[city] and matrix[current_city][city] < shortest_distance:
                    shortest_distance = matrix[current_city][city]
                    next_city = city
            if next_city is not None:
                route.append(next_city)
                visited[next_city] = True
                total_distance += shortest_distance
                current_city = next_city

        total_distance += matrix[current_city][0]  # Return to the start
        route.append(0)
        return route, total_distance

    optimal_route, total_distance = greedy_route(matrix)

    optimal_route_names = [locations[i] for i in optimal_route]

    # Displaying the best route
    messagebox.showinfo("Optimal Route", f"Optimal Route: {' -> '.join(optimal_route_names)}\nTotal Distance: {total_distance:.2f} km")

root = tk.Tk()
root.title("Vehicle Routing Problem")

# Entry for number of locations
tk.Label(root, text="Enter number of locations:").grid(row=0, column=0)
loc_entry = tk.Entry(root)
loc_entry.grid(row=0, column=1)

# Button to submit number of locations and proceed
submit_button = tk.Button(root, text="Submit", command=get_locations)
submit_button.grid(row=0, column=2)

root.mainloop()
