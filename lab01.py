import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Imaginator")
        self.root.geometry("600x500")
        self.label_imagine = tk.Label(root)
        self.label_imagine.pack(expand=True)
        
        self.original_img = None

        self.menu_bar = tk.Menu(root)
        
        # Meniul Fișier
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open Image", command=self.open_image)
        self.file_menu.add_command(label="Close Image", command=self.close_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        
        # Meniul Procesare
        self.process_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.process_menu.add_command(label="Conversie Grayscale", command=self.convert_to_grayscale)
        self.process_menu.add_separator()
        self.process_menu.add_command(label="1. Conversie YUV și YCbCr", command=self.convert_yuv_ycbcr)
        self.process_menu.add_command(label="2. Inversa YCbCr -> Canale RGB", command=self.inverse_ycbcr_to_rgb)
        self.process_menu.add_command(label="3. Binarizare Imagine", command=self.binarize_image)
        self.process_menu.add_command(label="4. Centru de Masă", command=self.center_of_mass)
        
        self.process_menu.add_separator()
        
        # --- NOI CERINȚE ---
        self.process_menu.add_command(label="5. Conversie RGB -> HSV", command=self.convert_to_hsv)
        self.process_menu.add_command(label="6. Afișare Histogramă Gri", command=self.show_histogram)
        self.process_menu.add_command(label="7. Moment de ordin 1 (M10, M01)", command=self.moment_ordin_1)
        self.process_menu.add_command(label="8. Moment de ordin 2 (M20, M02, M11)", command=self.moment_ordin_2)
        self.process_menu.add_command(label="9. Matricea de Covarianță", command=self.covariance_matrix)
        self.process_menu.add_command(label="10. Proiecții (Orizontală / Verticală)", command=self.image_projections)

        # Adăugăm meniurile în bara principală
        self.menu_bar.add_cascade(label="Fișier", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Procesare", menu=self.process_menu)
        
        root.config(menu=self.menu_bar)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imagini", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.original_img = Image.open(file_path).convert('RGB')
            self.display_main_image(self.original_img)

    def close_image(self):
        self.label_imagine.config(image="")
        self.label_imagine.image = None
        self.original_img = None

    def display_main_image(self, img_pil):
        img_display = img_pil.copy()
        img_display.thumbnail((550, 450))
        self.tk_img = ImageTk.PhotoImage(img_display)
        self.label_imagine.config(image=self.tk_img)
        self.label_imagine.image = self.tk_img

    def get_rgb_arrays(self):
        if self.original_img is None:
            messagebox.showwarning("Atenție", "Te rog să deschizi o imagine mai întâi!")
            return None, None, None
        img_array = np.array(self.original_img)
        R = img_array[:, :, 0].astype(np.float32)
        G = img_array[:, :, 1].astype(np.float32)
        B = img_array[:, :, 2].astype(np.float32)
        return R, G, B

    # --- Funcții Vechi ---
    def convert_to_grayscale(self):
        R, G, B = self.get_rgb_arrays()
        if R is None: return

        gray1 = ((R + G + B) / 3).astype(np.uint8)
        gray2 = (0.299 * R + 0.587 * G + 0.114 * B).astype(np.uint8)
        min_rgb = np.minimum.reduce([R, G, B])
        max_rgb = np.maximum.reduce([R, G, B])
        gray3 = ((min_rgb + max_rgb) / 2).astype(np.uint8)

        img_res1 = Image.fromarray(gray1, mode='L')
        img_res2 = Image.fromarray(gray2, mode='L')
        img_res3 = Image.fromarray(gray3, mode='L')
        self.show_results("Grayscale", [img_res1, img_res2, img_res3], ["Gray(1)", "Gray(2)", "Gray(3)"])

    def convert_yuv_ycbcr(self):
        R, G, B = self.get_rgb_arrays()
        if R is None: return

        Y = 0.3 * R + 0.6 * G + 0.1 * B
        U = 0.74 * (R - Y) + 0.27 * (B - Y)
        V = 0.48 * (R - Y) + 0.41 * (B - Y)
        U_norm = np.clip(U + 128, 0, 255)
        V_norm = np.clip(V + 128, 0, 255)
        yuv_array = np.stack([Y, U_norm, V_norm], axis=-1).astype(np.uint8)
        yuv_img = Image.fromarray(yuv_array, 'RGB')

        Y_cbcr = 0.299 * R + 0.587 * G + 0.114 * B
        Cb = -0.1687 * R - 0.3313 * G + 0.498 * B + 128
        Cr = 0.498 * R - 0.4187 * G - 0.0813 * B + 128
        ycbcr_array = np.stack([Y_cbcr, np.clip(Cb, 0, 255), np.clip(Cr, 0, 255)], axis=-1).astype(np.uint8)
        ycbcr_img = Image.fromarray(ycbcr_array, 'RGB')

        self.show_results("Conversii Culoare", [yuv_img, ycbcr_img], ["Imagine YUV", "Imagine YCbCr"])

    def inverse_ycbcr_to_rgb(self):
        R_orig, G_orig, B_orig = self.get_rgb_arrays()
        if R_orig is None: return
        Y = 0.299 * R_orig + 0.587 * G_orig + 0.114 * B_orig
        Cb = -0.1687 * R_orig - 0.3313 * G_orig + 0.498 * B_orig + 128
        Cr = 0.498 * R_orig - 0.4187 * G_orig - 0.0813 * B_orig + 128
        R_inv = np.clip(Y + 1.402 * (Cr - 128), 0, 255).astype(np.uint8)
        G_inv = np.clip(Y - 0.34414 * (Cb - 128) - 0.71414 * (Cr - 128), 0, 255).astype(np.uint8)
        B_inv = np.clip(Y + 1.772 * (Cb - 128), 0, 255).astype(np.uint8)
        img_R = Image.fromarray(R_inv, mode='L')
        img_G = Image.fromarray(G_inv, mode='L')
        img_B = Image.fromarray(B_inv, mode='L')
        self.show_results("Canale RGB Inversate", [img_R, img_G, img_B], ["Canal Roșu", "Canal Verde", "Canal Albastru"])

    def binarize_image(self):
        R, G, B = self.get_rgb_arrays()
        if R is None: return
        prag = simpledialog.askinteger("Prag Binarizare", "Introduceți pragul (0-255):", initialvalue=127)
        if prag is None: return
        gray = (0.299 * R + 0.587 * G + 0.114 * B)
        binary_array = np.where(gray >= prag, 255, 0).astype(np.uint8)
        img_binary = Image.fromarray(binary_array, mode='L')
        self.show_results("Imagine Binarizată", [img_binary], [f"Binarizat ({prag})"])

    def center_of_mass(self):
        R, G, B = self.get_rgb_arrays()
        if R is None: return
        prag = simpledialog.askinteger("Prag Binarizare", "Introduceți pragul pentru centru:", initialvalue=127)
        if prag is None: return
        gray = (0.299 * R + 0.587 * G + 0.114 * B)
        binary_array = np.where(gray >= prag, 255, 0).astype(np.uint8)
        y_coords, x_coords = np.nonzero(binary_array == 255)
        if len(x_coords) > 0:
            cx = int(np.mean(x_coords))
            cy = int(np.mean(y_coords))
            result_img = self.original_img.copy()
            draw = ImageDraw.Draw(result_img)
            draw.line((cx - 10, cy, cx + 10, cy), fill="red", width=3)
            draw.line((cx, cy - 10, cx, cy + 10), fill="red", width=3)
            messagebox.showinfo("Rezultat", f"Centrul de masă: X={cx}, Y={cy}")
            self.display_main_image(result_img)
        else:
            messagebox.showwarning("Atenție", "Nu s-au găsit pixeli albi!")

    # --- IMPLEMENTĂRI NOI ---

    # Cerința 1: RGB în HSV
    def convert_to_hsv(self):
        R, G, B = self.get_rgb_arrays()
        if R is None: return
        
        # Normalizare 0-1
        r, g, b = R / 255.0, G / 255.0, B / 255.0
        cmax = np.maximum.reduce([r, g, b])
        cmin = np.minimum.reduce([r, g, b])
        delta = cmax - cmin
        
        # Hue
        h = np.zeros_like(cmax)
        mask_r = (cmax == r) & (delta != 0)
        mask_g = (cmax == g) & (delta != 0)
        mask_b = (cmax == b) & (delta != 0)
        
        h[mask_r] = (60 * ((g[mask_r] - b[mask_r]) / delta[mask_r]) + 360) % 360
        h[mask_g] = (60 * ((b[mask_g] - r[mask_g]) / delta[mask_g]) + 120) % 360
        h[mask_b] = (60 * ((r[mask_b] - g[mask_b]) / delta[mask_b]) + 240) % 360
        
        # Saturation
        s = np.zeros_like(cmax)
        s[cmax != 0] = delta[cmax != 0] / cmax[cmax != 0]
        
        # Value
        v = cmax
        
        # Re-scalare la 0-255 pentru a putea afișa
        H_img = (h / 360.0 * 255).astype(np.uint8)
        S_img = (s * 255).astype(np.uint8)
        V_img = (v * 255).astype(np.uint8)
        
        hsv_array = np.stack([H_img, S_img, V_img], axis=-1)
        hsv_img = Image.fromarray(hsv_array, 'RGB')
        self.show_results("Spatiul HSV", [hsv_img], ["Imagine HSV"])

    # Cerința 2: Histogramă
    def show_histogram(self):
        R, G, B = self.get_rgb_arrays()
        if R is None: return
        gray = (0.299 * R + 0.587 * G + 0.114 * B).astype(np.uint8)
        
        # Calcul histogramă
        hist, _ = np.histogram(gray.flatten(), bins=256, range=(0, 256))
        
        # Creare vizuală histogramă (fără matplotlib)
        hist_img = Image.new('RGB', (256, 200), color='white')
        draw = ImageDraw.Draw(hist_img)
        max_val = max(hist) if max(hist) > 0 else 1
        
        for i in range(256):
            inaltime = int((hist[i] / max_val) * 200)
            draw.line((i, 200, i, 200 - inaltime), fill='black')
            
        self.show_results("Histogramă Imagine Gri", [hist_img], ["Histogramă"])

    # Funcție utilitară pentru Momente / Covarianță (presupune figuri închise pe fundal alb)
    def _get_binary_foreground(self):
        R, G, B = self.get_rgb_arrays()
        if R is None: return None, None
        
        prag = simpledialog.askinteger("Prag extragere obiect", "Prag (obiectul < prag va fi analizat):", initialvalue=127)
        if prag is None: return None, None
        
        gray = (0.299 * R + 0.587 * G + 0.114 * B)
        # 1 pentru obiect, 0 pentru fundal
        binary = np.where(gray < prag, 1, 0)
        y_coords, x_coords = np.nonzero(binary == 1)
        return x_coords, y_coords

    # Cerința 3: Momentul de ordin 1
    def moment_ordin_1(self):
        x, y = self._get_binary_foreground()
        if x is None or len(x) == 0:
            return messagebox.showwarning("Atenție", "Nu s-a găsit obiectul!")
        
        M10 = np.sum(x, dtype=np.float64)
        M01 = np.sum(y, dtype=np.float64)
        messagebox.showinfo("Moment de Ordin 1", f"M10 (suma pe X) = {M10}\nM01 (suma pe Y) = {M01}")

    # Cerința 4: Momentul de ordin 2
    def moment_ordin_2(self):
        x, y = self._get_binary_foreground()
        if x is None or len(x) == 0:
            return messagebox.showwarning("Atenție", "Nu s-a găsit obiectul!")
            
        M20 = np.sum(x**2, dtype=np.float64)
        M02 = np.sum(y**2, dtype=np.float64)
        M11 = np.sum(x * y, dtype=np.float64)
        messagebox.showinfo("Moment de Ordin 2", f"M20 (suma X^2) = {M20}\nM02 (suma Y^2) = {M02}\nM11 (suma X*Y) = {M11}")

    # Cerința 5: Matricea de covarianță
    def covariance_matrix(self):
        x, y = self._get_binary_foreground()
        if x is None or len(x) == 0:
            return messagebox.showwarning("Atenție", "Nu s-a găsit obiectul!")
        
        N = len(x)
        medie_x = np.mean(x)
        medie_y = np.mean(y)
        
        # Calcul momente centrale
        mu20 = np.sum((x - medie_x)**2)
        mu02 = np.sum((y - medie_y)**2)
        mu11 = np.sum((x - medie_x) * (y - medie_y))
        
        cov_xx = mu20 / N
        cov_yy = mu02 / N
        cov_xy = mu11 / N
        
        msg = f"Matricea de Covarianță:\n\n[ {cov_xx:.2f}   {cov_xy:.2f} ]\n[ {cov_xy:.2f}   {cov_yy:.2f} ]"
        messagebox.showinfo("Covarianță", msg)

    # Cerința 6: Proiecția pe Orizontală și Verticală
    def image_projections(self):
        R, G, B = self.get_rgb_arrays()
        if R is None: return
        
        prag = simpledialog.askinteger("Prag extragere", "Prag (sub prag = obiect=1):", initialvalue=127)
        if prag is None: return
        
        gray = (0.299 * R + 0.587 * G + 0.114 * B)
        binary = np.where(gray < prag, 1, 0)
        h_img, w_img = binary.shape
        
        # Proiectie Orizontala -> Suma pixelilor de pe fiecare rând (axa Y a ecranului)
        proj_horiz = np.sum(binary, axis=1) 
        # Proiectie Verticala -> Suma pixelilor de pe fiecare coloană (axa X a ecranului)
        proj_vert = np.sum(binary, axis=0)
        
        # Grafic pentru Proiectia Orizontala (Apare în stânga, bare orizontale)
        img_h = Image.new('RGB', (w_img, h_img), color='white')
        draw_h = ImageDraw.Draw(img_h)
        max_h = max(proj_horiz) if max(proj_horiz) > 0 else 1
        for y in range(h_img):
            val = int((proj_horiz[y] / max_h) * w_img)
            draw_h.line((0, y, val, y), fill='black')
            
        # Grafic pentru Proiectia Verticala (Apare jos, bare verticale)
        img_v = Image.new('RGB', (w_img, h_img), color='white')
        draw_v = ImageDraw.Draw(img_v)
        max_v = max(proj_vert) if max(proj_vert) > 0 else 1
        for x in range(w_img):
            val = int((proj_vert[x] / max_v) * h_img)
            draw_v.line((x, h_img, x, h_img - val), fill='black')

        self.show_results("Proiecții", [img_h, img_v], ["Orizontală (Sumă Linii)", "Verticală (Sumă Coloane)"])

    # --- Afisare ---
    def show_results(self, window_title, images, labels):
        top = tk.Toplevel(self.root)
        top.title(window_title)
        
        display_size = (300, 300)
        top.images = []

        for i, (img, label_text) in enumerate(zip(images, labels)):
            img.thumbnail(display_size)
            tk_img = ImageTk.PhotoImage(img)
            top.images.append(tk_img)
            
            lbl = tk.Label(top, image=tk_img, text=label_text, compound=tk.BOTTOM)
            lbl.grid(row=0, column=i, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()