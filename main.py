import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import qrcode
import io

def round_corners(img, radius=30):
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, *img.size], radius, fill=255)
    img.putalpha(mask)
    return img

def generate_qr():
    url = entry.get()
    if not url:
        ctk.CTkMessagebox(title="Ошибка", message="Введите ссылку!", icon="warning")
        return

    qr_color = color_map[color_var.get()]
    qr = qrcode.QRCode(box_size=10, border=1)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=qr_color, back_color="white").convert("RGBA")

    img = round_corners(img)  # Закругление углов

    qr_photo = ImageTk.PhotoImage(img)
    qr_label.configure(image=qr_photo)
    qr_label.image = qr_photo


def open_settings():
    main_frame.pack_forget()
    settings_frame.pack(fill="both", expand=True)

def back_to_main():
    settings_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def change_theme(theme_rus):
    ctk.set_appearance_mode("light" if theme_rus == "Светлая" else "dark")

color_map = {
    "Чёрный": "black",
    "Синий": "blue",
    "Красный": "red",
    "Зелёный": "green"
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("QR Генератор")
app.geometry("400x550")

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True)

entry = ctk.CTkEntry(main_frame, placeholder_text="Введите ссылку", width=300)
entry.pack(pady=20)

ctk.CTkButton(main_frame, text="Сгенерировать QR", command=generate_qr).pack(pady=10)
qr_label = ctk.CTkLabel(main_frame, text="")
qr_label.pack(pady=20)

ctk.CTkButton(main_frame, text="⚙ Настройки", command=open_settings).pack(pady=10)

settings_frame = ctk.CTkFrame(app)

ctk.CTkButton(settings_frame, text="← Назад", width=100, command=back_to_main).pack(pady=(10, 5), anchor="w", padx=10)
ctk.CTkLabel(settings_frame, text="Тема интерфейса:").pack(pady=10)

theme_menu = ctk.CTkOptionMenu(settings_frame, values=["Светлая", "Тёмная"], command=change_theme)
theme_menu.set("Тёмная")
theme_menu.pack(pady=5)

ctk.CTkLabel(settings_frame, text="Цвет QR-кода:").pack(pady=(20, 5))
color_var = ctk.StringVar(value="Чёрный")
color_menu = ctk.CTkOptionMenu(settings_frame, variable=color_var, values=list(color_map.keys()))
color_menu.pack()

app.mainloop()
