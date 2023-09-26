using System.Drawing;
using System.Xml.Serialization;

namespace WinFormsApp1
{
	public partial class Form1 : Form
	{
		Bitmap bitmapImage;
		List<Pixel> pixels;
		public Form1()
		{
			InitializeComponent();
		}

		private void splitContainer1_SplitterMoved(object sender, SplitterEventArgs e)
		{
			///
		}

		private void oppenToolStripMenuItem_Click(object sender, EventArgs e) //окно выбора картинки
			if (openFileDialog1.ShowDialog() == DialogResult.OK)
			{
				bitmapImage = new Bitmap(openFileDialog1.FileName);

				pixels = GetPixels(bitmapImage);

				pictureBox1.Image = bitmapImage;
			}
		}

		private void button1_Click(object sender, EventArgs e) //добавление точек
		{
			Random rnd = new Random();

			for (int y = 0; y < 10000; y++)
			{
				bitmapImage.SetPixel(rnd.Next(bitmapImage.Width - 1), rnd.Next(bitmapImage.Height), Color.Green);
			}

			pictureBox1.Image = bitmapImage;
		}

		private void button2_Click(object sender, EventArgs e) //добавление линий
		{
			Random rnd = new Random();

			int sy = rnd.Next(bitmapImage.Height - 1);
			int sx = rnd.Next(bitmapImage.Width / 2);
			int ex = rnd.Next(bitmapImage.Width);

			for (int y = sy; y < sy + 1; y++)
			{
				for (int x = sx; x < ex; x++)
				{
					bitmapImage.SetPixel(x, y, Color.Green);
				}
			}
			pictureBox1.Image = bitmapImage;

		}

		private void button3_Click(object sender, EventArgs e) //фильтр
		{
			List<Pixel> pixels = new List<Pixel>(8);
			for (int y = 1; y < bitmapImage.Height - 4; y++) //проходим по всем пикселям картинки помимо боковых
			{
				for (int x = 3; x < bitmapImage.Width - 3; x++)
				{
					for (int i = -1; i < 4; i++)
					{
						if (i != 0)
						{
							pixels.Add(new Pixel()
							{
								color = bitmapImage.GetPixel(x, y + i),
								point = new Point(x, y + i)
							});
						}
					}

					for (int i = -2; i < 3; i++)
					{
						if (i != 0)
						{
							pixels.Add(new Pixel()
							{
								color = bitmapImage.GetPixel(x + i, y),
								point = new Point(x + i, y)
							});
						}
					}

					bitmapImage.SetPixel(x, y, Filtr(pixels)); //замена цвета

					pixels.Clear();
				}
			}

			pictureBox1.Image = bitmapImage;
		}

		List<int> array = new List<int>();
		private Color Filtr(List<Pixel> pixels) //замена цвета пикселя 
		{
			array.Clear();

			int i = 0;
			foreach (var item in pixels)
			{
				array.Add(item.color.ToArgb());
			}
			array.Sort();

			if (array.Count % 2 == 1)
			{
				return Color.FromArgb(array[array.Count / 2]);
			}
			else
			{
				int s = (array[array.Count / 2] + array[(array.Count + 1) / 2]) / 2;
				return Color.FromArgb(s);
			}

		}

		private List<Pixel> GetPixels(Bitmap bitmap)//получение пикселя
		{
			var pixels = new List<Pixel>(bitmap.Width * bitmap.Height);

			for (int y = 0; y < bitmap.Height; y++)
			{
				for (int x = 0; x < bitmap.Width; x++)
				{
					pixels.Add(new Pixel()
					{
						color = bitmap.GetPixel(x, y),
						point = new Point() { X = x, Y = y },
					});
				}
			}

			return pixels;
		}
	}
}