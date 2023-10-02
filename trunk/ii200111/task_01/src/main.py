from flask import Flask, render_template, request
import cv2
import numpy as np
import base64
import secrets

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app) # Compliant
app.config['WTF_CSRF_ENABLED'] = True # Sensitive

DELIMITER = '@@@@@@@@@@@@@@@@@@@@@@'

def apply_row_median_filter(image, n):
    height, width, _ = image.shape
    filtered_image = np.copy(image)

    for y in range(height):
        for x in range(width):
            start_x = max(x - n // 2, 0)
            end_x = min(x + n // 2, width - 1)
            neighborhood = image[y, start_x:end_x + 1, :]

            print(f'{start_x}\t{end_x}')
            print(f'{x=}\t{y=}')
            print(neighborhood)
            print(DELIMITER)

            filtered_pixel = np.median(neighborhood, axis=0).astype(np.uint8)

            filtered_image[y, x, :] = filtered_pixel

    return filtered_image


def apply_column_median_filter(image, n):
    height, width, _ = image.shape
    filtered_image = np.copy(image)

    for y in range(height):
        for x in range(width):
            start_y = max(y - n // 2, 0)
            end_y = min(y + n // 2, height - 1)
            neighborhood = image[start_y:end_y + 1, x, :]

            print(f'{start_y}\t{end_y}')
            print(f'{x=}\t{y=}')
            print(neighborhood)
            print(DELIMITER)

            filtered_pixel = np.median(neighborhood, axis=0).astype(np.uint8)

            filtered_image[y, x, :] = filtered_pixel

    return filtered_image


def apply_cross_median_filter(image, n):
    height, width, _ = image.shape
    filtered_image = np.copy(image)

    for y in range(height):
        for x in range(width):
            start_x = max(x - n // 2, 0)
            end_x = min(x + n // 2, width - 1)
            start_y = max(y - n // 2, 0)
            end_y = min(y + n // 2, height - 1)

            neighborhood = image[start_y:end_y + 1, start_x:end_x + 1, :]

            print(f'{start_x=}\t{end_x=}\t{start_y}\t{end_y}')
            print(f'{x=}\t{y=}')
            print(f'{len(neighborhood)}\n{neighborhood=}')
            print(DELIMITER)

            filtered_pixel = np.median(neighborhood, axis=(0, 1)).astype(np.uint8)

            filtered_image[y, x, :] = filtered_pixel

    return filtered_image


def generate_noise_image(image, noise_level, noise_quantity):
    noise_image = image.copy()
    height, width, _ = noise_image.shape

    if noise_level == "high":
        noise_quantity *= 1000

    if noise_level == "none":
        return noise_image

    for _ in range(noise_quantity):
        x = secrets.randbelow(width)
        y = secrets.randbelow(height)

        if noise_level == "low":
            color = [0, 255][secrets.randbelow(2)]
        elif noise_level == "medium":
            color = [0, 255][secrets.randbelow(4) > 0]
        else:
            color = [0, 255][secrets.randbelow(2)]

        noise_image[y, x, :] = [color, color, color]

    return noise_image


@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        image = request.files["image"]
        method = request.form["method"]
        n = int(request.form["n"])
        noise_level = request.form["noise-level"]
        noise_quantity = int(request.form["noise-quantity"])

        if image:
            img_data = image.read()
            img_np_array = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_np_array, cv2.IMREAD_COLOR)

            if method == "row":
                filtered_image = apply_row_median_filter(img, n)
            elif method == "column":
                filtered_image = apply_column_median_filter(img, n)
            elif method == "cross":
                filtered_image = apply_cross_median_filter(img, n)

            noise_image = generate_noise_image(img, noise_level, noise_quantity)

            _, original_img_encoded = cv2.imencode(".png", img)  # Encode original image
            original_image_base64 = base64.b64encode(original_img_encoded).decode("utf-8")

            _, noisy_img_encoded = cv2.imencode(".png", noise_image)  # Encode noisy image
            noisy_image_base64 = base64.b64encode(noisy_img_encoded).decode("utf-8")

            _, filtered_img_encoded = cv2.imencode(".png", filtered_image)  # Encode filtered image
            filtered_image_base64 = base64.b64encode(filtered_img_encoded).decode("utf-8")

            return render_template("filtered_image.html", original_image=original_image_base64,
                                   noisy_image=noisy_image_base64, filtered_image=filtered_image_base64)
    else:
        return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
