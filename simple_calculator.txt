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
# Новая таблица с фурнитурой
kf_korp = pd.read_excel("data.xlsx", sheet_name="kf_korp")

furn = pd.read_excel("data.xlsx", sheet_name="furn")
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
furn_price_var = tk.StringVar(value="0.00")
furn_price_label = ctk.CTkLabel(app, text="Цена фурнитуры: 0.00 руб.")
furn_price_label.pack(pady=5)
total_price_var = ctk.StringVar(value="0.00")
total_price_label = ctk.CTkLabel(app, text=f"Итоговая цена: {total_price_var.get()} руб.")
total_price_label.pack(pady=5)

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

    # Если модуль не выбран
    if not selected_module:
        price_var.set(0)
        furn_price_var.set("0.00")
        price_label.configure(text="Цена корпуса: 0.00 руб.")
        furn_price_label.configure(text="Цена фурнитуры: 0.00 руб.")
        return

    # Получаем строку модуля
    price_row = df[df.iloc[:, 0] == selected_module]
    if price_row.empty:
        price_var.set(0)
        furn_price_var.set("0.00")
        price_label.configure(text="Цена корпуса: 0.00 руб.")
        furn_price_label.configure(text="Цена фурнитуры: 0.00 руб.")
        return

    # Базовая цена корпуса
    base_price_col = 12 if selected_color == "Базовый" else 13
    base_price = price_row.iloc[0, base_price_col]
    if pd.isna(base_price):
        base_price = 0.0

    # Базовые размеры
    baz_height = price_row.iloc[0, 14]
    baz_width  = price_row.iloc[0, 15]
    baz_depth  = price_row.iloc[0, 16]

    # Коэффициенты
    coeff_height = price_row.iloc[0, 17]
    coeff_width  = price_row.iloc[0, 18]
    coeff_depth  = price_row.iloc[0, 19]

    # Текущие размеры
    try: actual_height = float(height_var.get())
    except ValueError: actual_height = baz_height
    try: actual_width = float(width_var.get())
    except ValueError: actual_width = baz_width
    try: actual_depth = float(depth_var.get())
    except ValueError: actual_depth = baz_depth

    # === Цена корпуса ===
    price_corp = base_price
    price_corp += ((base_price * coeff_width - base_price) / 100) * round(actual_width - baz_width, 0)
    price_corp += ((base_price * coeff_height - base_price) / 100) * round(actual_height - baz_height, 0)
    if (actual_depth - baz_depth) > 0 and coeff_depth != 0:
        price_corp += ((base_price * coeff_depth - base_price) / 100) * round(actual_depth - baz_depth, 0)

    # === Цена фурнитуры ===
    price_furn = 0.0
    if 'kf_korp' in globals() and 'furn' in globals():
        kf_rows = kf_korp[kf_korp['name_module'] == selected_module]

        for _, row in kf_rows.iterrows():
            try:
                # Берём стандартную фурнитуру и количество
                name_furn = row['name_furn']
                quantity = row['quanity']

                # Проверяем условие (если есть)
                condition = row.get('condition', '')
                if isinstance(condition, str) and condition.strip():
                    local_vars = {
                        "actual_width": actual_width,
                        "actual_height": actual_height,
                        "actual_depth": actual_depth
                    }
                    if eval(condition, {}, local_vars):
                        # Подмена фурнитуры и количества
                        if pd.notna(row.get('name_furn_changed')):
                            name_furn = row['name_furn_changed']
                        if pd.notna(row.get('changed_quantity')):
                            quantity = row['changed_quantity']

                # Получаем цену фурнитуры
                furn_row = furn[furn['name_furn'].astype(str).str.strip() == str(name_furn).strip()]
                if not furn_row.empty:
                    furn_price = furn_row.iloc[0]['price']
                    if pd.isna(furn_price):
                        furn_price = 0.0
                    price_furn += furn_price * quantity

            except Exception as e:
                print(f"Ошибка при обработке строки kf_korp: {e}")

    # === Общая цена ===
    total_price = price_corp + price_furn

    # === Обновление меток ===
    price_var.set(round(total_price, 2))
    price_label.configure(text=f"Цена корпуса: {price_corp:.2f} руб.")
    furn_price_var.set(round(price_furn, 2))
    furn_price_label.configure(text=f"Цена фурнитуры: {price_furn:.2f} руб.")
    total_price_var.set(round(total_price, 2))  # <-- обновляем итоговую переменную
    total_price_label.configure(text=f"Цена корпус + фурнитура: {total_price:.2f} руб.")  # <-- обновляем итоговую метку







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

    # Берём отдельные цены корпуса и фурнитуры
    try:
        price_corp = float(price_label.cget("text").split(":")[1].split()[0])
    except Exception:
        price_corp = 0.0
    try:
        price_furn = float(furn_price_label.cget("text").split(":")[1].split()[0])
    except Exception:
        price_furn = 0.0

    total_price = (price_corp + price_furn) * qty

    if not mod:
        return

    # Добавляем размеры и цены в корзину
    cart.append((mod, cat, typ, fill, height, width, depth, qty, price_corp, price_furn, total_price))

    # Обновляем Treeview
    for item in tree.get_children():
        tree.delete(item)

    sum_total = 0
    for m, c, t, f, h, w, d, q, corp_p, furn_p, total_p in cart:
        tree.insert("", "end", values=(m, c, t, f, h, w, d, q, f"{total_p:.2f}"))
        sum_total += total_p

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
