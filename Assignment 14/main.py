import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os


class OpenCVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenCV Image Editor")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)
        self.image_path = None
        self.original_image = None
        self.processed_image = None

        self.build_ui()

    def build_ui(self):
        # Title Label
        title = ttk.Label(self.root, text="OpenCV Assignment App", font=("Helvetica", 18, "bold"))
        title.pack(pady=10)

        # Canvas Area
        self.canvas_frame = ttk.Frame(self.root, padding=10)
        self.canvas_frame.pack()
        self.canvas = ttk.Label(self.canvas_frame, borderwidth=2, relief="solid")
        self.canvas.pack()

        # Button Area
        self.btn_frame = ttk.Frame(self.root, padding=10)
        self.btn_frame.pack(pady=20)

        ttk.Button(self.btn_frame, text="Load Image", command=self.load_image, width=15).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.btn_frame, text="Grayscale", command=self.to_grayscale, width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.btn_frame, text="Blur", command=self.blur_image, width=15).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.btn_frame, text="Edge Detect", command=self.edge_detection, width=15).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(self.btn_frame, text="Reset", command=self.reset_image, width=15).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(self.btn_frame, text="Save", command=self.save_image, width=15).grid(row=0, column=5, padx=5, pady=5)

        # Status Bar
        self.status = ttk.Label(self.root, text="Status: Ready", relief=tk.SUNKEN, anchor='w')
        self.status.pack(fill='x', side='bottom')

    def update_status(self, message):
        self.status.config(text=f"Status: {message}")
        self.status.update_idletasks()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return
        self.image_path = file_path
        self.original_image = cv2.imread(file_path)
        self.processed_image = self.original_image.copy()
        self.display_image(self.processed_image)
        self.update_status("Image loaded.")

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((700, 500),  Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.canvas.img_tk = img_tk
        self.canvas.config(image=img_tk)

    def to_grayscale(self):
        if self.processed_image is not None:
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image)
            self.update_status("Converted to Grayscale.")

    def blur_image(self):
        if self.processed_image is not None:
            blur = cv2.GaussianBlur(self.processed_image, (15, 15), 0)
            self.processed_image = blur
            self.display_image(self.processed_image)
            self.update_status("Image blurred.")

    def edge_detection(self):
        if self.processed_image is not None:
            edges = cv2.Canny(self.processed_image, 100, 200)
            self.processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image)
            self.update_status("Edge detection applied.")

    def reset_image(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.display_image(self.processed_image)
            self.update_status("Image reset.")

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("Saved", "Image saved successfully!")
                self.update_status("Image saved.")


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")  # Modern theme
    app = OpenCVApp(root)
    root.mainloop()
