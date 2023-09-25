const Jimp = require('jimp')

const refRGB = (width, height, rgbArray) => {
  try {
    // Создаем новый массив для хранения результирующих значений
    const resultArray = []

    // Проходим по высоте (строкам)
    for (let i = 0; i < height; ++i) {
      const newRow = []

      // Проходим по ширине (пикселям) для текущей строки
      for (let j = 0; j < width; ++j) {
        const newPixel = []

        // Проходим по каналам цвета (R, G, B)
        for (let k = 0; k < 3; ++k) {
          // Собираем значения пикселей в окне 3x3
          const neighbors = []
          for (let x = -1; x <= 1; ++x) {
            for (let y = -1; y <= 1; ++y) {
              // Учитываем граничные условия
              const neighborX = Math.min(Math.max(j + x, 0), width - 1)
              const neighborY = Math.min(Math.max(i + y, 0), height - 1)
              neighbors.push(rgbArray[neighborY][neighborX][k])
            }
          }

          // Вычисляем новое значение пикселя
          newPixel[k] = centPixel(rgbArray[i][j][k], neighbors, threshold)
        }

        newRow.push(newPixel)
      }

      resultArray.push(newRow)
    }

    return resultArray
  } catch (err) {
    console.log(err.message)
  }
}

const centPixel = (number1, neighbors, threshold) => {
  /*
  reduce суммирует значения в массиве neighbors и делит на 9
  т.к маска у нас [1 1 1]
                  [1 1 1]
                  [1 1 1]
  */
  const sum = neighbors.reduce((acc, val) => acc + val, 0) / 9
  // Сравниваем значение пикселя по модулю с порогом
  if (Math.abs(number1 - sum) > threshold) {
    return sum
  }
  return number1
}

const addNoise = async (path, probability) => {
  const image = await Jimp.read(path)
  const width = image.bitmap.width
  const height = image.bitmap.height

  const size = width * height
  const count = Math.floor((size * probability) / 100)

  for (let i = 0; i < count; i++) {
    // Рандомим значения белых пикселей на фотке с размеров фото
    const x = Math.floor(Math.random() * width)
    const y = Math.floor(Math.random() * height)
    const color = Jimp.rgbaToInt(255, 255, 255, 255) // Белый цвет

    image.setPixelColor(color, x, y)
  }

  return image
}

const threshold = 128 // порог
const noiseLevel = 25 // уровень шума на фотке

const removeNoise = async (path) => {
  const image = await Jimp.read(path)

  const width = image.getWidth()
  const height = image.getHeight()

  // Получаем RGB данные из изображения
  let rgbArray = []

  for (let y = 0; y < height; y++) {
    const row = []
    for (let x = 0; x < width; x++) {
      const pixel = Jimp.intToRGBA(image.getPixelColor(x, y))
      row.push([pixel.r, pixel.g, pixel.b])
    }
    rgbArray.push(row)
  }

  // Применяем фильтр
  rgbArray = refRGB(width, height, rgbArray)

  // Создаем новое изображение
  const newImage = new Jimp(width, height)

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const [r, g, b] = rgbArray[y][x]
      const color = Jimp.rgbaToInt(r, g, b, 255)
      newImage.setPixelColor(color, x, y)
    }
  }

  // Отправляем новое изображение
  return newImage
}

module.exports = {
  addNoise,
  removeNoise,
}
