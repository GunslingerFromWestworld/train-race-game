import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TRACK_CENTER_X = WINDOW_WIDTH // 2
TRACK_CENTER_Y = WINDOW_HEIGHT // 2
TRACK_RADIUS = 250
TRAIN_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

class Train:
    def __init__(self, color, name, speed, start_angle=0):
        self.color = color
        self.name = name
        self.speed = speed  # degrees per frame
        self.angle = start_angle  # current position on track (in degrees)
        self.laps = 0
        self.last_angle = start_angle
        
    def update(self):
        """Update train position"""
        self.last_angle = self.angle
        self.angle += self.speed
        
        # Check for lap completion
        if self.last_angle < 360 and self.angle >= 360:
            self.laps += 1
        
        # Keep angle in 0-360 range
        self.angle = self.angle % 360
    
    def get_position(self):
        """Get x, y coordinates on the circular track"""
        rad = math.radians(self.angle)
        x = TRACK_CENTER_X + TRACK_RADIUS * math.cos(rad)
        y = TRACK_CENTER_Y + TRACK_RADIUS * math.sin(rad)
        return x, y
    
    def get_relative_speed_to(self, other_train):
        """Calculate relative speed compared to another train"""
        return self.speed - other_train.speed

def draw_track(screen):
    """Draw the circular track"""
    # Outer track boundary
    pygame.draw.circle(screen, WHITE, (TRACK_CENTER_X, TRACK_CENTER_Y), TRACK_RADIUS + 30, 3)
    # Inner track boundary
    pygame.draw.circle(screen, WHITE, (TRACK_CENTER_X, TRACK_CENTER_Y), TRACK_RADIUS - 30, 3)
    # Center line
    pygame.draw.circle(screen, GRAY, (TRACK_CENTER_X, TRACK_CENTER_Y), TRACK_RADIUS, 2)
    
    # Start/finish line
    start_x = TRACK_CENTER_X + TRACK_RADIUS - 30
    end_x = TRACK_CENTER_X + TRACK_RADIUS + 30
    pygame.draw.line(screen, YELLOW, (start_x, TRACK_CENTER_Y), (end_x, TRACK_CENTER_Y), 5)

def draw_train(screen, train):
    """Draw a train on the track"""
    x, y = train.get_position()
    pygame.draw.circle(screen, train.color, (int(x), int(y)), TRAIN_SIZE)
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), TRAIN_SIZE, 2)

def draw_info_panel(screen, train1, train2, font):
    """Draw information panel showing speeds and relative speeds"""
    info_y = 50
    line_height = 30
    
    # Title
    title_text = font.render("Train Race - Relative Speed Demonstration", True, WHITE)
    screen.blit(title_text, (20, 20))
    
    # Train 1 info
    train1_info = [
        f"Red Train: {train1.speed:.1f}°/frame",
        f"Laps: {train1.laps}",
        f"Position: {train1.angle:.1f}°"
    ]
    
    # Train 2 info
    train2_info = [
        f"Blue Train: {train2.speed:.1f}°/frame", 
        f"Laps: {train2.laps}",
        f"Position: {train2.angle:.1f}°"
    ]
    
    # Relative speed info
    relative_speed = train1.get_relative_speed_to(train2)
    relative_info = [
        f"Relative Speed (Red vs Blue): {relative_speed:.1f}°/frame",
        f"Red is {'faster' if relative_speed > 0 else 'slower' if relative_speed < 0 else 'same speed'} than Blue"
    ]
    
    # Draw all info
    all_info = train1_info + [""] + train2_info + [""] + relative_info
    
    for i, text in enumerate(all_info):
        if text:  # Skip empty strings
            color = RED if i < 3 else BLUE if i < 7 else GREEN
            info_text = font.render(text, True, color)
            screen.blit(info_text, (20, info_y + i * line_height))

def draw_controls(screen, font):
    """Draw control instructions"""
    controls = [
        "Controls:",
        "1/2 - Adjust Red Train Speed",
        "3/4 - Adjust Blue Train Speed", 
        "R - Reset Race",
        "ESC - Quit"
    ]
    
    start_y = WINDOW_HEIGHT - 150
    for i, text in enumerate(controls):
        color = YELLOW if i == 0 else WHITE
        control_text = font.render(text, True, color)
        screen.blit(control_text, (20, start_y + i * 25))

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Train Race - Relative Speed Demo")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    # Create trains with different speeds
    train1 = Train(RED, "Red Express", 2.0, 0)      # 2 degrees per frame
    train2 = Train(BLUE, "Blue Lightning", 1.5, 180) # 1.5 degrees per frame, starting opposite
    
    running = True
    paused = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:  # Decrease red train speed
                    train1.speed = max(0.1, train1.speed - 0.1)
                elif event.key == pygame.K_2:  # Increase red train speed
                    train1.speed = min(5.0, train1.speed + 0.1)
                elif event.key == pygame.K_3:  # Decrease blue train speed
                    train2.speed = max(0.1, train2.speed - 0.1)
                elif event.key == pygame.K_4:  # Increase blue train speed
                    train2.speed = min(5.0, train2.speed + 0.1)
                elif event.key == pygame.K_r:  # Reset race
                    train1.angle = 0
                    train1.laps = 0
                    train2.angle = 180
                    train2.laps = 0
                elif event.key == pygame.K_SPACE:  # Pause/unpause
                    paused = not paused
        
        if not paused:
            # Update train positions
            train1.update()
            train2.update()
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw everything
        draw_track(screen)
        draw_train(screen, train1)
        draw_train(screen, train2)
        draw_info_panel(screen, train1, train2, font)
        draw_controls(screen, font)
        
        # Show pause indicator
        if paused:
            pause_text = font.render("PAUSED - Press SPACE to continue", True, YELLOW)
            screen.blit(pause_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2))
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
