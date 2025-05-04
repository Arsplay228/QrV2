import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk, ImageDraw
import io


def round_corners(img, radius=30):
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    img.putalpha(mask)
    return img


def generate_qr():
    url = entry.get()
    if not url:
        ctk.CTkMessagebox(title="Ошибка", message="Введите ссылку!", icon="warning")
        return

    qr = qrcode.make(url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    img = Image.open(buffer).convert("RGBA")

    border_size = 0
    bordered_img = Image.new("RGBA", (img.width + border_size * 2, img.height + border_size * 2), "black")
    bordered_img.paste(img, (border_size, border_size))

    rounded = round_corners(bordered_img, radius=30)

    qr_photo = ImageTk.PhotoImage(rounded)
    qr_label.configure(image=qr_photo)
    qr_label.image = qr_photo

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("QR Генератор")
app.geometry("400x500")

entry = ctk.CTkEntry(app, placeholder_text="Введите ссылку", width=300)
entry.pack(pady=20)

generate_button = ctk.CTkButton(app, text="Сгенерировать QR", command=generate_qr)
generate_button.pack(pady=10)

qr_label = ctk.CTkLabel(app, text="")
qr_label.pack(pady=20)

app.mainloop()
