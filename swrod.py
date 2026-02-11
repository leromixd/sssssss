import tkinter as tk

# Основное окно
root = tk.Tk()
root.title("Настройка текста для оверлея")
root.geometry("800x600")

overlay_text = tk.StringVar()
color_text = tk.StringVar()
font_size = tk.IntVar(value=14)  # базовый размер 14

overlay_text.set("Пример текста\nМного строк\nДля оверлея")
color_text.set("cyan")  # по умолчанию

def update_overlay():
    text = text_entry.get("0.1", "end-1c")
    overlay_text.set(text)

def set_color(color):
    color_text.set(color)
    refresh_overlay_text()

def refresh_overlay_text():
    font_tuple = ('Arial', font_size.get())
    # Обновляем текст на canvas, добавляя перенос по ширине
    canvas.itemconfig(display_text, text=overlay_text.get(), fill=color_text.get(), font=font_tuple, width=200)

# Создаем Text для ввода текста
text_entry = tk.Text(root, height=5, width=40, wrap='word')
text_entry.insert(tk.END, overlay_text.get())
text_entry.pack(pady=10)

# Обработка Ctrl+A / Cmd+A для выделения всего текста
def on_key_press(event):
    # Проверка для Windows/Linux и Mac
    if (event.state & 0x4 and event.keysym == 'a') or (event.state & 0x1 and event.keysym == 'A'):
        # Выделение всего текста
        text_entry.tag_add('sel', '1.0', 'end')
        return 'break'  # Предотвращает стандартное поведение

text_entry.bind('<Control-a>', on_key_press)
text_entry.bind('<Command-a>', on_key_press)

# Создаем оверлей
overlay = tk.Toplevel(root)
overlay.title("Overlay")
overlay.overrideredirect(True)
overlay.attributes("-topmost", True)
# Команды для прозрачности и позиционирования
overlay.attributes("-transparentcolor", "black")
overlay.geometry("1600x800+0+0")

canvas = tk.Canvas(overlay, width=1600, height=800, bg='black', highlightthickness=0)
canvas.pack()

# Создаем текст на Canvas с переносом
display_text = canvas.create_text(10, 10, anchor='nw', text=overlay_text.get(), fill=color_text.get(), font=('Arial', 14), width=600)

def periodic_update():
    refresh_overlay_text()
    overlay.after(1000, periodic_update)

periodic_update()

def move_overlay_x(val):
    try:
        x_position = int(val)
        current_geom = overlay.geometry()
        parts = current_geom.split('+')
        size = parts[0]
        y = parts[2] if len(parts) > 2 else '0'
        overlay.geometry(f"{size}+{x_position}+{y}")
    except:
        pass

def move_overlay_y(val):
    try:
        y_position = int(val)
        current_geom = overlay.geometry()
        parts = current_geom.split('+')
        size = parts[0]
        x = parts[1] if len(parts) > 1 else '0'
        overlay.geometry(f"{size}+{x}+{y_position}")
    except:
        pass

tk.Label(root, text="Перемещение по ширине").pack()
slider_x = tk.Scale(root, from_=0, to=1600, orient='horizontal', command=move_overlay_x)
slider_x.set(0)
slider_x.pack()

tk.Label(root, text="Перемещение по высоте").pack()
slider_y = tk.Scale(root, from_=0, to=800, orient='horizontal', command=move_overlay_y)
slider_y.set(0)
slider_y.pack()

colors = ['red', 'green', 'blue', 'cyan', 'yellow', 'magenta', 'white', 'orange', 'purple']
palette_frame = tk.Frame(root)
palette_frame.pack(pady=10)

for color in colors:
    btn = tk.Button(palette_frame, bg=color, width=3, command=lambda c=color: set_color(c))
    btn.pack(side='left', padx=2)

def on_size_change(val):
    refresh_overlay_text()

size_label = tk.Label(root, text="Размер текста")
size_label.pack()

size_slider = tk.Scale(root, from_=8, to=30, orient='horizontal', variable=font_size, command=on_size_change)
size_slider.set(14)
size_slider.pack()

def on_text_change(event):
    update_overlay()

text_entry.bind("<KeyRelease>", on_text_change)

# Запуск
root.mainloop()