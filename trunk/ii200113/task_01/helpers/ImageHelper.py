import random
from PIL import Image

class ImageHelper:
    def noise_image(self, path, broken_pixels_count):
        with Image.open(path) as image:
            image_to_noise = image.copy()
            image_pixels = image_to_noise.load()
            count = 0
            while (count < broken_pixels_count):
                x_coordinate = 0
                y_coordinate = 0
                image_pixels[x_coordinate, y_coordinate] = (0, 0, 0)
                count += 1
            image_to_noise.save(path)

    def median_filter(self, image, progress_handler, kernel_width=1, kernel_height=1):
        image_to_unnoise = image.copy()
        image_width, image_height = image_to_unnoise.size
        image_pixels = image_to_unnoise.load()
        count = 0
        for i in range(image_width):
            for j in range(image_height):
                red_colors = []
                green_colors = []
                blue_colors = []
                for k_j in range(kernel_height):
                    if k_j + j + 1 < image_height:
                        red, green, blue = image_to_unnoise.getpixel((i, k_j + j + 1))
                        red_colors.append(red)
                        green_colors.append(green)
                        blue_colors.append(blue)
                red_colors.sort()
                green_colors.sort()
                blue_colors.sort()
                image_pixels[i, j] = (red_colors[len(red_colors) // 2],green_colors[len(green_colors) // 2],blue_colors[len(blue_colors) // 2])
            count += 1
            progress_handler(int(((count * 100 / (image_width * image_height * 3)) - 0.014) * 1000))
        
        image_to_unnoise.save('images/unnoised_image.png')