import tkinter as tk
from tkinter import ttk
import random
import time
from grid import create_grid
from algorithms import greedy_search, a_star
from heuristics import manhattan, euclidean

CELL = 25

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinding Agent")
        
        self.rows, self.cols = 20, 20
        self.start, self.goal = (0, 0), (19, 19)
        self.grid = create_grid(self.rows, self.cols)
        
        self.dynamic_mode = tk.BooleanVar(value=False)
        self.current_path = []
        self.visited_nodes = set()
        self.agent_pos = self.start
        
        self.setup_controls()
        self.setup_canvas()
        self.draw_grid()

    def setup_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        # Environment Specs: Row/Col/Density 
        tk.Label(control_frame, text="Rows").grid(row=0, column=0)
        self.rows_entry = tk.Entry(control_frame, width=5); self.rows_entry.insert(0, "20")
        self.rows_entry.grid(row=0, column=1)

        tk.Label(control_frame, text="Cols").grid(row=0, column=2)
        self.cols_entry = tk.Entry(control_frame, width=5); self.cols_entry.insert(0, "20")
        self.cols_entry.grid(row=0, column=3)

        tk.Label(control_frame, text="Wall %").grid(row=0, column=4)
        self.density_entry = tk.Entry(control_frame, width=5); self.density_entry.insert(0, "0.3")
        self.density_entry.grid(row=0, column=5)

        # Algorithm Selection [cite: 234, 241]
        self.algorithm_var = tk.StringVar(value="A*")
        ttk.Combobox(control_frame, textvariable=self.algorithm_var, values=["A*", "Greedy BFS"], state="readonly").grid(row=1, column=0, columnspan=2)

        # Heuristic Selection [cite: 238, 241]
        self.heuristic_var = tk.StringVar(value="Manhattan")
        ttk.Combobox(control_frame, textvariable=self.heuristic_var, values=["Manhattan", "Euclidean"], state="readonly").grid(row=1, column=2, columnspan=2)

        # Dynamic Obstacle Toggle 
        tk.Checkbutton(control_frame, text="Dynamic Mode", variable=self.dynamic_mode).grid(row=1, column=4, columnspan=2)

        # Action Buttons
        tk.Button(control_frame, text="Generate Map", command=self.random_map).grid(row=2, column=0, columnspan=2)
        tk.Button(control_frame, text="Run Agent", command=self.start_agent, bg="#4CAF50", fg="white").grid(row=2, column=2, columnspan=2)
        tk.Button(control_frame, text="Reset", command=self.reset_grid).grid(row=2, column=4, columnspan=2)

        # Metrics Dashboard [cite: 260]
        self.info_label = tk.Label(self.root, text="System Ready", font=('Arial', 10, 'bold'))
        self.info_label.pack()

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.cols * CELL, height=self.rows * CELL)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.toggle_obstacle) # Interactive Editor 

    def random_map(self):
        self.rows = int(self.rows_entry.get())
        self.cols = int(self.cols_entry.get())
        self.grid = create_grid(self.rows, self.cols)
        self.goal = (self.rows - 1, self.cols - 1)
        
        density = float(self.density_entry.get())
        for r in range(self.rows):
            for c in range(self.cols):
                if (r,c) not in [self.start, self.goal]:
                    self.grid[r][c] = 1 if random.random() < density else 0
        self.draw_grid()

    def toggle_obstacle(self, event):
        r, c = event.y // CELL, event.x // CELL
        if 0 <= r < self.rows and 0 <= c < self.cols and (r,c) not in [self.agent_pos, self.goal]:
            self.grid[r][c] = 1 - self.grid[r][c]
            self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * CELL, r * CELL
                color = "white"
                if self.grid[r][c] == 1: color = "black"
                elif (r, c) == self.agent_pos: color = "blue"
                elif (r, c) == self.goal: color = "purple"
                elif (r, c) in self.current_path: color = "#90EE90" # Green for Final Path 
                elif (r, c) in self.visited_nodes: color = "#FFCCCB" # Red/Light Red for Visited 
                
                self.canvas.create_rectangle(x1, y1, x1+CELL, y1+CELL, fill=color, outline="#eee")

    def start_agent(self):
        self.agent_pos = self.start
        self.replan()
        self.move_agent()

    def replan(self):
        """Logic for real-time re-planning [cite: 247]"""
        h_func = manhattan if self.heuristic_var.get() == "Manhattan" else euclidean
        if self.algorithm_var.get() == "A*":
            path, visited, nodes, ms = a_star(self.grid, self.agent_pos, self.goal, h_func)
        else:
            path, visited, nodes, ms = greedy_search(self.grid, self.agent_pos, self.goal, h_func)
        
        self.current_path = path if path else []
        self.visited_nodes = visited
        self.draw_grid()
        # Update metrics dashboard [cite: 260, 261, 262, 263]
        self.info_label.config(text=f"Visited: {nodes} | Path Cost: {len(self.current_path)-1} | Time: {round(ms, 2)}ms")

    def move_agent(self):
        if not self.current_path or len(self.current_path) <= 1:
            return

        self.agent_pos = self.current_path[1]
        self.current_path.pop(0)

        if self.dynamic_mode.get():
          
            for _ in range(2):
                r, c = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
                if (r,c) not in [self.agent_pos, self.goal] and random.random() < 0.05:
                    self.grid[r][c] = 1
                    
                    if (r,c) in self.current_path:
                        self.replan()
                        break 

        self.draw_grid()
        if self.agent_pos != self.goal:
            self.root.after(150, self.move_agent)
    def reset_grid(self):
        self.grid = create_grid(self.rows, self.cols)
        self.current_path = []
        self.visited_nodes = set()
        self.agent_pos = self.start
        self.draw_grid()
        self.info_label.config(text="Grid Reset")

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()