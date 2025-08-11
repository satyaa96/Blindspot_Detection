# blindspot_sim.py
import pygame
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blind Spot Simulation — No overlap, 3 zones")

# Timing / spawn
FPS = 60
SPAWN_INTERVAL_MS = 700
LAST_SPAWN = 0

clock = pygame.time.Clock()

# Vehicle/player sizes
CAR_W, CAR_H = 56, 100
VEH_W, VEH_H = 56, 100

# Player car centered
player = pygame.Rect(WIDTH // 2 - CAR_W // 2, HEIGHT // 2 - CAR_H // 2, CAR_W, CAR_H)

# Blindspot rectangles
BLIND_LEFT = pygame.Rect(player.left - 110, player.bottom - 30, 100, 140)   # rear-left
BLIND_RIGHT = pygame.Rect(player.right + 10, player.bottom - 30, 100, 140)  # rear-right
BLIND_REAR = pygame.Rect(player.left - 10, player.bottom + 10, CAR_W + 20, 120)  # directly behind

# Lanes
LANES_X = [
    player.left - 220,  # far-left
    player.left - 120,  # near-left
    player.right + 120, # near-right
    player.right + 220  # far-right
]

# Vehicles
vehicles = []

# Min gap
MIN_GAP = 160

def can_spawn_in_lane(spawn_rect, lane_index):
    """Check if spawn_rect would collide with any existing vehicle in same lane."""
    for v in vehicles:
        if v["lane"] == lane_index:
            if spawn_rect.colliderect(v["rect"].inflate(0, MIN_GAP)):  # add vertical gap
                return False
    return True

def spawn_vehicle():
    """Spawn vehicle from top or bottom without overlap."""
    for _ in range(8):  # attempts
        lane_idx = random.randrange(len(LANES_X))
        lane_x = LANES_X[lane_idx]
        direction = random.choice(["down", "up"])
        speed = random.uniform(2.5, 4.5)
        
        if direction == "down":
            spawn_y = -VEH_H - random.randint(0, 120)
            veh_rect = pygame.Rect(lane_x, spawn_y, VEH_W, VEH_H)
            if can_spawn_in_lane(veh_rect, lane_idx):
                vehicles.append({"rect": veh_rect, "speed": speed, "lane": lane_idx})
                return
        else:  # from bottom
            spawn_y = HEIGHT + random.randint(0, 120)
            veh_rect = pygame.Rect(lane_x, spawn_y, VEH_W, VEH_H)
            if can_spawn_in_lane(veh_rect, lane_idx):
                vehicles.append({"rect": veh_rect, "speed": -speed, "lane": lane_idx})
                return

def update_vehicles():
    """Move vehicles and remove off-screen ones."""
    for v in vehicles[:]:
        v["rect"].y += v["speed"]
        if v["rect"].top > HEIGHT + 200 or v["rect"].bottom < -200:
            vehicles.remove(v)

def bl_spot_occupied():
    left = any(v["rect"].colliderect(BLIND_LEFT) for v in vehicles)
    right = any(v["rect"].colliderect(BLIND_RIGHT) for v in vehicles)
    rear = any(v["rect"].colliderect(BLIND_REAR) for v in vehicles)
    return left, right, rear

def draw():
    screen.fill((200, 220, 240))  # bg

    # Road
    road_w = 480
    road_left = WIDTH//2 - road_w//2
    pygame.draw.rect(screen, (40, 40, 40), (road_left, 0, road_w, HEIGHT))

    # Lane markers
    for i in range(1, 4):
        x = road_left + i * (road_w / 4)
        for y in range(0, HEIGHT, 28):
            pygame.draw.rect(screen, (220,220,220), (x-2, y, 6, 16))

    # Blindspots
    BLIND_LEFT.topleft = (player.left - 110, player.bottom - 30)
    BLIND_RIGHT.topleft = (player.right + 10, player.bottom - 30)
    BLIND_REAR.topleft = (player.left - 10, player.bottom + 10)

    pygame.draw.rect(screen, (255,180,0), BLIND_LEFT, 3)
    pygame.draw.rect(screen, (255,180,0), BLIND_RIGHT, 3)
    pygame.draw.rect(screen, (255,180,0), BLIND_REAR, 3)

    # Player car
    pygame.draw.rect(screen, (10,100,180), player, border_radius=6)
    font = pygame.font.SysFont(None, 20)
    txt = font.render("YOU", True, (255,255,255))
    screen.blit(txt, (player.centerx - txt.get_width()/2, player.centery - txt.get_height()/2))

    # Vehicles
    for v in vehicles:
        pygame.draw.rect(screen, (40,200,60), v["rect"], border_radius=6)

    # Warnings
    left, right, rear = bl_spot_occupied()
    font_big = pygame.font.SysFont(None, 36, bold=True)
    warnings = []
    if left: warnings.append("LEFT")
    if right: warnings.append("RIGHT")
    if rear: warnings.append("REAR")
    if warnings:
        surf = font_big.render("⚠ " + "  ".join(warnings) + " blind spot!", True, (200,20,20))
        screen.blit(surf, (WIDTH//2 - surf.get_width()//2, 18))

    pygame.display.flip()

def main_loop():
    global LAST_SPAWN
    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        LAST_SPAWN += dt
        if LAST_SPAWN >= SPAWN_INTERVAL_MS:
            spawn_vehicle()
            LAST_SPAWN = 0

        update_vehicles()
        draw()

    pygame.quit()

if __name__ == "__main__":
    main_loop()
