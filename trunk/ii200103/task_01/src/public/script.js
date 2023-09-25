document.addEventListener('DOMContentLoaded', () => {
  const addNoiseButton = document.getElementById('addNoiseButton')
  const removeNoiseButton = document.getElementById('removeNoiseButton')
  const imageInput = document.getElementById('imageInput')
  const outputImage = document.getElementById('outputImage')
  let fileName = ''

  // Функция для отправки запроса на сервер
  async function sendRequest(url, method, body, headers = {}) {
    try {
      const response = await fetch(url, {
        method,
        headers,
        body,
      })
      if (!response.ok) {
        console.log(response)
        alert('Error')
        throw new Error('Network response was not ok')
      }
      return response.json()
    } catch (error) {
      console.error('Error:', error)
      return null
    }
  }

  // Обработчик для кнопки "Add Noise"
  addNoiseButton.addEventListener('click', async () => {
    if (fileName.length === 0) {
      alert('Error, first choose photo')
      return
    }
    const headers = {
      'Content-Type': 'application/json',
    }

    const noiseLevel = 25 // Уровень шума на фотке

    const data = {
      filename: fileName,
      noiseLevel,
    }

    // const formData
    const response = await sendRequest(
      '/noise',
      'POST',
      JSON.stringify(data),
      headers
    )

    if (response) {
      outputImage.src = `http://${response.link}`
    }
  })

  // Обработчик для кнопки "Remove Noise"
  removeNoiseButton.addEventListener('click', async () => {
    if (fileName.length === 0) {
      alert('Error, first choose photo')
      return
    }

    const headers = {
      'Content-Type': 'application/json',
    }

    const data = {
      filename: fileName,
    }

    // const formData
    const response = await sendRequest(
      '/clear',
      'POST',
      JSON.stringify(data),
      headers
    )

    if (response) {
      outputImage.src = `http://${response.link}`
    }
  })

  // Обработчик для загрузки изображения
  imageInput.addEventListener('change', async () => {
    const file = imageInput.files[0]

    const formData = new FormData()
    formData.append('image', file)

    const response = await sendRequest('/upload', 'POST', formData)

    if (response) {
      outputImage.src = `http://${response.link}`
      fileName = response.filename
    }
  })
})
