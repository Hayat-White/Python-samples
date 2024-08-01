#!/usr/bin/python3.5
import tkinter as tk
import random

class FireSimulation:
    def __init__(self, master):
        self.master = master
        master.title("Fire Simulation")

        self.tile_size = 10  # Size of each tile in pixels
        self.grid_size = 50  # Size of the grid (20x20)
        self.canvas_size = self.tile_size * self.grid_size  # Canvas size in pixels
        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.iteration_count = 0
        self.max_iterations = tk.IntVar(value=15)  # Default number of iterations
        self.running = False

        self.create_widgets()
        self.init_grid()
        

    def create_widgets(self):
        self.iteration_entry = tk.Entry(self.master, textvariable=self.max_iterations)
        self.iteration_entry.pack()

        self.start_button = tk.Button(self.master, text="Start", command=self.start_simulation)
        self.start_button.pack()

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_simulation)
        self.reset_button.pack()

    def init_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                state = random.randint(0, 100)
                self.grid[i][j] = state
                color = self.get_color(state)
                x0, y0 = i * self.tile_size, j * self.tile_size
                x1, y1 = x0 + self.tile_size, y0 + self.tile_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def get_color(self, state):
        if state > 70 and state <= 80:
            return "red"
        elif state > 90:
            return "yellow"
        elif state < 70:
            return "green"
        elif state <= 90 and state > 80:
            return "black"
        else:
            return "green"

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                state = self.grid[i][j]
                color = self.get_color(state)
                x0, y0 = i * self.tile_size, j * self.tile_size
                x1, y1 = x0 + self.tile_size, y0 + self.tile_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def simulate(self):
        if not self.running or self.iteration_count >= self.max_iterations.get():
            return

        new_grid = [row[:] for row in self.grid]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                state = self.grid[i][j]

                # Current tile is green
                if state < 70:
                    if any(self.grid[ni][nj] > 90 for ni in range(max(0, i-1), min(self.grid_size, i+2)) for nj in range(max(0, j-1), min(self.grid_size, j+2))):
                        if random.random() < 0.25:  # 25% chance to turn yellow if any surrounding tile is yellow
                            new_grid[i][j] = random.randint(91, 100)
                    elif any(self.grid[ni][nj] > 70 and self.grid[ni][nj] <= 80 for ni in range(max(0, i-1), min(self.grid_size, i+2)) for nj in range(max(0, j-1), min(self.grid_size, j+2))):
                        if random.random() < 0.15:  # 15% chance to turn yellow if any surrounding tile is red
                            new_grid[i][j] = random.randint(91, 100)
                # Current tile is yellow
                elif state > 90:
                    if any(self.grid[ni][nj] > 70 and self.grid[ni][nj] <= 80 for ni in range(max(0, i-1), min(self.grid_size, i+2)) for nj in range(max(0, j-1), min(self.grid_size, j+2))):
                        new_grid[i][j] = random.randint(71, 80)  # Turn red if any surrounding tile is red
                    elif any(self.grid[ni][nj] < 70 for ni in range(max(0, i-1), min(self.grid_size, i+2)) for nj in range(max(0, j-1), min(self.grid_size, j+2))):
                        if random.random() < 0.05:  # 5% chance to turn green if any surrounding tile is green
                            new_grid[i][j] = random.randint(0, 69)
                # Current tile is red
                elif state > 70 and state <= 80:
                    new_grid[i][j] = random.randint(81, 90)  # Turn black

        self.grid = new_grid
        self.update_grid()
        self.iteration_count += 1
        self.master.after(self.max_iterations.get(), self.simulate)

    def start_simulation(self):
        self.running = True
        self.iteration_count = 0
        self.simulate()

    def reset_simulation(self):
        self.running = False
        self.iteration_count = 0
        self.init_grid()
        self.update_grid()

if __name__ == "__main__":
    root = tk.Tk()
    fire_simulation = FireSimulation(root)
    root.mainloop()
