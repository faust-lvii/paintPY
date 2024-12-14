import tkinter as tk
from tkinter import colorchooser, messagebox, simpledialog, filedialog
import customtkinter as ctk
from PIL import Image, ImageDraw

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resim Çizme Uygulaması")
        
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.pen_color = "black"
        self.eraser_on = False
        self.pen_width = 2
        self.lines = []  # Çizilen çizgileri saklamak için
        self.shapes = []  # Çizilen şekilleri saklamak için
        self.drawing_shape = None  # Çizilen şekil türü

        self.create_widgets()

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_shape)

        # Sayfa boyutunu ayarlamak için
        self.root.geometry("800x600")
        self.root.minsize(400, 300)

    def create_widgets(self):
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.pen_button = ctk.CTkButton(button_frame, text="Kalem", command=self.use_pen)
        self.pen_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.eraser_button = ctk.CTkButton(button_frame, text="Silgi", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.color_button = ctk.CTkButton(button_frame, text="Renk Seç", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.width_button = ctk.CTkButton(button_frame, text="Kalem Kalınlığı", command=self.choose_width)
        self.width_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.undo_button = ctk.CTkButton(button_frame, text="Geri Al", command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.clear_button = ctk.CTkButton(button_frame, text="Temizle", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.rectangle_button = ctk.CTkButton(button_frame, text="Dikdörtgen", command=self.draw_rectangle)
        self.rectangle_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.circle_button = ctk.CTkButton(button_frame, text="Daire", command=self.draw_circle)
        self.circle_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = ctk.CTkButton(button_frame, text="Kaydet", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_button = ctk.CTkButton(button_frame, text="Yükle", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

    def paint(self, event):
        x, y = event.x, event.y
        if self.eraser_on:
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="white", outline="white")
        else:
            line = self.canvas.create_line(x, y, x + 1, y + 1, fill=self.pen_color, width=self.pen_width)
            self.lines.append(line)  # Çizgiyi sakla

    def reset_shape(self, event):
        self.drawing_shape = None

    def use_pen(self):
        self.eraser_on = False
        self.drawing_shape = None

    def use_eraser(self):
        self.eraser_on = True
        self.drawing_shape = None

    def choose_color(self):
        self.pen_color = colorchooser.askcolor()[1]

    def choose_width(self):
        width = simpledialog.askinteger("Kalem Kalınlığı", "Kalem kalınlığını girin (1-10):", minvalue=1, maxvalue=10)
        if width:
            self.pen_width = width

    def undo(self):
        if self.lines:
            self.canvas.delete(self.lines.pop())  # Son çizgiyi sil

    def clear_canvas(self):
        if messagebox.askyesno("Temizle", "Tüm çizimi temizlemek istediğinize emin misiniz?"):
            self.canvas.delete("all")
            self.lines.clear()  # Çizgileri temizle
            self.shapes.clear()  # Şekilleri temizle

    def draw_rectangle(self):
        self.drawing_shape = "rectangle"

    def draw_circle(self):
        self.drawing_shape = "circle"

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas.update()
            self.canvas.postscript(file=file_path.replace('.png', '.eps'))  # EPS formatında kaydet
            img = Image.open(file_path.replace('.png', '.eps'))
            img.save(file_path, 'png')  # PNG formatına dönüştür

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.clear_canvas()  # Önce tuvali temizle
            img = Image.open(file_path)
            img = img.resize((800, 600), Image.ANTIALIAS)  # Resmi boyutlandır
            self.canvas.image = img
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

if __name__ == "__main__":
    root = ctk.CTk()
    app = PaintApp(root)
    root.mainloop()