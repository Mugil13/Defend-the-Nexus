from raylibpy import *
import heapq

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800

map_data = [
    [2, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
    [4, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4],
    [4, 4, 4, 1, 4, 1, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1],
    [0, 0, 4, 1, 1, 1, 4, 0, 0, 0, 0, 0, 4, 4, 4, 1],
    [0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 1, 1, 1, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 1, 1, 4, 4, 4, 0],
    [0, 0, 0, 0, 0, 4, 4, 4, 4, 1, 1, 4, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 1, 1, 1, 1, 4, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 1, 4, 4, 4, 4, 4, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 1, 1, 1, 1, 1, 1, 4, 4, 0, 0],
    [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 1, 1, 1, 3],
]
pos=[]
for i in range(len(map_data)):
    for j in range(len(map_data[0])):
        if map_data[i][j]==4:
            pos.append((i,j))
print(pos)

rows = len(map_data)
cols = len(map_data[0])

tileheight = SCREEN_HEIGHT // rows
tilewidth = SCREEN_WIDTH // cols


def possible_pos(pos):
    x=pos[0]
    y=pos[1]

    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)]


def astar(map_data):
    start = None
    end = None
    for r, row in enumerate(map_data):
        for c, value in enumerate(row):
            if value == 2:
                start = (r, c)
            elif value == 3:
                end = (r, c)
    
    if start is None or end is None:
        return None  
    
    rows, cols = len(map_data), len(map_data[0])
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end), 0, start))  
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while open_set:
        _, current_g, current = heapq.heappop(open_set)  
        
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  
        
        
        for d in directions:
            neighbor = (current[0] + d[0], current[1] + d[1])
            
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and map_data[neighbor[0]][neighbor[1]] != 0 and map_data[neighbor[0]][neighbor[1]] != 4:
                tentative_g_score = current_g + 1
                
                
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    
                   
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor)) 
    
    return None 


class Turret:
    def __init__(self, position):
        self.position = position 
        self.attack_cooldown = 90  
        self.attack_timer = 90
        self.hitpos=possible_pos(position)
        self.damage=0
        self.kills=0

    def update(self, enemies):
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            for enemy in enemies:
                if enemy.position in self.hitpos:
                    self.damage+=3
                    enemy.health -= 3
                    if enemy.health<=0:
                        self.kills+=1 
                    self.attack_timer = 0  
                    break

    def draw(self):
        row, col = self.position
        center_x = (col * tilewidth) + (tilewidth // 2)
        center_y = (row * tileheight) + (tileheight // 2)
        radius = min(tilewidth, tileheight) // 3 
        draw_circle(center_x, center_y, radius, RED)


class Enemy:
    def __init__(self, path, slowdown_factor=10):
        self.path = path
        self.position = path[0]
        self.index = 0
        self.frame_counter = 0
        self.slowdown_factor = slowdown_factor
        self.health = 10
        self.color=BLUE

    def update(self):
        if self.index < len(self.path) - 1:
            self.frame_counter += 1
            if self.frame_counter >= self.slowdown_factor:
                self.index += 1
                self.position = self.path[self.index]
                self.frame_counter = 0
        if self.position==self.path[-1]:
            enemies.remove(self)
        if self.health<=0:
            enemies.remove(self)

    def draw(self):
        row, col = self.position
        center_x = (col * tilewidth) + (tilewidth // 2)
        center_y = (row * tileheight) + (tileheight // 2)
        radius = min(tilewidth, tileheight) // 4  
        if self.health==10:
            self.color=BLUE
        elif self.health==7:
            self.color=YELLOW
        elif self.health==4:
            self.color =PINK
        else:
            self.color =BLACK        
        draw_circle(center_x, center_y, radius, self.color)


def draw_map():
    for row in range(rows):
        for col in range(cols):
            if map_data[row][col] == 0 :
                color = GREEN
            elif map_data[row][col] == 1:
                color = BROWN
            elif map_data[row][col] == 2 or map_data[row][col] == 3:
                color = RED
            elif map_data[row][col] == 4:
                color = DARKGRAY
            
            draw_rectangle(col * tilewidth, row * tileheight, tilewidth, tileheight, color)


init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "TOWER DEFENSE")
set_target_fps(60)

turrets = []
enemies = []
maxenemies=10
enemycount=0
spawn_timer = 0
spawn_interval = 60

while not window_should_close():
    mouse_x, mouse_y = get_mouse_x(), get_mouse_y()
    row, col = mouse_y // tileheight, mouse_x // tilewidth


    if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and 0 <= row < rows and 0 <= col < cols and len(turrets)<5:
        if map_data[row][col] == 4:  
            turrets.append(Turret((row, col)))


    spawn_timer += 1
    if spawn_timer >= spawn_interval and enemycount<maxenemies :
        path = astar(map_data)
        enemies.append(Enemy(path))
        spawn_timer = 0
        enemycount+=1
    
    

    begin_drawing()
    clear_background(RAYWHITE)

    draw_map()

    for enemy in enemies:
        
        enemy.update()
        enemy.draw()
       


    for turret in turrets:
        turret.update(enemies)
        turret.draw()

    if len(enemies)==0 and enemycount!=0:
        end_drawing()
        totalkills=0
        totaldamage=0
        output=[]

        for turret in turrets:
            tdir={}
            tdir["position"]=turret.position
            tdir["kills"]=turret.kills
            tdir["damage"]=turret.damage
            totaldamage+=turret.damage
            totalkills+=turret.kills
            output.append(tdir)
        output.append(totaldamage)
        output.append(totalkills)
        print(output)
        break
    end_drawing()

close_window()
