const express = require('express')
const fileUpload = require('express-fileupload')
const path = require('path')
const bodyParser = require('body-parser')

const { addNoise, removeNoise } = require('./utils')

const app = express()

const PORT = 3000 // Порт, на котором будет работать сервер

app.use(fileUpload())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())
app.use(express.static('public')) // Папка для статических файлов (HTML, CSS, JS)
app.use('/images', express.static(__dirname + '/public/images'))
// Путь для фото изображений

// Обработка POST запроса для удаления шума
app.post('/upload', async (req, res) => {
  try {
    if (!req.files) {
      return res.status(400).send('Error')
    }
    const uploadedFile = req.files.image
    const filePath = path.join(__dirname, 'public/images', uploadedFile.name)

    uploadedFile.mv(filePath)

    return res.status(200).json({
      link: `localhost:${PORT}/images/${uploadedFile.name}`,
      filename: uploadedFile.name,
    })
  } catch (e) {
    res.status(400).json({ message: e.message })
  }
})

app.post('/noise', async (req, res) => {
  try {
    if (!req.body.filename) {
      return res.status(400).send('Error')
    }

    const { filename, noiseLevel } = req.body
    const filePath = path.join(__dirname, 'public/images', filename)

    const noiseImage = await addNoise(filePath, noiseLevel)

    const noiseImagePath = path.join(
      __dirname,
      'public/images',
      `noise_${filename}`
    )

    await noiseImage.writeAsync(noiseImagePath)

    return res.status(200).json({
      link: `localhost:${PORT}/images/noise_${filename}`,
    })
  } catch (e) {
    res.status(400).json({ message: e.message })
  }
})

app.post('/clear', async (req, res) => {
  try {
    if (!req.body.filename) {
      return res.status(400).send('Error')
    }

    const { filename } = req.body
    const filePath = path.join(__dirname, 'public/images', `noise_${filename}`)

    const clearImage = await removeNoise(filePath)

    const clearImagePath = path.join(
      __dirname,
      'public/images',
      `clear_${filename}`
    )

    await clearImage.writeAsync(clearImagePath)

    return res.status(200).json({
      link: `localhost:${PORT}/images/clear_${filename}`,
    })
  } catch (e) {
    res.status(400).json({ message: e.message })
  }
})

// Запуск сервера
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`)
})
