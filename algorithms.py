from collections import deque
import heapq
import random
import math

GRID_SIZE = 10  # Can be changed to a parameter

# ----------------- Helper Functions -----------------
def manhattan_distance(a, b):
    """Calculate Manhattan distance between two points"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_occupied_positions(bots, current_bot=None):
    """Get set of occupied positions, optionally excluding current bot"""
    if current_bot is None:
        return {(bot.x, bot.y) for bot in bots}
    return {(bot.x, bot.y) for bot in bots if bot is not current_bot}

# ----------------- Random Strategy -----------------
def random_strategy(bot, grid, points, bots):
    """Random movement strategy"""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)
    occupied = get_occupied_positions(bots)
    
    for dx, dy in directions:
        nx, ny = bot.x + dx, bot.y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in occupied:
            return dx, dy
    return 0, 0  # No movement if all directions blocked

# ----------------- Greedy Strategy -----------------
def greedy_strategy(bot, grid, points, bots):
    """Greedy strategy targeting nearest point"""
    if not points:
        return 0, 0
    
    # Find nearest point using Manhattan distance
    target = min(points, key=lambda pt: manhattan_distance((bot.x, bot.y), pt))
    
    # Choose direction that reduces distance to target
    if bot.x < target[0]: return 1, 0
    if bot.x > target[0]: return -1, 0
    if bot.y < target[1]: return 0, 1
    if bot.y > target[1]: return 0, -1
    return 0, 0

# ----------------- Rule-based Strategy -----------------
def rule_based_strategy(bot, grid, points, bots):
    """Rule-based strategy with fallback to greedy"""
    occupied = get_occupied_positions(bots)
    
    # First check adjacent cells for points
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = bot.x + dx, bot.y + dy
        if (nx, ny) in points and (nx, ny) not in occupied:
            return dx, dy
    
    # Fallback to greedy strategy if no adjacent points
    return greedy_strategy(bot, grid, points, bots)

# ----------------- BFS Strategy -----------------
def bfs_path(start, goals, bots):
    """Breadth-First Search pathfinding"""
    queue = deque([(start, [])])
    visited = set()
    occupied = get_occupied_positions(bots)
    goal_set = set(goals)
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) in goal_set:
            return path
        
        if (x, y) in visited:
            continue
            
        visited.add((x, y))
        
        # Explore neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and 
                (nx, ny) not in visited and 
                (nx, ny) not in occupied or (nx, ny) in goal_set):
                queue.append(((nx, ny), path + [(dx, dy)]))
    
    return []  # No path found

def bfs_strategy(bot, grid, points, bots):
    """BFS-based movement strategy"""
    if not points:
        return 0, 0
        
    path = bfs_path((bot.x, bot.y), points, bots)
    return path[0] if path else (0, 0)

# ----------------- A* Strategy -----------------
def a_star_path(start, goals, bots):
    """A* pathfinding algorithm with Manhattan heuristic"""
    def heuristic(pos):
        return min(manhattan_distance(pos, goal) for goal in goals)
    
    open_set = []
    heapq.heappush(open_set, (0, start, []))  # (f_score, position, path)
    closed = set()
    occupied = get_occupied_positions(bots)
    goal_set = set(goals)
    
    while open_set:
        _, current, path = heapq.heappop(open_set)
        
        if current in goal_set:
            return path
            
        if current in closed:
            continue
            
        closed.add(current)
        
        x, y = current
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and 
                (nx, ny) not in closed and 
                ((nx, ny) not in occupied or (nx, ny) in goal_set)):
                new_path = path + [(dx, dy)]
                g_score = len(new_path)
                h_score = heuristic((nx, ny))
                f_score = g_score + h_score
                heapq.heappush(open_set, (f_score, (nx, ny), new_path))
    
    return []  # No path found

def a_star_strategy(bot, grid, points, bots):
    """A*-based movement strategy"""
    if not points:
        return 0, 0
        
    path = a_star_path((bot.x, bot.y), points, bots)
    return path[0] if path else (0, 0)

# ----------------- JPS Strategy -----------------
def jps_identify_successors(parent, current, goals, bots):
    x, y = current
    occupied = get_occupied_positions(bots)
    successors = []

    if parent is None:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                successors.append((dx, dy))
        return successors

    # 以下保留你的原本判斷
    px, py = parent
    dx, dy = x - px, y - py
    
    # Check for forced neighbors
    if dx != 0 and dy != 0:  # Diagonal movement
        # Natural neighbors
        if (x + dx, y + dy) not in occupied:
            successors.append((dx, dy))
        
        # Forced neighbors
        if (x, y + dy) in occupied and (x + dx, y) not in occupied:
            successors.append((dx, 0))
        if (x + dx, y) in occupied and (x, y + dy) not in occupied:
            successors.append((0, dy))
    else:  # Straight movement
        if dx == 0:  # Vertical
            if (x, y + dy) not in occupied:
                successors.append((0, dy))
            
            # Forced neighbors
            if (x + 1, y) in occupied and (x + 1, y + dy) not in occupied:
                successors.append((1, dy))
            if (x - 1, y) in occupied and (x - 1, y + dy) not in occupied:
                successors.append((-1, dy))
        else:  # Horizontal
            if (x + dx, y) not in occupied:
                successors.append((dx, 0))
            
            # Forced neighbors
            if (x, y + 1) in occupied and (x + dx, y + 1) not in occupied:
                successors.append((dx, 1))
            if (x, y - 1) in occupied and (x + dx, y - 1) not in occupied:
                successors.append((dx, -1))
    
    return successors

def jps_jump(current, direction, goals, bots):
    dx, dy = direction
    x, y = current
    occupied = get_occupied_positions(bots)
    goal_set = set(goals)
    
    while True:
        x += dx
        y += dy
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return None
        if (x, y) in occupied:
            return None
        if (x, y) in goal_set:
            return (x, y)
        # forced neighbor check
        if dx != 0 and dy != 0:  # diagonal
            # 如果正交方向有 forced neighbor，則回傳這個跳點
            if (((x - dx, y + dy) in occupied and (x - dx, y) not in occupied) or
                ((x + dx, y - dy) in occupied and (x, y - dy) not in occupied)):
                return (x, y)
            # 斜向時也要對正交方向遞迴 jump
            if (jps_jump((x, y), (dx, 0), goals, bots) is not None or
                jps_jump((x, y), (0, dy), goals, bots) is not None):
                return (x, y)
        else:  # straight
            if dx == 0:  # vertical
                if ((x + 1, y) in occupied and (x + 1, y - dy) not in occupied) or \
                   ((x - 1, y) in occupied and (x - 1, y - dy) not in occupied):
                    return (x, y)
            else:  # horizontal
                if ((x, y + 1) in occupied and (x - dx, y + 1) not in occupied) or \
                   ((x, y - 1) in occupied and (x - dx, y - 1) not in occupied):
                    return (x, y)

def jps_path(start, goals, bots):
    """Jump Point Search main algorithm"""
    open_set = []
    heapq.heappush(open_set, (0, start, None, []))  # (f, node, parent, path)
    closed = set()
    occupied = get_occupied_positions(bots)
    goal_set = set(goals)
    
    while open_set:
        _, current, parent, path = heapq.heappop(open_set)
        
        if current in goal_set:
            return path
            
        if current in closed:
            continue
            
        closed.add(current)
        
        # Get valid jump directions
        directions = jps_identify_successors(parent, current, goal_set, bots)
        
        for dx, dy in directions:
            jump_point = jps_jump(current, (dx, dy), goal_set, bots)
            
            if jump_point:
                jx, jy = jump_point
                new_path = path + [(dx, dy)]
                g = len(new_path)
                h = min(manhattan_distance((jx, jy), goal) for goal in goals)
                f = g + h
                heapq.heappush(open_set, (f, jump_point, current, new_path))
    
    return []  # No path found

def jps_strategy(bot, grid, points, bots):
    if not points:
        return 0, 0
    occupied = {(b.x, b.y) for b in bots if b is not bot}
    target = min(points, key=lambda pt: abs(bot.x - pt[0]) + abs(bot.y - pt[1]))
    path = jps_path((bot.x, bot.y), [target], bots)
    print("bot位置:", (bot.x, bot.y), "目標:", target, "路徑:", path)
    return path[0] if path else (0, 0)

# ----------------- Improved RRT Strategy -----------------
def rrt_path(start, goal, bots, max_iter=500):
    """Rapidly-exploring Random Tree pathfinding"""
    occupied = get_occupied_positions(bots)
    tree = {start: None}  # Node: parent
    
    for _ in range(max_iter):
        # Bias sampling toward goal (80% chance)
        if random.random() < 0.8:
            target = goal
        else:
            target = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        
        # Find nearest node in tree
        nearest = min(tree.keys(), 
                     key=lambda n: manhattan_distance(n, target))
        
        # Calculate step direction (max step size = 1)
        dx = target[0] - nearest[0]
        dy = target[1] - nearest[1]
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        new_node = (nearest[0] + step_x, nearest[1] + step_y)
        
        # Check validity
        if (0 <= new_node[0] < GRID_SIZE and 0 <= new_node[1] < GRID_SIZE and 
            new_node not in occupied and new_node not in tree):
            
            tree[new_node] = nearest
            
            # Check if goal reached
            if new_node == goal:
                # Reconstruct path
                path = []
                current = new_node
                while tree[current] is not None:
                    parent = tree[current]
                    path.append((current[0]-parent[0], current[1]-parent[1]))
                    current = parent
                return path[::-1]  # Reverse to start->goal
    
    return []  # No path found

def rrt_strategy(bot, grid, points, bots):
    """RRT-based movement strategy"""
    if not points:
        return 0, 0
    
    # Find nearest point
    target = min(points, key=lambda pt: manhattan_distance((bot.x, bot.y), pt))
    
    path = rrt_path((bot.x, bot.y), target, bots)
    return path[0] if path else (0, 0)

# ----------------- Hybrid Strategy -----------------
def hybrid_strategy(bot, grid, points, bots):
    """Hybrid strategy that selects the best approach based on situation"""
    if not points:
        return 0, 0
    
    # If target is adjacent, take it immediately
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = bot.x + dx, bot.y + dy
        if (nx, ny) in points and (nx, ny) not in get_occupied_positions(bots):
            return dx, dy
    
    # For small number of points in large grid, use RRT
    if len(points) < GRID_SIZE // 5:
        return rrt_strategy(bot, grid, points, bots)
    
    # For very open spaces with few obstacles, use JPS
    if len(bots) < GRID_SIZE // 4:
        return jps_strategy(bot, grid, points, bots)
    
    # Default to A* which works well in most cases
    return a_star_strategy(bot, grid, points, bots)

# ----------------- Best_First_strategy -----------------
def best_first_strategy(bot, grid, points, bots):
    """Best-First Search: 只用啟發式排序"""
    if not points:
        return 0, 0
    start = (bot.x, bot.y)
    goal = min(points, key=lambda pt: manhattan_distance(start, pt))
    heap = []
    heapq.heappush(heap, (manhattan_distance(start, goal), start, []))
    visited = set()
    occupied = get_occupied_positions(bots, bot)
    while heap:
        h, curr, path = heapq.heappop(heap)
        if curr == goal:
            return path[0] if path else (0, 0)
        if curr in visited:
            continue
        visited.add(curr)
        x, y = curr
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in occupied and (nx, ny) not in visited:
                heapq.heappush(heap, (manhattan_distance((nx, ny), goal), (nx, ny), path+[(dx,dy)]))
    return 0, 0

# ----------------- Weighted_A_Star_strategy -----------------
def weighted_a_star_strategy(bot, grid, points, bots, weight=2.0):
    """Weighted A*: 啟發式乘權重，速度快但不一定最短路"""
    if not points:
        return 0, 0
    start = (bot.x, bot.y)
    goal = min(points, key=lambda pt: manhattan_distance(start, pt))
    heap = []
    heapq.heappush(heap, (0, 0, start, []))
    visited = set()
    occupied = get_occupied_positions(bots, bot)
    while heap:
        f, g, curr, path = heapq.heappop(heap)
        if curr == goal:
            return path[0] if path else (0, 0)
        if curr in visited:
            continue
        visited.add(curr)
        x, y = curr
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and ((nx, ny) not in occupied or (nx, ny) == goal):
                if (nx, ny) not in visited:
                    new_path = path+[(dx,dy)]
                    g2 = len(new_path)
                    h = manhattan_distance((nx,ny), goal)
                    heapq.heappush(heap, (g2+weight*h, g2, (nx,ny), new_path))
    return 0, 0

# ----------------- Wall_Follower_strategy -----------------
class WallFollowerBot:
    def __init__(self):
        self.last_direction = (0, 1)  # 初始方向：向上

def wall_follower_strategy(bot, grid, points, bots):
    if not hasattr(bot, 'last_direction'):
        bot.last_direction = (0, 1)  # 初始化方向

    # 定義方向的相對右轉順序（右手法則）
    directions_order = {
        (0, 1): [(1, 0), (0, 1), (-1, 0), (0, -1)],   # 當前向上 → 優先嘗試右轉
        (1, 0): [(0, -1), (1, 0), (0, 1), (-1, 0)],    # 當前向右 → 優先嘗試向下
        (0, -1): [(-1, 0), (0, -1), (1, 0), (0, 1)],    # 當前向下 → 優先嘗試左轉
        (-1, 0): [(0, 1), (-1, 0), (0, -1), (1, 0)]     # 當前向左 → 優先嘗試向上
    }

    occupied = get_occupied_positions(bots)
    
    # 根據上一次方向，取得優先級順序
    for dx, dy in directions_order[bot.last_direction]:
        nx, ny = bot.x + dx, bot.y + dy
        if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and 
            (nx, ny) not in occupied):
            bot.last_direction = (dx, dy)  # 記住當前方向
            return dx, dy
    
    return 0, 0  # 無路可走