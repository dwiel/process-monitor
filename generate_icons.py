from PIL import Image, ImageDraw

def create_circle_image(color, filename):
    size = (16, 16)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 15, 15), fill=color)
    image.save(filename, "PNG")

# Create green circle image
create_circle_image("green", "green_circle.png")

# Create red circle image
create_circle_image("red", "red_circle.png")
