import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tensorflow.keras.models import load_model
from PIL import Image, ImageTk

# Modeli yükle
model = load_model("stroke_detection_model.h5")

def convert_to_png(image_path):
    img = Image.open(image_path)
    png_path = image_path.rsplit(".", 1)[0] + ".png"
    img.save(png_path, "PNG")
    return png_path

def extract_brain(image_path):
    if not image_path.lower().endswith(".png"):
        image_path = convert_to_png(image_path)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Hata: {image_path} yüklenemedi.")
        return None
    _, bone_mask = cv2.threshold(image, np.max(image) - 3, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    bone_mask = cv2.morphologyEx(bone_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    bone_removed = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(bone_mask))
    blurred = cv2.GaussianBlur(bone_removed, (3,3), 0)
    _, brain_mask = cv2.threshold(blurred, np.max(blurred) * 0.1, 255, cv2.THRESH_BINARY)
    num_labels, labels_img, stats, _ = cv2.connectedComponentsWithStats(brain_mask, connectivity=4)
    largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    brain_only_mask = np.uint8(labels_img == largest_label) * 255
    brain_extracted = cv2.bitwise_and(image, image, mask=brain_only_mask)
    return brain_extracted

def preprocess_image(image):
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    image = extract_brain(file_path)
    if image is None:
        return

    # Görüntüyü göster
    img_display = Image.fromarray(image.astype(np.uint8), mode="L")
    img_display = img_display.resize((300, 300))
    img_display = ImageTk.PhotoImage(img_display)

    panel.config(image=img_display)
    panel.image = img_display

    # Tahmin yap
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)[0][0]
    result_text = "İnme Var" if prediction > 0.5 else "İnme Yok"
    confidence = f"{prediction * 100:.2f}%"
    result_label.config(text=f"{file_path.split('/')[-1]}\nTahmin: {result_text} ({confidence})", fg="black")

# Arayüz
root = tk.Tk()
root.title("Tek Görsel İnme Tespiti")
root.geometry("400x450")

btn_select = tk.Button(root, text="Görsel Seç", command=select_image)
btn_select.pack(pady=10)

panel = tk.Label(root)
panel.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

root.mainloop()
