import heapq
import time

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.position)
        node = node.parent
    return path[::-1]

def get_neighbors(grid, position):
    rows, cols = len(grid), len(grid[0])
    r, c = position
    neighbors = []
    # Grid supports 4-directional movement
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

def greedy_search(grid, start, goal, heuristic):
    start_time = time.time()
    open_list = []
    visited = set()
    nodes_expanded = 0
    
    start_node = Node(start)
    start_node.h = heuristic(start, goal)
    start_node.f = start_node.h
    heapq.heappush(open_list, (start_node.f, start_node))

    while open_list:
        _, current = heapq.heappop(open_list)
        if current.position == goal:
            return reconstruct_path(current), visited, set([item[1].position for item in open_list]), nodes_expanded, (time.time() - start_time)*1000

        if current.position in visited: continue
        visited.add(current.position)
        nodes_expanded += 1

        for neighbor in get_neighbors(grid, current.position):
            if neighbor not in visited:
                node = Node(neighbor, current)
                node.h = heuristic(neighbor, goal)
                node.f = node.h
                heapq.heappush(open_list, (node.f, node))
    return None, visited, set([item[1].position for item in open_list]), nodes_expanded, 0

def a_star(grid, start, goal, heuristic):
    start_time = time.time()
    open_list = []
    closed_list = {} # Stores position: g_cost to allow node re-opening if better path found
    nodes_expanded = 0
    
    start_node = Node(start)
    start_node.h = heuristic(start, goal)
    start_node.f = start_node.g + start_node.h
    heapq.heappush(open_list, (start_node.f, start_node))

    while open_list:
        _, current = heapq.heappop(open_list)
        if current.position == goal:
            return reconstruct_path(current), set(closed_list.keys()), set([item[1].position for item in open_list]), nodes_expanded, (time.time() - start_time)*1000

        if current.position in closed_list and closed_list[current.position] <= current.g:
            continue
            
        closed_list[current.position] = current.g
        nodes_expanded += 1

        for neighbor in get_neighbors(grid, current.position):
            g_score = current.g + 1
            node = Node(neighbor, current)
            node.g = g_score
            node.h = heuristic(neighbor, goal)
            node.f = node.g + node.h
            heapq.heappush(open_list, (node.f, node))
            
    return None, set(closed_list.keys()), set([item[1].position for item in open_list]), nodes_expanded, 0
