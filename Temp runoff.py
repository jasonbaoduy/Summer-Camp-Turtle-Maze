import pygame
import sys
import math

# --- Bounds and duration for success ---
MAX_BOUND = 250
MIN_BOUND = -100
BOUND_DURATION_MS = 10_000  # 10 seconds in milliseconds

# --- Cooling strength (0 < COOLING_RATE < 1) ---
COOLING_RATE = 0.35          # 0.5 exactly cancels linear growth

# --- Runaway-growth model definitions ---
def linear_growth(temp):
    """Linear growth: Δ = temp"""
    return temp

def quadratic_growth(temp):
    """Quadratic growth: Δ = temp^2"""
    return temp ** 2

def cubic_growth(temp):
    """Cubic growth: Δ = temp^3"""
    return temp ** 3

def sinusoidal_growth(temp):
    """Sinusoidal growth: Δ = sin(temp)"""
    return math.sin(temp)

# Map menu choices to runaway models
runaway_models = {
    '1': ('Linear', linear_growth),
    '2': ('Quadratic', quadratic_growth),
    '3': ('Cubic', cubic_growth),
    '4': ('Sinusoidal', sinusoidal_growth),
}

def control_runoff(temp):
    """
   Example of Linear runoff control 
    """
    return -COOLING_RATE * temp

def draw_thermometer(screen, temp):
    THERMO_X, THERMO_Y = screen.get_width()//2 - 25, 50
    THERMO_W, THERMO_H = 50, 400
    BULB_R = 40
    OUTLINE = (200,200,200)
    MERCURY = (200,50,50)

    tube = pygame.Rect(THERMO_X, THERMO_Y, THERMO_W, THERMO_H)
    pygame.draw.rect(screen, OUTLINE, tube, 4)
    bulb_center = (screen.get_width()//2, THERMO_Y + THERMO_H + BULB_R//2)
    pygame.draw.circle(screen, OUTLINE, bulb_center, BULB_R, 4)

    clamped = max(MIN_BOUND, min(MAX_BOUND, temp))
    ratio = (clamped - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    fill_h = int(ratio * THERMO_H)

    if fill_h > 4:
        rect = pygame.Rect(
            THERMO_X + 4,
            THERMO_Y + THERMO_H - fill_h + 4,
            THERMO_W - 8,
            fill_h - 4
        )
        pygame.draw.rect(screen, MERCURY, rect)
    pygame.draw.circle(screen, MERCURY, bulb_center, BULB_R - 4)

def main():
    # --- Terminal menu for runaway model ---
    print("Choose a runaway-growth model:")
    for key, (name, _) in runaway_models.items():
        print(f"  {key}) {name}")
    choice = input("Enter the number of your choice: ").strip()
    if choice not in runaway_models:
        print("Invalid choice—exiting.")
        return

    model_name, runaway_func = runaway_models[choice]
    print(f"\nSelected runaway model: {model_name}")
    print("Thermometer will update once per second.")
    print("Close window or press ESC to quit.\n")

    # --- Pygame setup ---
    pygame.init()
    WIDTH, HEIGHT = 300, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Thermometer")
    clock = pygame.time.Clock()

    # --- Simulation state ---
    temp = 20.0
    step = 0
    update_interval = 1000  # ms
    last_update = pygame.time.get_ticks()
    in_bounds_start = last_update

    print(f"Step {step}: Temperature = {temp:.2f}°C")

    # --- Main loop ---
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT or (evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        now = pygame.time.get_ticks()
        if now - last_update >= update_interval:
            # 1. Runaway increase
            delta = runaway_func(temp)
            temp += delta

            # 2. Cooling adjustment (proportional)
            correction = control_runoff(temp)
            temp += correction

            # 3. Report
            step += 1
            print(f"Step {step}: Temperature = {temp:.2f}°C  "
                  f"(Δrunaway={delta:.2f}, Δcooling={correction:.2f})")

            # 4. Immediate failure if out of bounds
            if temp > MAX_BOUND or temp < MIN_BOUND:
                print("Failed: temperature out of bounds")
                pygame.quit()
                sys.exit()

            # 5. Success if stays in bounds for 10 s
            if now - in_bounds_start >= BOUND_DURATION_MS:
                print("Success: temperature stayed within bounds for 10 seconds")
                pygame.quit()
                sys.exit()

            last_update = now

        # Draw and refresh
        screen.fill((30,30,30))
        draw_thermometer(screen, temp)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
