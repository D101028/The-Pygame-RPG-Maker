import heapq
import random

# Define the grid size
grid_size = 20  # Each cell is 20x20 pixels
map_width = 30
map_height = 20

# Create a grid with random obstacles
grid = [[0 for _ in range(map_width)] for _ in range(map_height)]

# Add obstacles randomly
for _ in range(int(map_width * map_height * 0.2)):  # 20% obstacles
    x = random.randint(0, map_width - 1)
    y = random.randint(0, map_height - 1)
    grid[y][x] = 1

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]
        
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
        
        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + 1
            
            if 0 <= neighbor[0] < map_width:
                if 0 <= neighbor[1] < map_height:                
                    if grid[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
    
    return False

# Example usage
start = (0, 0)
goal = (7, 6)
path = a_star(grid, start, goal)
[print(i) for i in grid]
print(path)
