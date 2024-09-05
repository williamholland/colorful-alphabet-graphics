import cairo
import random
import string
import math

NUM_RANDOM_LETTERS = 300
outline_width = 5
font_family = "VAGRounded BT"  # Replace with your desired font


drawn_boxes = []  # List to store bounding boxes of drawn letters
def generate_letter_image(target_letter, output_file):
    width, height = 1920, 1080

    palette = [
        (0.95, 0.64, 0.64, 1),
        (0.64, 0.95, 0.64, 1),
        (0.64, 0.64, 0.95, 1),
        (0.95, 0.95, 0.64, 1)
    ]
    
    surface = cairo.SVGSurface(output_file, width, height)
    context = cairo.Context(surface)

    context.set_source_rgba(1, 1, 1, 1)
    context.rectangle(0, 0, width, height)
    context.fill()

    letters = string.ascii_uppercase[:string.ascii_uppercase.index(target_letter)]
    letters = letters + string.ascii_lowercase[:string.ascii_uppercase.index(target_letter)]

    def get_bounding_box(letter, x, y, font_size):
        # Get the extents of the text
        context.set_font_size(font_size)
        extents = context.text_extents(letter)
        width = extents.width
        height = extents.height
        x_bearing = extents.x_bearing
        y_bearing = extents.y_bearing
        return (x + x_bearing, y + y_bearing, width, height)

    def is_overlapping(box1, box2):
        # Check if two boxes overlap (simple AABB collision detection)
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        return not (x1 + w1 < x2 or x1 > x2 + w2 or y1 + h1 < y2 or y1 > y2 + h2)

    def draw_letter(letter, color):
        font_size = random.randint(50, 200)
        context.select_font_face(font_family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        context.set_font_size(font_size)

        # Retry up to 10 times to avoid overlap
        border_padding = 50
        max_loops = 100
        for i in range(max_loops):
            x, y = random.randint(border_padding, width - border_padding), random.randint(border_padding, height - border_padding)
            rotation = random.uniform(0, 2 * math.pi)

            # Calculate bounding box and check for overlap
            box = get_bounding_box(letter, x, y, font_size)
            if any(is_overlapping(box, other_box) for other_box in drawn_boxes):
                if i < (max_loops - 1):
                    if letter != target_letter:
                        break
                else:
                    continue  # Try a new position if it overlaps

            # If no overlap, proceed to draw the letter
            context.save()
            context.translate(x, y)
            if letter != target_letter:
                context.rotate(rotation)
            context.move_to(0, 0)

            # Draw the outline
            context.set_line_width(outline_width)
            context.set_source_rgb(0, 0, 0)  # Black outline
            context.text_path(letter)
            context.stroke_preserve()

            # Fill the letter with color
            context.set_source_rgba(*color)
            context.fill()

            context.restore()
            drawn_boxes.append(box)
            break

    def draw_random_letter():
        letter = random.choice(letters)
        color = random.choice(palette)
        draw_letter(letter, color)

    for _ in range(NUM_RANDOM_LETTERS):
        draw_random_letter()

    # Draw the target letter
    for color in palette:
        draw_letter(target_letter, color)
    
    surface.finish()

# Usage
target_letter = 'O'
generate_letter_image(target_letter, f'letters_image_{target_letter}.svg')
