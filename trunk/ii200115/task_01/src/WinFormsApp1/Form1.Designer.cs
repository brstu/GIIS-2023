namespace WinFormsApp1
{
	partial class Form1
	{
		/// <summary>
		///  Required designer variable.
		/// </summary>
		private System.ComponentModel.IContainer components = null;

		/// <summary>
		///  Clean up any resources being used.
		/// </summary>
		/// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
		protected override void Dispose(bool disposing)
		{
			if (disposing && (components != null))
			{
				components.Dispose();
			}
			base.Dispose(disposing);
		}

		#region Windows Form Designer generated code

		/// <summary>
		///  Required method for Designer support - do not modify
		///  the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
			splitContainer1 = new SplitContainer();
			pictureBox1 = new PictureBox();
			menuStrip1 = new MenuStrip();
			fillToolStripMenuItem = new ToolStripMenuItem();
			oppenToolStripMenuItem = new ToolStripMenuItem();
			Button = new Button();
			button2 = new Button();
			button1 = new Button();
			openFileDialog1 = new OpenFileDialog();
			((System.ComponentModel.ISupportInitialize)splitContainer1).BeginInit();
			splitContainer1.Panel1.SuspendLayout();
			splitContainer1.Panel2.SuspendLayout();
			splitContainer1.SuspendLayout();
			((System.ComponentModel.ISupportInitialize)pictureBox1).BeginInit();
			menuStrip1.SuspendLayout();
			SuspendLayout();
			// 
			// splitContainer1
			// 
			splitContainer1.Dock = DockStyle.Fill;
			splitContainer1.IsSplitterFixed = true;
			splitContainer1.Location = new Point(0, 0);
			splitContainer1.Margin = new Padding(3, 4, 3, 4);
			splitContainer1.Name = "splitContainer1";
			// 
			// splitContainer1.Panel1
			// 
			splitContainer1.Panel1.Controls.Add(pictureBox1);
			splitContainer1.Panel1.Controls.Add(menuStrip1);
			// 
			// splitContainer1.Panel2
			// 
			splitContainer1.Panel2.Controls.Add(Button);
			splitContainer1.Panel2.Controls.Add(button2);
			splitContainer1.Panel2.Controls.Add(button1);
			splitContainer1.Size = new Size(914, 600);
			splitContainer1.SplitterDistance = 779;
			splitContainer1.SplitterWidth = 5;
			splitContainer1.TabIndex = 0;
			splitContainer1.SplitterMoved += splitContainer1_SplitterMoved;
			// 
			// pictureBox1
			// 
			pictureBox1.Dock = DockStyle.Fill;
			pictureBox1.Location = new Point(0, 30);
			pictureBox1.Margin = new Padding(3, 4, 3, 4);
			pictureBox1.Name = "pictureBox1";
			pictureBox1.Size = new Size(779, 570);
			pictureBox1.SizeMode = PictureBoxSizeMode.Zoom;
			pictureBox1.TabIndex = 0;
			pictureBox1.TabStop = false;
			// 
			// menuStrip1
			// 
			menuStrip1.ImageScalingSize = new Size(20, 20);
			menuStrip1.Items.AddRange(new ToolStripItem[] { fillToolStripMenuItem });
			menuStrip1.Location = new Point(0, 0);
			menuStrip1.Name = "menuStrip1";
			menuStrip1.Padding = new Padding(7, 3, 0, 3);
			menuStrip1.Size = new Size(779, 30);
			menuStrip1.TabIndex = 1;
			menuStrip1.Text = "menuStrip1";
			// 
			// fillToolStripMenuItem
			// 
			fillToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { oppenToolStripMenuItem });
			fillToolStripMenuItem.Name = "fillToolStripMenuItem";
			fillToolStripMenuItem.Size = new Size(42, 24);
			fillToolStripMenuItem.Text = "Fill";
			// 
			// oppenToolStripMenuItem
			// 
			oppenToolStripMenuItem.Name = "oppenToolStripMenuItem";
			oppenToolStripMenuItem.Size = new Size(128, 26);
			oppenToolStripMenuItem.Text = "Open";
			oppenToolStripMenuItem.Click += oppenToolStripMenuItem_Click;
			// 
			// Button
			// 
			Button.Location = new Point(1, 82);
			Button.Name = "Button";
			Button.Size = new Size(129, 29);
			Button.TabIndex = 2;
			Button.Text = "Filter";
			Button.UseVisualStyleBackColor = true;
			Button.Click += button3_Click;
			// 
			// button2
			// 
			button2.Location = new Point(1, 47);
			button2.Name = "button2";
			button2.Size = new Size(126, 29);
			button2.TabIndex = 1;
			button2.Text = "Create line";
			button2.UseVisualStyleBackColor = true;
			button2.Click += button2_Click;
			// 
			// button1
			// 
			button1.Location = new Point(1, 12);
			button1.Name = "button1";
			button1.Size = new Size(126, 29);
			button1.TabIndex = 0;
			button1.Text = "Create points";
			button1.UseVisualStyleBackColor = true;
			button1.Click += button1_Click;
			// 
			// openFileDialog1
			// 
			openFileDialog1.FileName = "openFileDialog1";
			openFileDialog1.Filter = "Images|*.bmp;*.jpg;*.png;";
			// 
			// Form1
			// 
			AutoScaleDimensions = new SizeF(8F, 20F);
			AutoScaleMode = AutoScaleMode.Font;
			ClientSize = new Size(914, 600);
			Controls.Add(splitContainer1);
			MainMenuStrip = menuStrip1;
			Margin = new Padding(3, 4, 3, 4);
			Name = "Form1";
			Text = "Form1";
			splitContainer1.Panel1.ResumeLayout(false);
			splitContainer1.Panel1.PerformLayout();
			splitContainer1.Panel2.ResumeLayout(false);
			((System.ComponentModel.ISupportInitialize)splitContainer1).EndInit();
			splitContainer1.ResumeLayout(false);
			((System.ComponentModel.ISupportInitialize)pictureBox1).EndInit();
			menuStrip1.ResumeLayout(false);
			menuStrip1.PerformLayout();
			ResumeLayout(false);
		}

		#endregion

		private SplitContainer splitContainer1;
		private PictureBox pictureBox1;
		private MenuStrip menuStrip1;
		private ToolStripMenuItem fillToolStripMenuItem;
		private ToolStripMenuItem oppenToolStripMenuItem;
		private OpenFileDialog openFileDialog1;
		private Button Button;
		private Button button2;
		private Button button1;
	}
}