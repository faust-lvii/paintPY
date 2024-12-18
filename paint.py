import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import customtkinter as ctk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basit Resim Çizme Uygulaması")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E2E2E")

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="#505050", width=800, height=500)
        self.canvas.pack(pady=20)

        # Bindings for resizing
        self.canvas.bind("<Button-3>", self.start_resize)  # Sağ fare tuşu ile boyut değiştirme başlat
        self.canvas.bind("<B3-Motion>", self.resize_canvas)  # Sağ fare tuşu ile sürükleme
        self.canvas.bind("<ButtonRelease-3>", self.stop_resize)  # Sağ fare tuşu ile bırakma

        # Resizing variables
        self.resizing = False

        # Toolbar
        self.toolbar = ctk.CTkFrame(self.root)
        self.toolbar.pack()

        # Color Button
        self.color_button = ctk.CTkButton(self.toolbar, text="Renk Seç", command=self.choose_color)
        self.color_button.grid(row=0, column=0, padx=5)

        # Clear Button
        self.clear_button = ctk.CTkButton(self.toolbar, text="Temizle", command=self.clear_canvas)
        self.clear_button.grid(row=0, column=1, padx=5)

        # Save Button
        self.save_button = ctk.CTkButton(self.toolbar, text="Kaydet", command=self.save_canvas)
        self.save_button.grid(row=0, column=2, padx=5)

        # Variables
        self.color = "white"
        self.last_x, self.last_y = None, None
        self.drawing = False  # Çizim durumunu takip etmek için bir değişken

        # Bindings
        self.canvas.bind("<Button-1>", self.start_drawing)  # Sol fare tuşu ile çizim başlat
        self.canvas.bind("<B1-Motion>", self.paint)  # Fare hareketi ile çizim yap
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)  # Sol fare tuşu ile bırakma

        self.scale_factor = 1.0  # Yakınlaştırma faktörü

    def choose_color(self):
        """Renk seçme fonksiyonu."""
        self.color = colorchooser.askcolor()[1]

    def paint(self, event):
        """Kanvas üzerinde çizim yapma fonksiyonu."""
        x, y = event.x, event.y
        if self.drawing:  # Çizim yapılıyorsa
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.color, width=2)  # Çizim yap
        self.last_x, self.last_y = x, y

    def start_drawing(self, event):
        """Çizim işlemini başlatma fonksiyonu."""
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def stop_drawing(self, event):
        """Çizim işlemini durdurma fonksiyonu."""
        self.drawing = False
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """Kanvası temizleme fonksiyonu."""
        self.canvas.delete("all")

    def save_canvas(self):
        """Kanvası kaydetme fonksiyonu."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG dosyası", "*.png")])
        if file_path:
            try:
                self.canvas.postscript(file=file_path + ".eps")
                messagebox.showinfo("Başarılı", "Kanvas başarıyla kaydedildi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Kanvas kaydedilemedi: {e}")

    def start_resize(self, event):
        """Boyut değiştirme işlemini başlatma fonksiyonu."""
        self.resizing = True
        self.start_x = event.x
        self.start_y = event.y

    def resize_canvas(self, event):
        """Kanvas boyutunu değiştirme fonksiyonu."""
        if self.resizing:
            new_width = max(100, event.x)  # Minimum genişlik
            new_height = max(100, event.y)  # Minimum yükseklik
            self.canvas.config(width=new_width, height=new_height)

    def stop_resize(self, event):
        """Boyut değiştirme işlemini durdurma fonksiyonu."""
        self.resizing = False

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Karanlık tema
    ctk.set_default_color_theme("blue")  # Renk teması
    root = ctk.CTk()  # CustomTkinter penceresi
    app = PaintApp(root)
    root.mainloop()
