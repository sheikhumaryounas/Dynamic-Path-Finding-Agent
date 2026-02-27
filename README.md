# Dynamic Pathfinding Agent

This repository contains a Dynamic Pathfinding Agent that navigates a grid-based environment using Informed Search Algorithms: Greedy Best-First Search (GBFS) and A* Search.

## Features
- Dynamic Grid Environment with adjustable size and obstacle density
- Manual Obstacle Placement via interactive GUI
- Greedy Best-First Search and A* Search implementations
- Manhattan and Euclidean Heuristics
- Dynamic Obstacle Spawning (Dynamic Mode for real-time adjustments)
- Real-Time Re-planning when obstacles block the path
- Performance Metrics Dashboard (Execution Time, Path Cost, Nodes Expanded)

## Prerequisites & Dependencies
The project relies solely on Python's standard libraries (`tkinter`, `heapq`, `time`, `random`, `math`). **You do not need to install external packages like `pygame`.**

*Note: On Windows and macOS, `tkinter` is included with Python by default. On some Linux distributions, you might need to install it via your package manager (e.g., `sudo apt-get install python3-tk`).*

## How to Run

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd Dynamic_Path_Finder
   ```
2. Run the main application:
   ```bash
   python main.py
   ```

## Controls & Usage
- **Algorithm Selection**: Choose between A* and Greedy BFS using the dropdown.
- **Heuristic Selection**: Choose between Manhattan and Euclidean heuristics using the dropdown.
- **Dynamic Mode Toggle**: Enable dynamic obstacles that spontaneously appear as the agent moves.
- **Generate Map**: Creates a new random grid based on the provided rows, columns, and wall density percentage.
- **Run Agent**: Starts the pathfinding agent to navigate to the target.
- **Reset**: Clears the grid but keeps the obstacle layout, returning the agent to the starting point.
- **Interactive Editor**: Left Mouse Click on any grid cell to manually toggle obstacles on or off.

## Repository Structure
- `main.py`: GUI and application entry point.
- `algorithms.py`: A* and Greedy Best-First Search implementations.
- `heuristics.py`: Manhattan and Euclidean distance functions.
- `grid.py`: Utility for generating the initial grid.
- `README.md`: Project documentation and instructions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Developed by Umar Younas**
