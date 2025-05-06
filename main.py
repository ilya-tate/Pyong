import pygame

# ILYA TATE

pygame.init()

color = {
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}

# Display window
display_dim = {
    'width': 800,
    'height': 600
}
display = pygame.display.set_mode((display_dim['width'], display_dim['height']))
display.fill(color['black'])
# Icon
icon = pygame.image.load('./assets/game-icon.png')
pygame.display.set_icon(icon)
# Name
pygame.display.set_caption("Pong")

paddles = {
    # How much the paddle moves per keystroke
    'vel': 10,
    # Paddle dimensions
    'width': display_dim['width'] / 24,
    'height': display_dim['height'] / 4,
    # Paddle positions on display
    'pos_left': {
        'x': display_dim['width'] / 8,
        'y': display_dim['height'] / 3
    },
    'pos_right': {
        'x': display_dim['width'] / 1.25,
        'y': display_dim['height'] / 3
    },
}

# Paddle starting positions
paddles['left'] = pygame.draw.rect(display, color['white'], (paddles['pos_left']['x'], paddles['pos_left']['y'], paddles['width'], paddles['height']))
paddles['right'] = pygame.draw.rect(display, color['white'], (paddles['pos_right']['x'], paddles['pos_right']['y'], paddles['width'], paddles['height']))

ball = {
    # How much the ball moves per frame
    'vel': 10,
    # Direction of balls movement in degrees
    'direction': 'left',
    'vel_x': 7,  # Horizontal speed
    'vel_y': 4,  # Vertical speed
    # Ball starting position
    'x': (display_dim['width'] / 2) - (display_dim['width'] / 24),
    'y': (display_dim['height'] / 2) - (display_dim['width'] / 24),
    # Ball dimensions
    'width': display_dim['width'] / 24,
    'height': display_dim['width'] / 24
}

# Score tracking
score = {
    'left': 0,
    'right': 0
}

font = pygame.font.SysFont('Arial', 30)

def reset_ball():
    ball['x'] = (display_dim['width'] / 2) - (ball['width'] / 2)
    ball['y'] = (display_dim['height'] / 2) - (ball['height'] / 2)
    # Alternate starting direction
    # ball['direction'] = 'right' if ball['direction'] == 'left' else 'left'
    ball['vel_x'] *= -1  # switch direction
    ball['vel_y'] = 4  # reset vertical movement


ball_pos = pygame.draw.rect(display, color['white'], pygame.Rect(
    (ball['x'], ball['y']),
    (ball['width'], ball['height'])
))

def move_ball():
    # Clear old ball
    pygame.draw.rect(display, color['black'], pygame.Rect(
        (ball['x'], ball['y']),
        (ball['width'], ball['height'])
    ))

    # Update position
    ball['x'] += ball['vel_x']
    ball['y'] += ball['vel_y']

    # Bounce off top/bottom
    if ball['y'] <= 0 or ball['y'] + ball['height'] >= display_dim['height']:
        ball['vel_y'] *= -1

    # Bounce off left paddle
    if (ball['x'] <= paddles['pos_left']['x'] + paddles['width'] and
        paddles['pos_left']['y'] <= ball['y'] + ball['height'] and
        ball['y'] <= paddles['pos_left']['y'] + paddles['height']):
        ball['vel_x'] *= -1
        offset = (ball['y'] + ball['height']/2) - (paddles['pos_left']['y'] + paddles['height']/2)
        ball['vel_y'] = offset / (paddles['height']/2) * 5  # vertical angle change

    # Bounce off right paddle
    if (ball['x'] + ball['width'] >= paddles['pos_right']['x'] and
        paddles['pos_right']['y'] <= ball['y'] + ball['height'] and
        ball['y'] <= paddles['pos_right']['y'] + paddles['height']):
        ball['vel_x'] *= -1
        offset = (ball['y'] + ball['height']/2) - (paddles['pos_right']['y'] + paddles['height']/2)
        ball['vel_y'] = offset / (paddles['height']/2) * 5

    # Check for score
    if ball['x'] < 0:
        score['right'] += 1
        reset_ball()
    elif ball['x'] > display_dim['width']:
        score['left'] += 1
        reset_ball()

    # Draw ball and paddles
    pygame.draw.rect(display, color['white'], (ball['x'], ball['y'], ball['width'], ball['height']))
    pygame.draw.rect(display, color['white'], (paddles['pos_left']['x'], paddles['pos_left']['y'], paddles['width'], paddles['height']))
    pygame.draw.rect(display, color['white'], (paddles['pos_right']['x'], paddles['pos_right']['y'], paddles['width'], paddles['height']))

    pygame.display.set_caption(f"Pong | Left: {score['left']}  Right: {score['right']}")

def key_strokes():
    '''
    What happens on each key stroke
    '''

    keys = pygame.key.get_pressed()

    # Left paddle positioning
    if keys[pygame.K_w] and paddles['pos_left']['y'] > 0:
        paddles['left'] = pygame.draw.rect(display, color['black'], (paddles['pos_left']['x'], paddles['pos_left']['y'], paddles['width'], paddles['height']))
        paddles['pos_left']['y'] -= paddles['vel']
        pygame.draw.rect(display, color['white'], (paddles['pos_left']['x'], paddles['pos_left']['y'], paddles['width'], paddles['height']))
    if keys[pygame.K_s] and paddles['pos_left']['y'] + paddles['height'] < display_dim['height']:
        paddles['left'] = pygame.draw.rect(display, color['black'], (paddles['pos_left']['x'], paddles['pos_left']['y'], paddles['width'], paddles['height']))
        paddles['pos_left']['y'] += paddles['vel']
        pygame.draw.rect(display, color['white'], (paddles['pos_left']['x'], paddles['pos_left']['y'], paddles['width'], paddles['height']))
    
    # Right paddle positioning
    if keys[pygame.K_UP] and paddles['pos_right']['y'] > 0:
        paddles['right'] = pygame.draw.rect(display, color['black'], (paddles['pos_right']['x'], paddles['pos_right']['y'], paddles['width'], paddles['height']))
        paddles['pos_right']['y'] -= paddles['vel']
        pygame.draw.rect(display, color['white'], (paddles['pos_right']['x'], paddles['pos_right']['y'], paddles['width'], paddles['height']))
    if keys[pygame.K_DOWN] and paddles['pos_right']['y'] + paddles['height'] < display_dim['height']:
        paddles['right'] = pygame.draw.rect(display, color['black'], (paddles['pos_right']['x'], paddles['pos_right']['y'], paddles['width'], paddles['height']))
        paddles['pos_right']['y'] += paddles['vel']
        pygame.draw.rect(display, color['white'], (paddles['pos_right']['x'], paddles['pos_right']['y'], paddles['width'], paddles['height']))

def run_game():
    running = True
    frame_time = 50
    while running:
        pygame.time.delay(frame_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key_strokes()
        move_ball()
        pygame.display.update()

run_game()
