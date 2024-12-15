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
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=500)
        self.canvas.pack(pady=20)

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
        self.color = "black"
        self.last_x, self.last_y = None, None

        # Bindings
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def choose_color(self):
        """Renk seçme fonksiyonu."""
        self.color = colorchooser.askcolor()[1]

    def paint(self, event):
        """Kanvas üzerinde çizim yapma fonksiyonu."""
        x, y = event.x, event.y
        if self.last_x and self.last_y:
            self.canvas.create_line((self.last_x, self.last_y, x, y), fill=self.color, width=2)
        self.last_x, self.last_y = x, y

    def reset(self, event):
        """Çizim işlemini sıfırlama fonksiyonu."""
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

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Karanlık tema
    ctk.set_default_color_theme("blue")  # Renk teması
    root = ctk.CTk()  # CustomTkinter penceresi
    app = PaintApp(root)
    root.mainloop()
