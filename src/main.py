import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

image = None
photo = None  # Declare photo globally
num_images = 0

def import_image():
	global image, photo  # Add photo here
	image_path = filedialog.askopenfilename(title="Select image", filetypes=[("Image files", "*.jpg *.png")])  # Open the file explorer
	if image_path:  # If a file is selected
		image = Image.open(image_path)
		image = image.resize((250, 250))
		photo = ImageTk.PhotoImage(image)
		image_label.config(bg='black', image=photo)
		image_label.image = photo
		convertButton.config(state=tk.NORMAL)  # Enable the convertButton
	elif image_path == None:
		convertButton.config(state=tk.DISABLED)  # Disable the convertButton if no file is selected

def convert_image():
	global image, num_images
	num_images += 1

	# Convert image to grayscale and rotate it properly
	new_image = image.convert("L")
	new_image = new_image.rotate(-90)
	new_image = new_image.transpose(Image.FLIP_LEFT_RIGHT)

	# Resize image
	width, height = new_image.size
	aspect_ratio = height / width

	ascii_chars = " .-=+#$@"
	brightness_step = 255 / len(ascii_chars)
	ascii_image = ""

	for x in range(width):
		for y in range(height):
			pixel_brightness = new_image.getpixel((x, y))
			ascii_index = min(int(pixel_brightness / brightness_step), len(ascii_chars) - 1)
			ascii_image += ascii_chars[ascii_index] * 3
		ascii_image += "\n"
	print(ascii_image)

	with open(f'output/text-version({num_images}).txt', 'w') as f:
		f.write(ascii_image)

	char_width = 18
	char_height = 16

	image_width = width * char_width
	image_height = height * char_height

	# Create the output image
	text_image = Image.new("P", (image_width, image_height), color = (0, 0, 0))
	d = ImageDraw.Draw(text_image)
	d.text((0, 0), ascii_image, fill=(255, 255, 255))

	text_image.save(f"output/converted-image({num_images}).png")
	root.destroy()  # debug

root = tk.Tk()
root.geometry("400x400")
root.title("ImageToASCII")

# Calculate the center of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int((screen_width/2) - (400/2))  # 400 is the width of the window
center_y = int((screen_height/2) - (400/2))  # 400 is the height of the window

# Set the position of the window to the center of the screen
root.geometry("+{}+{}".format(center_x, center_y))
root.resizable(width=False, height=False)

frame = tk.Frame(root)
frame.pack(side=tk.BOTTOM, padx=10, pady=10)

importButton = tk.Button(frame, text="Import Image", command=import_image)
convertButton = tk.Button(frame, text="Convert Image", command=convert_image)
image_label = tk.Label(root)  # Create a label to display the image

importButton.pack(side=tk.LEFT)
convertButton.pack(side=tk.LEFT)
image_label.place(relx=0.5, rely=0.45, anchor='center')

root.mainloop()