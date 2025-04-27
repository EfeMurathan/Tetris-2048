import lib.stddraw as stddraw
from lib.picture import Picture
from lib.color import Color
import os
from game_grid import GameGrid
from tetromino import Tetromino
import random
import time

def start():
    grid_h, grid_w = 20, 12
    canvas_w = 32 * (grid_w + 8)
    canvas_h = 32 * grid_h
    stddraw.setCanvasSize(canvas_w, canvas_h)
    stddraw.setXscale(-0.5, grid_w + 7.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w

    grid = GameGrid(grid_h, grid_w)
    current_tetromino = create_tetromino()
    next_tetromino = create_tetromino()

    grid.current_tetromino = current_tetromino
    grid.next_tetromino = next_tetromino

    game_paused = False

    last_down_time = 0
    down_press_count = 0
    double_press_interval = 0.3

    display_game_menu(grid_h, grid_w)

    while True:
        # --- Key Kontrol ---
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()

            if key_typed == "p":
                game_paused = not game_paused
                time.sleep(0.2)  # Yanlışlıkla iki kere basmayı önlemek için küçük bir bekleme

            if not game_paused:
                if key_typed == "left":
                    current_tetromino.move(key_typed, grid)
                elif key_typed == "right":
                    current_tetromino.move(key_typed, grid)
                elif key_typed == "down":
                    current_time = time.time()
                    if current_time - last_down_time < double_press_interval:
                        down_press_count += 1
                    else:
                        down_press_count = 1

                    last_down_time = current_time

                    if down_press_count == 2:
                        while current_tetromino.move("down", grid):
                            pass
                        down_press_count = 0
                    else:
                        current_tetromino.move("down", grid)

                elif key_typed == "space":
                    while current_tetromino.move("down", grid):
                        pass
                elif key_typed == "up":
                    current_tetromino.rotate(grid)

            stddraw.clearKeysTyped()

        # --- Duruma Göre Ekran Güncelle ---
        if game_paused:
            grid.display()
            draw_pause_screen(grid.grid_width, grid.grid_height)
            stddraw.show(50)

        else:
            success = current_tetromino.move("down", grid)
            if not success:
                tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
                game_over = grid.update_grid(tiles, pos)
                if game_over:
                    grid.display_game_over()
                    break
                current_tetromino = next_tetromino
                grid.current_tetromino = current_tetromino
                next_tetromino = create_tetromino()
                grid.next_tetromino = next_tetromino

            grid.display()
            stddraw.show(50)

    print("Game over")

def draw_pause_screen(grid_w, grid_h):
    stddraw.setPenColor(stddraw.BLACK)
    stddraw.filledRectangle(grid_w / 2 - 3, grid_h / 2 - 1, 6, 2)
    stddraw.setPenColor(stddraw.WHITE)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.text(grid_w / 2, grid_h / 2, "PAUSED")
    stddraw.setFontSize(15)
    stddraw.text(grid_w / 2, grid_h / 2 - 0.8, "Press 'p' to resume")

def create_tetromino():
    tetromino_types = ['I', 'O', 'Z', 'T', 'J', 'L', 'S']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    return Tetromino(random_type)

def display_game_menu(grid_height, grid_width):
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    stddraw.clear(background_color)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = current_dir + "/images/menu_image.png"
    img_center_x, img_center_y = (grid_width + 6.5) / 2, grid_height - 8
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)

    button_w, button_h = grid_width - 1.5, 2
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    stddraw.text(img_center_x, 5, "Click Here to Start the Game")
    stddraw.setFontSize(18)

    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_blc_x <= mouse_x <= button_blc_x + button_w and button_blc_y <= mouse_y <= button_blc_y + button_h:
                break

if __name__ == '__main__':
    start()
