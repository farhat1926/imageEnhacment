import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageTk
import numpy as np
import cv2
from scipy.ndimage import convolve

class ImageApp:
    def __init__(self, root):
        # komponen GUI
        self.root = root
        self.root.title("Perancangan Citra Digital")
        self.root.geometry("900x800")
        self.root.configure(bg='#72CDF4')

        self.panel = tk.Label(root)
        self.panel.pack(side="top", fill="both", expand="yes")
        self.panel.configure(bg='#319DCB')

        self.btn_open = tk.Button(root, text="Open Image", command=self.open_image, bg='#A4C39B')
        self.btn_open.pack(side="left", padx=10, pady=10)

        # self.btn_open2 = tk.Button(root, text="Open Second Image", command=self.open_second_image, bg='#A4C39B')
        # self.btn_open2.pack(side="left", padx=10, pady=10)

        self.btn_save = tk.Button(root, text="Save Image", command=self.save_image, bg='#A4C39B')
        self.btn_save.pack(side="left", padx=10, pady=10)

        self.btn_enhance = tk.Button(root, text="Enhance Contrast", command=self.enhance_image, bg='#A4C39B')
        self.btn_enhance.pack(side="left", padx=10, pady=10)

        # self.btn_edge = tk.Button(root, text="Edge Detection", command=self.pendeteksi_garis, bg='#A4C39B')
        # self.btn_edge.pack(side="left", padx=10, pady=10)

        # self.btn_pixel_op = tk.Button(root, text="Pixel Operation", command=self.penggabungan_dua_gambar, bg='#A4C39B')
        # self.btn_pixel_op.pack(side="left", padx=10, pady=10)

        self.btn_convolution = tk.Button(root, text="Sharpen Image", command=self.sharpen, bg='#A4C39B')
        self.btn_convolution.pack(side="left", padx=10, pady=10)

        # Slider untuk Adjust Brightness/Color
        self.label_brightness_color = tk.Label(root,  bg='#72CDF4')
        self.label_brightness_color.pack(side="left", padx=10)

        #untuk reduce noice
        self.btn_reduce_noise = tk.Button(root, text="Reduce Noise", command=self.reduce_noise, bg='#A4C39B')
        self.btn_reduce_noise.pack(side="left", padx=10, pady=10)

        self.slider_brightness_color = tk.Scale(root, from_=0, to=100, orient="horizontal", command=self.adjust_brightness_color)
        self.slider_brightness_color.set(50)  # Set slider di tengah (50%)
        self.slider_brightness_color.pack(side="left", padx=10)

        root.bind('<MouseWheel>', self.zoom)
        self.zoom_factor = 1.0
        self.image = None
        self.processed_image = None
        self.second_image = None

    def open_image(self):
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
                self.image = Image.open(file_path)
                self.processed_image = self.image
                self.display_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # def open_second_image(self):
    #     try:
    #         file_path = filedialog.askopenfilename()
    #         if file_path:
    #             self.second_image = Image.open(file_path)
    #     except Exception as e:
    #         messagebox.showerror("Error", str(e))

    def save_image(self):
        try:
            if self.processed_image:
                file_path = filedialog.asksaveasfilename(defaultextension=".png")
                if file_path:
                    self.processed_image.save(file_path)
                    messagebox.showinfo("Image Saved", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def enhance_image(self):
        try:
            if self.image:
                enhancer = ImageEnhance.Contrast(self.image)
                self.processed_image = enhancer.enhance(2)  # Enhance contrast by a factor of 2
                self.display_image(self.processed_image)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # def pendeteksi_garis(self):
    #     try:
    #         if self.image:
    #             img_array = np.array(self.image)
    #             edges = cv2.Canny(img_array, 100, 200)
    #             self.processed_image = Image.fromarray(edges)
    #             self.display_image(self.processed_image)
    #     except Exception as e:
    #         messagebox.showerror("Error", str(e))

    # def penggabungan_dua_gambar(self):
    #     try:
    #         if self.image and self.second_image:
    #             img1 = np.array(self.image.resize((500, 500)))
    #             img2 = np.array(self.second_image.resize((500, 500)))
    #             combined = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
    #             self.processed_image = Image.fromarray(combined)
    #             self.display_image(self.processed_image)
    #     except Exception as e:
    #         messagebox.showerror("Error", str(e))

    def sharpen(self):
        try:
            if self.image:
                img_array = np.array(self.image.convert('L'))
                kernel = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
                convolved = convolve(img_array, kernel)
                self.processed_image = Image.fromarray(convolved)
                self.display_image(self.processed_image)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def adjust_brightness_color(self, value):
        try:
            if self.image:
                factor = int(value) / 50  # Nilai slider 50 = 1.0 (default)
                
                # Adjust brightness
                enhancer_brightness = ImageEnhance.Brightness(self.image)
                brightened_image = enhancer_brightness.enhance(factor)

                # Adjust sharpness
                enhancer_sharpness = ImageEnhance.Sharpness(brightened_image)
                self.processed_image = enhancer_sharpness.enhance(factor)

                self.display_image(self.processed_image)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reduce_noise(self):
        try:
            if self.image:
                self.processed_image = self.image.filter(ImageFilter.MedianFilter(size=3))
                self.display_image(self.processed_image)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_image(self, img):
        try:
            img_resized = img.resize((int(500 * self.zoom_factor), int(700 * self.zoom_factor)), Image.LANCZOS)
            framed_img = ImageOps.expand(img_resized, border=8, fill='white')
            img_tk = ImageTk.PhotoImage(framed_img)
            self.panel.config(image=img_tk, width=200, height=300)
            self.panel.image = img_tk
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def zoom(self, event):
        try:
            if event.delta > 0:
                self.zoom_factor *= 1.1
            else:
                self.zoom_factor /= 1.1
            if self.image:
                self.display_image(self.processed_image or self.image)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ImageApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
