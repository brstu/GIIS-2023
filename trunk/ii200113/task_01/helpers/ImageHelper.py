import random
from PIL import Image

class ImageHelper:
    def noise_image(self, path, broken_pixels_count):
        with Image.open(path) as image:
            image_to_noise_buff = image.copy()
            image_pixels_counter = image_to_noise_buff.load()
            count = 0
            while (count < broken_pixels_count):
                x_coord = random.randint(0, abs(image.size[0] - 1))
                y_coord = random.randint(0, abs(image.size[1] - 1))
                image_pixels_counter[x_coord, y_coord] = (0, 0, 0)
                count += 1
            image_to_noise_buff.save(path)

def get_pixel_colors(image, i, j):
    red_colors = []
    green_colors = [] 
    blue_colors = []
    for k_i in range(kernel_width):
        if k_i + i + 1 < image_width:
            r, g, b = image.getpixel((k_i + i + 1, j))
            red_colors.append(r)
            green_colors.append(g) 
            blue_colors.append(b)
    for k_j in range(kernel_height):
        if k_j + j + 1 < image_height:
            r, g, b = image.getpixel((i, k_j + j + 1))
            red_colors.append(r)
            green_colors.append(g)
            blue_colors.append(b)
    return red_colors, green_colors, blue_colors


def get_median_color(color_list):
    color_list.sort()
    return color_list[len(color_list) // 2]


def median_filter(image, progress_handler, kernel_width=1, kernel_height=1):
    image_copy = image.copy()
    width, height = image_copy.size
    for i in range(width):
        for j in range(height):
            colors = get_pixel_colors(image_copy, i, j)  
            r = get_median_color(colors[0])
            g = get_median_color(colors[1])
            b = get_median_color(colors[2])
            image_copy.putpixel((i, j), (r, g, b))
            count += 1
            progress_handler(count)
        image_copy.save('unnoised_image.png')
        image_to_unnoise_buff = image.copy()
        image_width_buff, image_height_buff = image_to_unnoise_buff.size
        image_pixels_counter = image_to_unnoise_buff.load()
        count = 0
        for i in range(image_width_buff):
            for j in range(image_height_buff):
                red_colors_buff = []
                green_colors_buff = []
                blue_colors_buff = []
                for k_i in range(kernel_width):
                    if k_i + i + 1 < image_width_buff:
                        red, green, blue = image_to_unnoise_buff.getpixel((k_i + i + 1, j))
                        red_colors_buff.append(red)
                        green_colors_buff.append(green)
                        blue_colors_buff.append(blue)
                for k_j in range(kernel_height):
                    if k_j + j + 1 < image_height_buff:
                        red, green, blue = image_to_unnoise_buff.getpixel((i, k_j + j + 1))
                        red_colors_buff.append(red)
                        green_colors_buff.append(green)
                        blue_colors_buff.append(blue)
                red_colors_buff.sort()
                green_colors_buff.sort()
                blue_colors_buff.sort()
                image_pixels_counter[i, j] = (
                    red_colors_buff[len(red_colors_buff) // 2],
                    green_colors_buff[len(green_colors_buff) // 2],
                    blue_colors_buff[len(blue_colors_buff) // 2]
                )
            count += 1
            progress_handler(int(((count * 100 / (image_width_buff * image_height_buff * 3)) - 0.014) * 1000))
        print(count)
        image_to_unnoise_buff.save('images/unnoised_image.png')