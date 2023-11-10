from PIL import Image

class ImageHelper:
    def noise_image(path, broken_pixels_count):
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

    def median_filter(image, progress_handler, kernel_height=1):
        image_to_unnoise = image.copy()
        image_width, image_height = image_to_unnoise.size
        image_pixels = image_to_unnoise.load()
        count = 0
        for i in range(image_width):
            for j in range(image_height):
                krasniu_colors = []
                zeleniy_colors = []
                siniu_colors = []
                for k_j in range(kernel_height):
                    if k_j + j + 1 < image_height:
                        krasniu, zeleniy, siniu = image_to_unnoise.getpixel((i, k_j + j + 1))
                        krasniu_colors.append(krasniu)
                        zeleniy_colors.append(zeleniy)
                        siniu_colors.append(siniu)
                krasniu_colors.sort()
                zeleniy_colors.sort()
                siniu_colors.sort()
                image_pixels[i, j] = (krasniu_colors[len(krasniu_colors) // 2],zeleniy_colors[len(zeleniy_colors) // 2],siniu_colors[len(siniu_colors) // 2])
            count += 1
            progress_handler(int(((count * 100 / (image_width * image_height * 3)) - 0.014) * 1000))
        image_to_unnoise.save('images/unnoised_image.png')