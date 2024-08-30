import cairo


colors = [
    "#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1", "#955251", 
    "#B565A7", "#009B77", "#DD4124", "#D65076", "#45B8AC", "#EFC050", 
    "#5B5EA6", "#9B2335", "#BC243C", "#F7786B", "#DECD3A", "#79C753", 
    "#FF6F61", "#00A591", "#CE3175", "#FFA07A", "#7B68EE", "#00CED1",
    "#F4A460", "#8B0000"
]


# Image size and outline width
image_size = 500
outline_width = 30


# Font settings
font_size = 500
font_family = "VAGRounded BT"  # Replace with your desired font


def make_images(lst, extra_width=0, extra_height=0):
    for i, letter in enumerate(lst):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, image_size+extra_width, image_size+extra_height)
        context = cairo.Context(surface)

        # Set background to transparent
        context.set_source_rgba(1, 1, 1, 0)
        context.paint()

        # Set the font
        context.select_font_face(font_family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(font_size)

        # Get text extents for centering
        text_extents = context.text_extents(letter)
        x_center = (image_size + extra_width - text_extents.width) / 2 - text_extents.x_bearing
        y_center = (image_size + extra_height - text_extents.height) / 2 - text_extents.y_bearing

        # Draw the outline
        context.set_line_width(outline_width)
        context.set_source_rgb(0, 0, 0)  # Black outline
        context.move_to(x_center, y_center)
        context.text_path(letter)
        context.stroke_preserve()

        # Fill the letter with color
        r, g, b = tuple(int(colors[i % len(colors)][j:j+2], 16) / 255.0 for j in (1, 3, 5))
        context.set_source_rgb(r, g, b)
        context.fill()

        # Save image
        surface.write_to_png(f"{letter}.png")


if __name__ == "__main__":
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    pairs = list(zip(list(alphabet), list(lowercase)))
    #make_images(["".join(t) for t in pairs], extra_width=200)
    #make_images(["junk"]*12 + ["Mm"] + ["junk"]*9 + ["Ww"], extra_width=400)
    #make_images(["junk"]*23 + ["X x"] + ["junk"] + ["Z z"], extra_width=300)
    #make_images(["junk"]*23 + ["X x"] + ["junk"] + ["Z z"], extra_width=300)
    #make_images(["junk"]*9 + ["j"] + ["junk"]*6 + ["Q"], extra_height=100)
    make_images(["junk"]*9 + ["Jj"] + ["junk"]*6 + ["Qq"], extra_width=200, extra_height=100)
    #make_images(alphabet)
    #make_images(lowercase)
