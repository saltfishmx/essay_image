import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog
from PIL import Image, ImageTk, ImageDraw
import os


class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_click)

        self.load_button = tk.Button(root, text="Load Images", command=self.load_images)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(root, text="Save Cropped", command=self.save_cropped_images)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.color_button = tk.Button(root, text="Choose Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.size_entry_button = tk.Button(root, text="Set Size", command=self.set_size)
        self.size_entry_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.rect_color = "red"
        self.rect_width = 3
        self.rect_size = 100  # Default size
        self.saved_times = 0

        self.file_paths = []
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.cur_img = None
        self.crop_area = None
        self.saved_rectangle = None
        self.saved_rectangles = []
        self.unsaved_rectangle_id = []

    def load_images(self):
        self.file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if not self.file_paths:
            return
        img = Image.open(self.file_paths[0])
        self.cur_img = img
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_click(self, event):
        for i in self.unsaved_rectangle_id:
            self.canvas.delete(i)
        self.unsaved_rectangle_id.clear()
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x + self.rect_size, self.start_y + self.rect_size,
                                                 outline=self.rect_color, width=self.rect_width)
        self.unsaved_rectangle_id.append(self.rect)
        self.crop_area = (self.start_x, self.start_y, self.start_x + self.rect_size, self.start_y + self.rect_size)
        self.saved_rectangle = (self.crop_area, self.rect_color, self.rect_width)

    def save_cropped_images(self):
        self.saved_rectangles.append(self.saved_rectangle)
        if not self.saved_rectangles:
            messagebox.showerror("Error", "No area selected for cropping.")
            return
        self.saved_times += 1
        save_dir = os.path.join("Cropped_Images", str(self.saved_times))
        os.makedirs(save_dir, exist_ok=True)

        marked_img = self.cur_img.copy()
        draw = ImageDraw.Draw(marked_img)

        for rect, color, width in self.saved_rectangles:
            draw.rectangle(rect, outline=color, width=width)

        for path in self.file_paths:
            img = Image.open(path)
            cropped_img = img.crop(self.crop_area)
            cropped_img = cropped_img.resize((512, 512), Image.LANCZOS)
            cropped_img.save(os.path.join(save_dir, f"Cropped_{os.path.basename(path)}"))

        marked_img.save(os.path.join(save_dir, "Original_with_box.png"))
        self.unsaved_rectangle_id.clear()

    def set_size(self):
        size = simpledialog.askinteger("Size Input", "Enter the size of the square (pixels):", minvalue=1, maxvalue=1000)
        if size:
            self.rect_size = size

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Rectangle Color")
        if color_code[1]:
            self.rect_color = color_code[1]

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropper(root)
    root.mainloop()
