# Imaginator - Aplicație Prelucrare Imagini

Aplicație desktop dezvoltată în Python folosind biblioteca **Tkinter** pentru interfața grafică și **Pillow/NumPy** pentru algoritmii de procesare digitală a imaginilor.

## 🚀 Funcționalități principale
1.  **Conversii Spații de Culoare:** Grayscale (3 metode), YUV, YCbCr, HSV.
2.  **Analiză Structurală:** Binarizare cu prag variabil, calcul Centru de Masă.
3.  **Momente și Statistică:** Momente de ordin 1 și 2, Matricea de Covarianță.
4.  **Analiză Vizuală:** Histogramă pe nivele de gri, Proiecții Orizontale și Verticale.

## 🛠️ Cerințe de sistem
* **Python:** Versiunea 3.8 sau mai nouă.
* **Sistem de operare:** Windows, macOS sau Linux.

## 📦 Instalare și Configurare

1. **Clonarea proiectului / Descărcarea arhivei**
   ```bash
   git clone [https://github.com/Deyutzu/PrelucrareaImaginilor.git](https://github.com/Deyutzu/PrelucrareaImaginilor.git)
   cd PrelucrareaImaginilor

2. **Crearea și activarea unui mediu virtual (recomandat)**
  python -m venv venv
# Pe Windows:
.\venv\Scripts\activate
# Pe Linux/macOS:
source venv/bin/activate


3. **Instalarea librăriilor necesare**
   pip install -r requirements.txt


4. **Pornirea aplicației**
Pentru a lansa interfața grafică, rulează:
  python lab01.py
