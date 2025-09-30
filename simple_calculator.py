import tkinter as tk
from tkinter import ttk
import pandas as pd
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# -----------------
# Загрузка данных
# -----------------
df = pd.read_excel("data.xlsx", sheet_name="modules")

# -----------------
# Создание окна
# -----------------
app = ctk.CTk()
app.geometry("900x650")
app.title("Калькулятор модулей")

# -----------------
# Переменные
# -----------------
module_var = ctk.StringVar()
category_var = ctk.StringVar()
type_var = ctk.StringVar()
filling_var = ctk.StringVar()
price_var = ctk.StringVar()
qty_var = tk.IntVar(value=1)

color_var = ctk.StringVar()
color_values = ["Базовый", "Премиум"]
color_var.set(color_values[0])  # по умолчанию "Базовый"

# -----------------
# Верхние списки
# -----------------
category_menu = ctk.CTkOptionMenu(
    app,
    values=df.iloc[:, 1].dropna().astype(str).unique().tolist(),
    variable=category_var
)
category_menu.pack(pady=5)

type_menu = ctk.CTkOptionMenu(
    app,
    values=[],
    variable=type_var
)
type_menu.pack(pady=5)

filling_menu = ctk.CTkOptionMenu(
    app,
    values=[],
    variable=filling_var
)
filling_menu.pack(pady=5)

module_menu = ctk.CTkOptionMenu(
    app,
    values=[],
    variable=module_var
)
module_menu.pack(pady=5)


color_menu = ctk.CTkOptionMenu(app, values=color_values, variable=color_var)
color_menu.pack(pady=5)



price_label = ctk.CTkLabel(app, text="Цена корпуса: ")
price_label.pack(pady=5)


# -----------------
# Поля для ввода размеров (по центру)
# -----------------
size_frame = ctk.CTkFrame(app)
size_frame.pack(pady=5)

# Высота
height_var = tk.StringVar()
height_label = ctk.CTkLabel(size_frame, text="Высота:")
height_label.grid(row=0, column=0, padx=(0,5))
height_entry = ctk.CTkEntry(size_frame, textvariable=height_var, width=80)
height_entry.grid(row=0, column=1, padx=(0,15))

# Ширина
width_var = tk.StringVar()
width_label = ctk.CTkLabel(size_frame, text="Ширина:")
width_label.grid(row=0, column=2, padx=(0,5))
width_entry = ctk.CTkEntry(size_frame, textvariable=width_var, width=80)
width_entry.grid(row=0, column=3, padx=(0,15))

# Глубина
depth_var = tk.StringVar()
depth_label = ctk.CTkLabel(size_frame, text="Глубина:")
depth_label.grid(row=0, column=4, padx=(0,5))
depth_entry = ctk.CTkEntry(size_frame, textvariable=depth_var, width=80)
depth_entry.grid(row=0, column=5)

# Сделаем все колонки по центру
for i in range(6):
    size_frame.grid_columnconfigure(i, weight=1)
qty_spin = tk.Spinbox(app, from_=1, to=100, textvariable=qty_var, width=5)
qty_spin.pack(pady=5)

# -----------------
# Корзина Treeview
# -----------------
columns = columns = ("module", "category", "type", "filling", "height", "width", "depth", "qty", "price")
tree = ttk.Treeview(app, columns=columns, show="headings", height=10)
tree.pack(pady=5, fill="x")

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=60, anchor="center")

total_label = ctk.CTkLabel(app, text="Итоговая сумма: 0 руб.")
total_label.pack(pady=5)

cart = []

# -----------------
# Функции
# -----------------
def update_price(*args):
    selected_module = module_var.get()
    selected_color = color_var.get()

    if not selected_module:
        price_var.set(0)
        price_label.configure(text="Цена корпуса: 0.00 руб.")
        return

    price_row = df[df.iloc[:, 0] == selected_module]
    if price_row.empty:
        price_var.set(0)
        price_label.configure(text="Цена корпуса: 0.00 руб.")
        return

    # Определяем колонку с базовой ценой по цвету
    if selected_color == "Базовый":
        base_price_col = 12  # 13-й столбец
    else:  # "Премиум"
        base_price_col = 13  # 14-й столбец

    base_price = price_row.iloc[0, base_price_col]
    if pd.isna(base_price):
        base_price = 0.0

    # Получаем базовые размеры
    baz_height = price_row.iloc[0, 14]  # 16-й столбец
    baz_width  = price_row.iloc[0, 15]  # 17-й столбец
    baz_depth  = price_row.iloc[0, 16]  # 18-й столбец

    # Получаем коэффициенты
    coeff_height = price_row.iloc[0, 17]  # 19-й столбец
    coeff_width  = price_row.iloc[0, 18]  # 20-й столбец
    coeff_depth  = price_row.iloc[0, 19]  # 21-й столбец

    # Считываем текущие размеры
    try:
        actual_height = float(height_var.get())
    except ValueError:
        actual_height = baz_height
    try:
        actual_width = float(width_var.get())
    except ValueError:
        actual_width = baz_width
    try:
        actual_depth = float(depth_var.get())
    except ValueError:
        actual_depth = baz_depth

    # Расчет цены с учетом размеров
    price = base_price
    price += ((base_price * coeff_width - base_price) / 100) * round(actual_width - baz_width, 0)
    price += ((base_price * coeff_height - base_price) / 100) * round(actual_height - baz_height, 0)
    if (actual_depth - baz_depth) > 0 and coeff_depth != 0:
        price += ((base_price * coeff_depth - base_price) / 100) * round(actual_depth - baz_depth, 0)

    # Обновляем переменную и метку
    price_var.set(round(price, 2))
    price_label.configure(text=f"Цена корпуса: {price:.2f} руб.")

def update_module_defaults():
    """При выборе модуля подставляем базовые размеры в поля"""
    selected_module = module_var.get()
    if selected_module:
        row = df[df.iloc[:, 0] == selected_module]
        if not row.empty:
            # Подставляем базовые размеры
            height_var.set(row.iloc[0, 14])
            width_var.set(row.iloc[0, 15])
            depth_var.set(row.iloc[0, 16])


def update_module_list(*args):
    """Иерархическая фильтрация: category -> type -> filling -> module"""
    filtered_df = df.copy()

    # 1. Фильтруем по категории
    cat = category_var.get()
    if cat:
        filtered_df = filtered_df[filtered_df.iloc[:, 1] == cat]

    # Обновляем список типов
    types = filtered_df.iloc[:, 3].dropna().astype(str).unique().tolist()
    type_menu.configure(values=types)
    if type_var.get() not in types:
        type_var.set(types[0] if types else "")

    # 2. Фильтруем по типу
    typ = type_var.get()
    if typ:
        filtered_df = filtered_df[filtered_df.iloc[:, 3] == typ]

    # Обновляем список наполнений
    fillings = filtered_df.iloc[:, 5].dropna().astype(str).unique().tolist()
    filling_menu.configure(values=fillings)
    if filling_var.get() not in fillings:
        filling_var.set(fillings[0] if fillings else "")

    # 3. Фильтруем по наполнению
    fill = filling_var.get()
    if fill:
        filtered_df = filtered_df[filtered_df.iloc[:, 5] == fill]

    # 4. Обновляем список модулей
    modules = filtered_df.iloc[:, 0].dropna().astype(str).unique().tolist()
    module_menu.configure(values=modules)
    if module_var.get() not in modules:
        module_var.set(modules[0] if modules else "")
    update_module_defaults()  # <-- Подставляем базовые размеры
    update_price()  # <-- Пересчёт цены с учётом этих размеров

# -----------------
# Функция добавления в корзину
# -----------------
def add_to_cart():
    mod = module_var.get()
    cat = category_var.get()
    typ = type_var.get()
    fill = filling_var.get()
    try:
        height = float(height_var.get())
    except ValueError:
        height = 0
    try:
        width = float(width_var.get())
    except ValueError:
        width = 0
    try:
        depth = float(depth_var.get())
    except ValueError:
        depth = 0
    qty = qty_var.get()
    
    try:
        price = float(price_var.get())
    except ValueError:
        price = 0.0
    total_price = price * qty
    
    if not mod:
        return
    
    # Добавляем размеры в корзину
    cart.append((mod, cat, typ, fill, height, width, depth, qty, total_price))
    
    # Обновляем Treeview
    for item in tree.get_children():
        tree.delete(item)
    
    sum_total = 0
    for m, c, t, f, h, w, d, q, p in cart:
        tree.insert("", "end", values=(m, c, t, f, h, w, d, q, f"{p:.2f}"))
        sum_total += p
    total_label.configure(text=f"Итоговая сумма: {sum_total:.2f} руб.")

# -----------------
# Функция удаления выделенного
# -----------------
def remove_selected():
    selected_item = tree.selection()
    if not selected_item:
        return
    index = tree.index(selected_item)
    del cart[index]
    tree.delete(selected_item)
    sum_total = sum(p for _, _, _, _, _, _, _, _, p in cart)
    total_label.configure(text=f"Итоговая сумма: {sum_total:.2f} руб.")

# -----------------
# Привязки
# -----------------
category_var.trace_add("write", update_module_list)
type_var.trace_add("write", update_module_list)
filling_var.trace_add("write", update_module_list)
module_var.trace_add("write", update_price)
color_var.trace_add("write", update_price)
height_var.trace_add("write", update_price)
width_var.trace_add("write", update_price)
depth_var.trace_add("write", update_price)

# -----------------
# Кнопки
# -----------------
add_btn = ctk.CTkButton(app, text="Добавить в корзину", command=add_to_cart)
add_btn.pack(pady=5)

remove_btn = ctk.CTkButton(app, text="Удалить выделенный модуль", command=remove_selected)
remove_btn.pack(pady=5)

# -----------------
# Инициализация первого фильтра
# -----------------
if df.iloc[:, 1].dropna().tolist():
    category_var.set(df.iloc[:, 1].dropna().astype(str).unique().tolist()[0])
    update_module_list()

app.mainloop()
