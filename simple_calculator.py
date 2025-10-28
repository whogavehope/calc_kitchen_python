import tkinter as tk
from tkinter import ttk
import pandas as pd
import customtkinter as ctk

# Устанавливаем тему для интерфейса
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# -----------------
# Загрузка данных из Excel
# -----------------
# Загружаем данные из разных листов Excel-файла
df = pd.read_excel("data.xlsx", sheet_name="modules")        # Основная информация по корпусам
kf_korp = pd.read_excel("data.xlsx", sheet_name="kf_korp")   # Фурнитура корпуса (КФ)
furn = pd.read_excel("data.xlsx", sheet_name="furn")         # Цены фурнитуры
kompl = pd.read_excel("data.xlsx", sheet_name="kompl")       # Комплектация
polki = pd.read_excel("data.xlsx", sheet_name="polki")       # Информация о полках
color_korp = pd.read_excel("data.xlsx", sheet_name="color_korp")  # Информация о цвете корпуса
color_fasades = pd.read_excel("data.xlsx", sheet_name="color_fasades")   # Цвета фасадов
frez = pd.read_excel("data.xlsx", sheet_name="frez")                     # Фрезеровка
price_collections = pd.read_excel("data.xlsx", sheet_name="price_collections")  # Коллекции и цены
# Выводим, что находится в столбце "Изделие" на листе "polki"
print("Столбец 'Изделие' из листа 'polki':")
print(polki["Изделие"].dropna().tolist())

# Создаём список типов полок (уникальные значения из столбца "Изделие")
polki_types = polki["Изделие"].dropna().astype(str).unique().tolist()
print("polki_types:", polki_types)

# -----------------
# Создание основного окна приложения
# -----------------
app = ctk.CTk()
app.geometry("900x900")
app.title("Калькулятор модулей")

# -----------------
# Переменные для хранения выбранных значений
# -----------------
module_var = ctk.StringVar()      # Выбранный модуль
category_var = ctk.StringVar()    # Категория
type_var = ctk.StringVar()        # Тип
filling_var = ctk.StringVar()     # Наполнение
kompl_var = ctk.StringVar()       # Комплектация
price_var = ctk.StringVar()       # Цена
qty_var = tk.IntVar(value=1)      # Количество

color_var = ctk.StringVar()       # Цвет (из Excel)
color_options = color_korp["Цвета"].dropna().astype(str).tolist()  # ← НОВОЕ
# -----------------
# Переменные для фасадов
# -----------------
collection_var = ctk.StringVar()  # Выбранная коллекция фасада
print("color_options:", color_options)
if color_options:
    color_var.set(color_options[0])  # По умолчанию первый цвет

frez_var = ctk.StringVar()  # Выбранная фрезеровка

facade_color_var = ctk.StringVar()  # Выбранный цвет фасада

facade_thickness_var = ctk.StringVar()  # Выбранная толщина фасада

facade_type_var = ctk.StringVar()  # Тип фасада: Глухая / Витрина / Решетка




# -----------------
# Фрейм для размещения меню в сетке (2 колонки)
# -----------------
menu_frame = ctk.CTkFrame(app)
menu_frame.pack(pady=10, padx=10, fill="x")
# -----------------
# Верхние выпадающие списки (категория, тип, наполнение, модуль)
# -----------------
category_menu = ctk.CTkOptionMenu(
    menu_frame,
    values=df.iloc[:, 1].dropna().astype(str).unique().tolist(),  # Значения из 2-го столбца
    variable=category_var
)
#category_menu.pack(pady=5)

type_menu = ctk.CTkOptionMenu(menu_frame, values=[], variable=type_var)
#type_menu.pack(pady=5)

filling_menu = ctk.CTkOptionMenu(menu_frame, values=[], variable=filling_var)
#filling_menu.pack(pady=5)

module_menu = ctk.CTkOptionMenu(menu_frame, values=[], variable=module_var)
#module_menu.pack(pady=5)

# -----------------
# Список цветов
# -----------------
color_menu = ctk.CTkOptionMenu(menu_frame, values=color_options, variable=color_var)
#color_menu.pack(pady=5)

# -----------------
# Список комплектаций
# -----------------
kompl_var = ctk.StringVar()
kompl_menu = ctk.CTkOptionMenu(menu_frame, values=[], variable=kompl_var)
#kompl_menu.pack(pady=5)

# -----------------
# Список коллекций фасадов
# -----------------
collection_options = price_collections["Коллекция"].dropna().astype(str).unique().tolist()
if collection_options:
    collection_var.set(collection_options[0])  # По умолчанию — первая коллекция
collection_menu = ctk.CTkOptionMenu(menu_frame, values=collection_options, variable=collection_var)
# -----------------
# Список фрезеровок (зависит от коллекции)
# -----------------
frez_menu = ctk.CTkOptionMenu(menu_frame, values=[], variable=frez_var)
# -----------------
# Список цветов фасада (зависит от коллекции)
# -----------------
facade_color_menu = ctk.CTkOptionMenu(menu_frame, values=[], variable=facade_color_var)
# -----------------
# Список толщин фасадов (зависит от коллекции и фрезеровки)
# -----------------
thickness_menu = ctk.CTkOptionMenu(menu_frame, values=[], variable=facade_thickness_var)
# -----------------
# Список типов фасада (зависит от коллекции и фрезеровки)
# -----------------
facade_type_menu = ctk.CTkOptionMenu(menu_frame, values=[], variable=facade_type_var)

# === Левая колонка: корпус ===
row = 0
for label_text, menu_widget in [
    ("Категория:", category_menu),
    ("Тип:", type_menu),
    ("Наполнение:", filling_menu),
    ("Модуль:", module_menu),
    ("Цвет корпуса:", color_menu),
    ("Комплектация:", kompl_menu),
]:
    label = ctk.CTkLabel(menu_frame, text=label_text)
    label.grid(row=row, column=0, padx=(10, 5), pady=3, sticky="e")
    menu_widget.grid(row=row, column=1, padx=(5, 20), pady=3, sticky="w")
    row += 1

# === Правая колонка: фасад ===
row = 0
for label_text, menu_widget in [
    ("Коллекция фасада:", collection_menu),
    ("Фрезеровка:", frez_menu),
    ("Цвет фасада:", facade_color_menu),
    ("Толщина фасада:", thickness_menu),
    ("Тип фасада:", facade_type_menu),
]:
    label = ctk.CTkLabel(menu_frame, text=label_text)
    label.grid(row=row, column=2, padx=(10, 5), pady=3, sticky="e")
    menu_widget.grid(row=row, column=3, padx=(5, 10), pady=3, sticky="w")
    row += 1

# -----------------
# Фрейм для размещения лейблов в сетке (2 колонки)
# -----------------
label_frame = ctk.CTkFrame(app)
label_frame.pack(pady=10, padx=10, fill="x")

# -----------------
# Метки для отображения цен корпуса
# -----------------
price_label = ctk.CTkLabel(label_frame, text="Цена корпуса: ")
price_label.grid(row=row, column=0, padx=(10, 20), pady=3, sticky="w")
row +=1
# -----------------
# Метка для цены базового комплекта
# -----------------
furn_price_var = tk.StringVar(value="0.00")
furn_price_label = ctk.CTkLabel(label_frame, text="Цена фурнитуры: 0.00 руб.")
furn_price_label.grid(row=row, column=0, padx=(10, 20), pady=3, sticky="w")
row +=1
# -----------------
# Метка для комплектации
# -----------------
kompl_price_var = tk.StringVar(value="0.00")
kompl_price_label = ctk.CTkLabel(label_frame, text=f"Цена комплектации: {kompl_price_var.get()} руб.")
kompl_price_label.grid(row=row, column=0, padx=(10, 20), pady=3, sticky="w")
row +=1

# -----------------------------------
# Поле для цены полок
# -----------------------------------
polki_price_var = tk.StringVar(value="0.00")
polki_price_label = ctk.CTkLabel(label_frame, text=f"Цена полок: {polki_price_var.get()} руб.")
polki_price_label.grid(row=row, column=0, padx=(10, 20), pady=3, sticky="w")
row +=1


# -----------------
# Метка для площади фасадов
# -----------------
facade_area_var = tk.StringVar(value="0.00")
facade_area_label = ctk.CTkLabel(label_frame, text=f"Площадь фасада: {facade_area_var.get()} м²")
facade_area_label.grid(row=row, column=1, padx=(10, 20), pady=3, sticky="w")
row =1

# -----------------
# Метка для цены фасадов
# -----------------
facade_price_var = tk.StringVar(value="0.00")
facade_price_label = ctk.CTkLabel(label_frame, text=f"Цена фасадов: {facade_price_var.get()} руб.")
facade_price_label.grid(row=row, column=1, padx=(10, 20), pady=3, sticky="w")
row +=1


# -----------------
# Метка для итоговой цены
# -----------------
total_price_var = ctk.StringVar(value="0.00")
total_price_label = ctk.CTkLabel(app, text=f"Итоговая цена: {total_price_var.get()} руб.")
total_price_label.pack(pady=5)

# -----------------
# Поля для ввода размеров (по центру)
# -----------------
size_frame = ctk.CTkFrame(app)
size_frame.pack(pady=5)

height_var = tk.StringVar()
height_label = ctk.CTkLabel(size_frame, text="Высота:")
height_label.grid(row=0, column=0, padx=(0,5))
height_entry = ctk.CTkEntry(size_frame, textvariable=height_var, width=80)
height_entry.grid(row=0, column=1, padx=(0,15))

width_var = tk.StringVar()
width_label = ctk.CTkLabel(size_frame, text="Ширина:")
width_label.grid(row=0, column=2, padx=(0,5))
width_entry = ctk.CTkEntry(size_frame, textvariable=width_var, width=80)
width_entry.grid(row=0, column=3, padx=(0,15))

depth_var = tk.StringVar()
depth_label = ctk.CTkLabel(size_frame, text="Глубина:")
depth_label.grid(row=0, column=4, padx=(0,5))
depth_entry = ctk.CTkEntry(size_frame, textvariable=depth_var, width=80)
depth_entry.grid(row=0, column=5)

# Высота ниши (по умолчанию скрыта)
height_case_var = tk.StringVar()
height_case_label = ctk.CTkLabel(size_frame, text="Высота ниши:")
height_case_entry = ctk.CTkEntry(size_frame, textvariable=height_case_var, width=80)
height_case_label.grid_forget()
height_case_entry.grid_forget()

# Переменная для выпадающего списка
height_case_menu = None  # глобальная переменная
width_menu = None  
# -----------------
# Полки
# -----------------
polki_frame = ctk.CTkFrame(app)
polki_frame.pack(pady=5)

polki_count_label = ctk.CTkLabel(polki_frame, text="Количество полок:")
polki_count_label.grid(row=0, column=0, padx=(0,5))

polki_count_var = tk.IntVar(value=0)
polki_count_spin = tk.Spinbox(polki_frame, from_=0, to=0, textvariable=polki_count_var, width=5)
polki_count_spin.grid(row=0, column=1, padx=(0,15))

polki_type_label = ctk.CTkLabel(polki_frame, text="Тип полки:")
polki_type_label.grid(row=0, column=2, padx=(0,5))

polki_type_var = ctk.StringVar()
print("Инициализируем polki_type_menu с:", polki_types)
polki_type_menu = ctk.CTkOptionMenu(polki_frame, values=polki_types, variable=polki_type_var)
polki_type_menu.grid(row=0, column=3, padx=(0,15))

# -----------------
# Спинбокс количества
# -----------------
for i in range(8):
    size_frame.grid_columnconfigure(i, weight=1)

qty_spin = tk.Spinbox(app, from_=1, to=100, textvariable=qty_var, width=5)
qty_spin.pack(pady=5)

# -----------------
# Корзина Treeview
# -----------------
columns = ("module", "category", "type", "filling", "kompl", "height", "width", "depth", "qty", "price")
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

def calculate_facade_area():
    """Рассчитывает площадь фасада по формуле из Excel"""
    selected_module = module_var.get()
    if not selected_module:
        return 0.0

    # Находим строку модуля
    row = df[df.iloc[:, 0] == selected_module]
    if row.empty:
        return 0.0

    # Получаем формулу
    formula_col_name = "Формула_расчета_фасадов"
    if formula_col_name not in df.columns:
        print(f"⚠️ Столбец '{formula_col_name}' не найден в таблице 'modules'")
        return 0.0

    formula_raw = row.iloc[0][formula_col_name]
    if pd.isna(formula_raw) or str(formula_raw).strip().lower() in ["", "нет", "nan"]:
        return 0.0

    formula = str(formula_raw).strip()
    print(f"Формула фасада: {formula}")

    # Получаем текущие размеры
    try:
        actual_height = float(height_var.get())
    except (ValueError, AttributeError):
        actual_height = 0.0

    try:
        actual_width = float(width_var.get())
    except (ValueError, AttributeError):
        actual_width = 0.0

    try:
        actual_depth = float(depth_var.get())
    except (ValueError, AttributeError):
        actual_depth = 0.0

    # Получаем высоту ниши, если есть
    try:
        nisha_height = float(height_case_var.get()) if height_case_var.get() else 0.0
    except (ValueError, AttributeError):
        nisha_height = 0.0

    # Подготавливаем контекст для eval
    eval_vars = {
        "height": actual_height,
        "width": actual_width,
        "depth": actual_depth,
        "nisha": nisha_height  # именно "nisha", как в формуле
    }

    try:
        area = eval(formula, {"__builtins__": {}}, eval_vars)
        # Формулы уже делят на 1000 → результат в м²
        return float(area)
    except Exception as e:
        print(f"❌ Ошибка при расчёте фасада по формуле '{formula}': {e}")
        return 0.0

def calculate_facade_price():
    """Рассчитывает цену фасада с учётом всех параметров, включая особенности 'Softline Marine', скидку и наценку за сложную фрезеровку/решётку"""
    # 1. Получаем входные данные
    selected_collection = collection_var.get()
    selected_frez = frez_var.get()
    selected_color = facade_color_var.get()
    selected_thickness = facade_thickness_var.get()
    selected_type = facade_type_var.get()
    if not all([selected_collection, selected_frez, selected_color, selected_thickness, selected_type]):
        return 0.0

    # 2. Площадь фасада
    area = calculate_facade_area()
    if area <= 0:
        return 0.0

    # 3. Определяем ЦЕНОВУЮ ГРУППУ и СКИДКУ
    price_group = None
    discount = 0.0  # Инициализируем скидку
    if selected_collection == "Softline Marine":
        # Для Softline Marine — ценовая группа = выбранная фрезеровка
        price_group = selected_frez.strip()
        film_category = ""  # ← уточните: нужна ли категория пленки для Softline Marine?
        # Скидка для Softline Marine не предусмотрена в текущей логике
    else:
        # Для всех остальных — берём из color_fasades по цвету и коллекции
        color_row = color_fasades[
            (color_fasades["Коллекция"].astype(str).str.strip() == selected_collection.strip()) &
            (color_fasades["Номер цвета"].astype(str).str.strip() == selected_color.strip())
        ]
        if color_row.empty:
            print(f"⚠️ Цвет '{selected_color}' не найден в коллекции '{selected_collection}'")
            return 0.0

        # Получаем ценовую группу и скидку
        price_group_raw = color_row.iloc[0].get("Ценовая группа")
        film_category_raw = color_row.iloc[0].get("Категория пленки")
        discount_raw = color_row.iloc[0].get("Скидка") # <- НОВОЕ: получаем скидку

        if pd.isna(price_group_raw) or str(price_group_raw).strip().lower() in ["", "nan"]:
            print(f"⚠️ Не указана 'Ценовая группа' для цвета '{selected_color}'")
            return 0.0
        price_group = str(price_group_raw).strip()
        film_category = str(film_category_raw).strip() if pd.notna(film_category_raw) else ""

        # <- НОВОЕ: обработка скидки
        if pd.notna(discount_raw):
            try:
                discount = float(discount_raw)
                # Ограничиваем скидку от 0 до 1 (например, 0.2 = 20%)
                discount = max(0.0, min(1.0, discount))
            except (ValueError, TypeError):
                print(f"⚠️ Неверное значение скидки '{discount_raw}' для цвета '{selected_color}', устанавливаем 0.")
                discount = 0.0
        else:
            discount = 0.0
        # <- КОНЕЦ НОВОГО

    # 4. Находим строку в price_collections
    # Фильтруем по коллекции и ценовой группе
    filtered_pc = price_collections[
        (price_collections["Коллекция"].astype(str).str.strip() == selected_collection.strip()) &
        (price_collections["Ценовая группа"].astype(str).str.strip() == price_group.strip())
    ]
    # Если есть "Категория пленки" (и не Softline Marine), уточняем фильтр
    if selected_collection != "Softline Marine" and film_category:
        filtered_pc = filtered_pc[
            filtered_pc["Категория пленки"].astype(str).str.strip() == film_category.strip()
        ]

    if filtered_pc.empty:
        print(f"⚠️ Не найдена цена: коллекция='{selected_collection}', ценовая группа='{price_group}'"
              + (f", категория пленки='{film_category}'" if film_category else ""))
        return 0.0

    row = filtered_pc.iloc[0]

    # 5. Определяем столбец цены по толщине и типу фасада
    try:
        thickness = int(float(selected_thickness))
    except (ValueError, TypeError):
        thickness = 19
    col = None
    if selected_type == "Глухая":
        if thickness == 16:
            col = "Цена глухих 16 мм"
        elif thickness in (18, 19):
            col = "Цена глухих 18_19 мм"
        elif thickness == 22:
            col = "Цена глухих 22 мм"
        else:
            col = "Цена глухих 18_19 мм"
    elif selected_type == "Витрина":
        if thickness == 16:
            col = "Цена витрин 16 мм"
        elif thickness in (18, 19):
            col = "Цена витрин 18_19 мм"
        elif thickness == 22:
            col = "Цена витрин 22 мм"
        else:
            col = "Цена витрин 18_19 мм"
    elif selected_type == "Решетка":
        # Пока как глухая
        if thickness == 16:
            col = "Цена глухих 16 мм"
        elif thickness in (18, 19):
            col = "Цена глухих 18_19 мм"
        elif thickness == 22:
            col = "Цена глухих 22 мм"
        else:
            col = "Цена глухих 18_19 мм"

    # 6. Получаем базовую цену за м²
    if col not in row or pd.isna(row[col]):
        print(f"⚠️ Столбец '{col}' отсутствует или пуст в price_collections")
        return 0.0
    base_price_per_m2 = float(row[col])

    # 7. ПРИМЕНЯЕМ СКИДКУ К БАЗОВОЙ ЦЕНЕ (до фрезеровки)
    # <- НОВОЕ: Применяем скидку
    discounted_price_per_m2 = base_price_per_m2 * (1 - discount)
    print(f"Базовая цена: {base_price_per_m2}, Скидка: {discount*100}%, Цена после скидки: {discounted_price_per_m2}")
    # <- КОНЕЦ НОВОГО

    # 8. ДОПЛАТА ЗА ФРЕЗЕРОВКУ И ПРОВЕРКА ТИПА ФРЕЗЕРОВКИ / ТИПА ФАСАДА
    frez_row = frez[
        (frez["Коллекция"].astype(str).str.strip() == selected_collection.strip()) &
        (frez["Фрезеровка"].astype(str).str.strip() == selected_frez.strip())
    ]
    frez_surcharge = 0.0
    is_complex_frez = False  # флаг для "Сложной" фрезеровки или "Решетки"

    # Проверка типа фасада: "Решетка" всегда "Сложная"
    if selected_type == "Решетка":
        is_complex_frez = True
        print(f"Фасад типа '{selected_type}' считается 'Сложной' фрезеровкой.")
    elif not frez_row.empty:
        # --- Проверка типа фрезеровки для НЕ-решетки ---
        frez_type = frez_row.iloc[0].get("Тип Фрезеровки")
        if pd.notna(frez_type) and str(frez_type).strip().lower() == "сложная":
            is_complex_frez = True
        # --- Доплата за фрезеровку (обычная, не 25%) ---
        surcharge_val = frez_row.iloc[0].get("Доплата_руб_м2")
        if pd.notna(surcharge_val):
            try:
                frez_surcharge = float(surcharge_val)
            except (ValueError, TypeError):
                frez_surcharge = 0.0
    # else: для Softline Marine или если фрезеровка не найдена, is_complex_frez остаётся False, frez_surcharge = 0

    # 9. РАСЧЁТ ИТОГОВОЙ ЦЕНЫ ЗА М² (с учётом наценки за сложность)
    # Наценка за сложную фрезеровку (или решётку) = 25% от цены со скидкой
    complex_frez_surcharge_per_m2 = 0.0
    if is_complex_frez:
        complex_frez_surcharge_per_m2 = discounted_price_per_m2 * 0.25
        print(f"Применена наценка за 'Сложную' фрезеровку/Решетку: {complex_frez_surcharge_per_m2:.2f} руб/м2")

    # Итоговая цена за м² = цена со скидкой + обычная доплата за фрезеровку + наценка за сложность
    total_price_per_m2 = discounted_price_per_m2 + frez_surcharge + complex_frez_surcharge_per_m2
    total_price = total_price_per_m2 * area
    # <- КОНЕЦ ИЗМЕНЕНИЯ
    return total_price

def update_frez_list(*args):
    """Обновляет список фрезеровок и цветов фасада в зависимости от выбранной коллекции"""
    selected_collection = collection_var.get()
    
    # --- Обновление фрезеровок ---
    if frez.empty or not selected_collection:
        frez_menu.configure(values=["Без фрезеровки"])
        frez_var.set("Без фрезеровки")
    else:
        filtered_frez = frez[
            frez["Коллекция"].astype(str).str.strip() == selected_collection.strip()
        ]
        frez_options = filtered_frez["Фрезеровка"].dropna().astype(str).unique().tolist() if not filtered_frez.empty else ["Без фрезеровки"]
        if not frez_options:
            frez_options = ["Без фрезеровки"]
        frez_menu.configure(values=frez_options)
        frez_var.set(frez_options[0])

    # --- Обновление цветов фасада ---
    update_facade_color_list()
    # Обновляем толщину фасада
    update_thickness_list()
    # Обновляем тип фасада
    update_facade_type_list()
    # Пересчёт цены
    update_price()

def update_facade_color_list(*args):
    """Обновляет список цветов фасада в зависимости от выбранной коллекции"""
    selected_collection = collection_var.get()
    
    if color_fasades.empty or not selected_collection:
        color_options = ["Без цвета"]
    else:
        # Фильтруем по коллекции
        filtered_colors = color_fasades[
            color_fasades["Коллекция"].astype(str).str.strip() == selected_collection.strip()
        ]
        if filtered_colors.empty:
            color_options = ["Без цвета"]
        else:
            color_options = filtered_colors["Номер цвета"].dropna().astype(str).unique().tolist()
            if not color_options:
                color_options = ["Без цвета"]

    # Обновляем меню
    facade_color_menu.configure(values=color_options)
    facade_color_var.set(color_options[0])
    
    # Пересчёт цены (для будущего расчёта стоимости фасада)
    update_price()

def update_thickness_list(*args):
    """Обновляет список толщин фасада на основе выбранной коллекции и фрезеровки"""
    selected_collection = collection_var.get()
    selected_frez = frez_var.get()
    
    if frez.empty or not selected_collection or not selected_frez:
        thickness_options = ["19"]  # значение по умолчанию
    else:
        # Фильтруем по коллекции И фрезеровке
        filtered = frez[
            (frez["Коллекция"].astype(str).str.strip() == selected_collection.strip()) &
            (frez["Фрезеровка"].astype(str).str.strip() == selected_frez.strip())
        ]
        
        if filtered.empty:
            thickness_options = ["19"]
        else:
            thicknesses = set()
            for _, row in filtered.iterrows():
                t1 = row.get("Толщина 1")
                t2 = row.get("Толщина 2")
                
                # Добавляем Толщину 1, если она есть и не NaN
                if pd.notna(t1) and str(t1).strip().lower() not in ["", "nan"]:
                    try:
                        thicknesses.add(str(int(float(t1))))
                    except (ValueError, TypeError):
                        pass
                
                # Добавляем Толщину 2, если она есть, не NaN и не 0
                if pd.notna(t2) and str(t2).strip().lower() not in ["", "nan", "0"]:
                    try:
                        thicknesses.add(str(int(float(t2))))
                    except (ValueError, TypeError):
                        pass
            
            thickness_options = sorted(thicknesses, key=int) if thicknesses else ["19"]
    
    # Обновляем меню
    thickness_menu.configure(values=thickness_options)
    facade_thickness_var.set(thickness_options[0])
    
    # Пересчёт цены (для будущего расчёта)
    update_price()
def update_facade_type_list(*args):
    """Обновляет список типов фасада на основе коллекции и фрезеровки"""
    selected_collection = collection_var.get()
    selected_frez = frez_var.get()
    
    options = ["Глухая"]  # всегда доступно

    if not frez.empty and selected_collection and selected_frez:
        # Фильтруем по коллекции и фрезеровке
        filtered = frez[
            (frez["Коллекция"].astype(str).str.strip() == selected_collection.strip()) &
            (frez["Фрезеровка"].astype(str).str.strip() == selected_frez.strip())
        ]

        if not filtered.empty:
            # Проверяем значения в первых строках (если несколько — достаточно одной с "Да")
            has_vitrina = (
                filtered["Наличие_витрин"]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("да")
                .any()
            )
            has_reshetka = (
                filtered["Наличие_решеток"]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("да")
                .any()
            )

            if has_vitrina:
                options.append("Витрина")
            if has_reshetka:
                options.append("Решетка")

    # Обновляем меню
    facade_type_menu.configure(values=options)
    facade_type_var.set(options[0])
    
    # Пересчёт цены (на будущее)
    update_price()
def set_polki_type_menu(new_values):
    """Обновляет выпадающее меню выбора типа полок"""
    print("set_polki_type_menu получил:", new_values)
    global polki_type_menu, polki_type_var
    if hasattr(polki_type_menu, "set_values"):
        polki_type_menu.set_values(new_values)
    else:
        polki_type_menu.grid_forget()
        polki_type_menu.destroy()
        polki_type_menu = ctk.CTkOptionMenu(polki_frame, values=new_values, variable=polki_type_var)
        polki_type_menu.grid(row=0, column=3, padx=(0,15))
    if new_values:
        polki_type_var.set(new_values[0])

def update_module_defaults(*args):
    print("update_module_defaults вызван")
    global polki_type_menu, height_case_menu, width_menu
    selected_module = module_var.get()
    if not selected_module:
        return
    row = df[df.iloc[:, 0] == selected_module]
    if row.empty:
        return

    # Проверяем 29-й столбец — "Доступные ширины по умолчанию"
    width_options_str = str(row.iloc[0, 28]).strip()  # столбец 29
    if width_options_str and width_options_str.lower() not in ["", "nan", "нет"]:
        try:
            width_options = sorted(set(int(x.strip()) for x in width_options_str.split(",")))
            # Заменяем поле ввода ширины на выпадающий список
            width_entry.grid_forget()
            width_var.set(str(width_options[0]))  # устанавливаем первое значение
            if width_menu:
                width_menu.destroy()
            width_menu = ctk.CTkOptionMenu(
                size_frame,
                values=[str(x) for x in width_options],
                variable=width_var
            )
            width_menu.grid(row=0, column=3, padx=(0,15))
        except Exception:
            # Если ошибка — оставляем поле ввода
            if width_menu:
                width_menu.destroy()
                width_menu = None
            width_var.set(row.iloc[0, 15])  # базовая ширина
            width_entry.grid(row=0, column=3, padx=(0,15))
    else:
        # Поле ввода
        if width_menu:
            width_menu.destroy()
            width_menu = None
        width_var.set(row.iloc[0, 15])  # базовая ширина
        width_entry.grid(row=0, column=3, padx=(0,15))

    # Подставляем базовые размеры
    height_var.set(row.iloc[0, 14])
    depth_var.set(row.iloc[0, 16])

    # Проверяем 21-й столбец ("Да" — показываем поле "Высота ниши")
    value_21 = str(row.iloc[0, 20]).strip().lower()
    if value_21 == "да":
        # Проверяем 28-й столбец — "Размеры ниши по умолчанию"
        size_options_str = str(row.iloc[0, 27]).strip()  # столбец 28
        if size_options_str and size_options_str.lower() not in ["", "nan", "нет"]:
            try:
                options = sorted(set(int(x.strip()) for x in size_options_str.split(",")))
                # Создаём выпадающий список
                if height_case_menu:
                    height_case_menu.destroy()
                height_case_menu = ctk.CTkOptionMenu(
                    size_frame,
                    values=[str(x) for x in options],
                    variable=height_case_var
                )
                height_case_entry.grid_forget()
                height_case_label.grid(row=0, column=6, padx=(15,5))
                height_case_menu.grid(row=0, column=7, padx=(0,15))
                height_case_var.set(str(options[0]))  # устанавливаем первое значение из Excel
            except Exception as e:
                # Если ошибка — всё равно устанавливаем первое значение из Excel
                if height_case_menu:
                    height_case_menu.destroy()
                    height_case_menu = None
                height_case_label.grid(row=0, column=6, padx=(15,5))
                height_case_entry.grid(row=0, column=7, padx=(0,15))
                try:
                    height_case_var.set(str(options[0]))  # устанавливаем первое значение из Excel
                except:
                    height_case_var.set("")  # оставляем пустым
        else:
            # Поле ввода, но без 595 — оставляем пустым
            if height_case_menu:
                height_case_menu.destroy()
                height_case_menu = None
            height_case_label.grid(row=0, column=6, padx=(15,5))
            height_case_entry.grid(row=0, column=7, padx=(0,15))
            height_case_var.set("")  # оставляем пустым
    else:
        height_case_label.grid_forget()
        height_case_entry.grid_forget()
        if height_case_menu:
            height_case_menu.destroy()
            height_case_menu = None

    # === Полки ===
    value_min = row.iloc[0, 22]  # столбец 24
    value_max = row.iloc[0, 23]  # столбец 25
    value_25 = row.iloc[0, 24]   # столбец 26 (по умолчанию)

    glass_access = str(row.iloc[0, 25]).strip().lower() == "да"

    def safe_int(value):
        try:
            s = str(value).strip().lower()
        except Exception:
            return 0
        if s in ["нет", "", "nan", "none"]:
            return 0
        try:
            return int(float(s))
        except ValueError:
            return 0

    min_polki = safe_int(value_min)
    max_polki = safe_int(value_max)
    if max_polki < min_polki:
        max_polki = min_polki

    default_polki = safe_int(value_25)

    # Если в столбце 26 пусто или 0 — ставим максимальное значение
    if pd.isna(value_25) or default_polki == 0:
        default_polki = max_polki
    elif default_polki < min_polki:
        default_polki = min_polki
    elif default_polki > max_polki:
        default_polki = max_polki

    # === Обновляем Spinbox ===
    polki_count_spin.config(from_=min_polki, to=max_polki)
    print(f"Spinbox обновлён: from={min_polki}, to={max_polki}, default={default_polki}")
    polki_count_var.set(default_polki)

    # Настройка типа полки
    available_types = polki_types.copy()
    if not glass_access:
        available_types = [t for t in available_types if t != "Стекло"]

    new_values = available_types
    print("update_module_defaults: передаём в set_polki_type_menu:", new_values)
    set_polki_type_menu(new_values)

    # === ВАЖНО: вызываем пересчёт цены после обновления полок ===
    update_price()

def update_kompl_list(*args):
    """Обновляет список комплектаций в зависимости от выбранного модуля"""
    selected_module = module_var.get()
    if not selected_module or kompl.empty:
        kompl_menu.configure(values=["Комплектация №2"])
        kompl_var.set("Комплектация №2")
        return

    rows = kompl[kompl["name_module"].astype(str).str.strip() == str(selected_module).strip()]
    if rows.empty:
        values = ["Комплектация №2"]
    else:
        values = sorted(rows["number_kompl"].dropna().astype(str).unique().tolist())
        if not values:
            values = ["Комплектация №2"]

    kompl_menu.configure(values=values)
    kompl_var.set(values[0])

def update_module_list(*args):
    """Иерархическая фильтрация: category -> type -> filling -> module"""
    filtered_df = df.copy()

    cat = category_var.get()
    if cat:
        filtered_df = filtered_df[filtered_df.iloc[:, 1] == cat]

    types = filtered_df.iloc[:, 3].dropna().astype(str).unique().tolist()
    type_menu.configure(values=types)
    if type_var.get() not in types:
        type_var.set(types[0] if types else "")

    typ = type_var.get()
    if typ:
        filtered_df = filtered_df[filtered_df.iloc[:, 3] == typ]

    fillings = filtered_df.iloc[:, 5].dropna().astype(str).unique().tolist()
    filling_menu.configure(values=fillings)
    if filling_var.get() not in fillings:
        filling_var.set(fillings[0] if fillings else "")

    fill = filling_var.get()
    if fill:
        filtered_df = filtered_df[filtered_df.iloc[:, 5] == fill]

    modules = filtered_df.iloc[:, 0].dropna().astype(str).unique().tolist()
    module_menu.configure(values=modules)
    if module_var.get() not in modules:
        module_var.set(modules[0] if modules else "")

    # Подставляем размеры и обновляем цену
    update_module_defaults()
    update_kompl_list()
    update_price()

def update_price(*args):
    """Рассчитывает и обновляет цену корпуса, фурнитуры, комплектации, полок"""
    print("update_price вызван")
    selected_module = module_var.get()
    selected_color_name = color_var.get()
    # === Определяем категорию цвета ===
    color_row = color_korp[color_korp["Цвета"] == selected_color_name]
    if not color_row.empty:
        color_category = color_row.iloc[0]["Категория"].strip()
    else:
        color_category = "Базовый"  # по умолчанию
    selected_kompl = kompl_var.get()

    if not selected_module:
        price_var.set(0)
        furn_price_var.set("0.00")
        kompl_price_var.set("0.00")
        total_price_var.set("0.00")
        price_label.configure(text="Цена корпуса: 0.00 руб.")
        furn_price_label.configure(text="Цена фурнитуры: 0.00 руб.")
        kompl_price_label.configure(text="Цена комплектации: 0.00 руб.")
        total_price_label.configure(text="Цена корпус + фурнитура + комплектация + полки: 0.00 руб.")
        return

    price_row = df[df.iloc[:, 0] == selected_module]
    if price_row.empty:
        price_var.set(0)
        furn_price_var.set("0.00")
        kompl_price_var.set("0.00")
        total_price_var.set("0.00")
        price_label.configure(text="Цена корпуса: 0.00 руб.")
        furn_price_label.configure(text="Цена фурнитуры: 0.00 руб.")
        kompl_price_label.configure(text="Цена комплектации: 0.00 руб.")
        total_price_label.configure(text="Цена корпус + фурнитура + комплектация + полки: 0.00 руб.")
        return

    # === Базовая цена корпуса ===
    base_price_col = 12 if color_category == "Базовый" else 13
    base_price = price_row.iloc[0, base_price_col]
    if pd.isna(base_price):
        base_price = 0.0

    # === Базовые размеры ===
    baz_height = price_row.iloc[0, 14]
    baz_width  = price_row.iloc[0, 15]
    baz_depth  = price_row.iloc[0, 16]

    # === Коэффициенты ===
    coeff_height = price_row.iloc[0, 17]
    coeff_width  = price_row.iloc[0, 18]
    coeff_depth  = price_row.iloc[0, 19]

    # === Текущие размеры ===
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
                name_furn = row['name_furn']
                quantity = row['quanity']
                condition = row.get('condition', '')
                if isinstance(condition, str) and condition.strip():
                    if eval(condition, {}, {
                        "actual_width": actual_width,
                        "actual_height": actual_height,
                        "actual_depth": actual_depth
                    }):
                        if pd.notna(row.get('name_furn_changed')):
                            name_furn = row['name_furn_changed']
                        if pd.notna(row.get('changed_quantity')):
                            quantity = row['changed_quantity']
                furn_row = furn[furn['name_furn'].astype(str).str.strip() == str(name_furn).strip()]
                if not furn_row.empty:
                    furn_price = furn_row.iloc[0]['price']
                    if pd.isna(furn_price): furn_price = 0.0
                    price_furn += furn_price * quantity
            except Exception as e:
                print(f"Ошибка в kf_korp: {e}")

    # === Цена комплектации ===
    price_kompl = 0.0
    if 'kompl' in globals() and selected_kompl:
        kompl_rows = kompl[
            (kompl["name_module"].astype(str).str.strip() == str(selected_module).strip()) &
            (kompl["number_kompl"].astype(str).str.strip() == selected_kompl.strip())
        ]

        nisha_required = False
        if not df[df.iloc[:, 0] == selected_module].empty:
            nisha_value = df[df.iloc[:, 0] == selected_module].iloc[0, 20]
            nisha_required = str(nisha_value).strip().lower() == "да"

        try:
            nisha_height = 0.0
            if nisha_required:
                nisha_height = float(height_case_var.get()) if height_case_var.get() else 0.0
        except:
            nisha_height = 0.0

        for _, row in kompl_rows.iterrows():
            try:
                name_furn = row['name_furn']
                quantity = row['quanity']

                condition = row.get('condition', '')
                if isinstance(condition, str) and condition.strip():
                    eval_vars = {
                        "actual_width": actual_width,
                        "actual_height": actual_height,
                        "actual_depth": actual_depth,
                        "nisha_height": nisha_height
                    }

                    # === Обработка case_1 / case_2 ===
                    if "case_1:" in condition or "case_2:" in condition:
                        try:
                            parts = condition.split("case_2:")
                            case_1_expr = parts[0].replace("case_1:", "").strip()
                            case_2_expr = parts[1].strip() if len(parts) > 1 else ""

                            case_1 = eval(case_1_expr, {}, eval_vars) if case_1_expr else False
                            case_2 = eval(case_2_expr, {}, eval_vars) if case_2_expr else False

                            if case_1 and pd.notna(row.get('changed_quantity')):
                                quantity = row['changed_quantity']
                            elif case_2 and pd.notna(row.get('changed_quantity_case_2')):
                                quantity = row['changed_quantity_case_2']
                        except Exception as e:
                            print(f"Ошибка при обработке case: {e}")
                    # === Обычное условие ===
                    else:
                        if eval(condition, {}, eval_vars):
                            if pd.notna(row.get('name_furn_changed')):
                                name_furn = row['name_furn_changed']
                            if pd.notna(row.get('changed_quantity')):
                                quantity = row['changed_quantity']
                        else:
                            continue  # пропускаем, если условие не выполнено
                # else: ← если условия нет — просто используем фурнитуру (как раньше)

                furn_row = furn[furn['name_furn'].astype(str).str.strip() == str(name_furn).strip()]
                if not furn_row.empty:
                    furn_price = furn_row.iloc[0]['price']
                    if pd.isna(furn_price): furn_price = 0.0
                    price_kompl += furn_price * quantity
            except Exception as e:
                print(f"Ошибка в kompl: {e}")

    # === Цена полок ===
    price_polki = 0.0

    try:
        count_polki = polki_count_var.get()
        print("count_polki:", count_polki)
        if count_polki > 0:
            type_selected = polki_type_var.get().strip()
            if type_selected == "ЛДСП":
                col_name = 'Формула_расчета_полок'
            else:
                col_name = 'Формула_расчета_стеклянных_полок'
            print("type_selected:", type_selected)
            
            formula = str(price_row.iloc[0][col_name]).strip()
            print("formula (до исправления):", formula)
            if not formula or formula.lower() in ["нет", "", "nan"]:
                formula = "0"

            eval_vars = {
                "width": actual_width,
                "depth": actual_depth,
                "height": actual_height
            }

            try:
                area = eval(formula, {}, eval_vars)
                print("area:", area)
            except Exception as e:
                print(f"Ошибка в формуле: {e}")
                area = 0


            row_polka = polki[polki["Изделие"].astype(str).str.strip() == type_selected.strip()]
            print("row_polka:", row_polka)
            if not row_polka.empty:
                try:
                    price_m2 = float(row_polka.iloc[0]["Цена,м2"])
                    print("price_m2:", price_m2)
                except Exception:
                    price_m2 = 0
                    print("price_m2 (ошибка): 0")
                price_polki = area * price_m2 * count_polki
                print("price_polki:", price_polki)
    except Exception as e:
        print(f"Ошибка при расчете полок: {e}")
        price_polki = 0
    
    # === Площадь фасада ===
    facade_area = calculate_facade_area()
    facade_area_var.set(f"{facade_area:.2f}")
    facade_area_label.configure(text=f"Площадь фасада: {facade_area:.2f} м²")
    # === Цена фасада ===
    facade_price = calculate_facade_price()
    facade_price_var.set(f"{facade_price:.2f}")
    facade_price_label.configure(text=f"Цена фасадов: {facade_price:.2f} руб.")
    # === Общая цена ===
    total_price = price_corp + price_furn + price_kompl + price_polki

    # === Обновление меток ===
    price_var.set(round(total_price, 2))
    price_label.configure(text=f"Цена корпуса: {price_corp:.2f} руб.")
    furn_price_var.set(round(price_furn, 2))
    furn_price_label.configure(text=f"Цена фурнитуры: {price_furn:.2f} руб.")
    kompl_price_var.set(round(price_kompl, 2))
    kompl_price_label.configure(text=f"Цена комплектации: {price_kompl:.2f} руб.")
    
    polki_price_var.set(round(price_polki, 2))
    polki_price_label.configure(text=f"Цена полок: {price_polki:.2f} руб.")
    total_price_var.set(round(total_price, 2))
    total_price_label.configure(text=f"Цена корпус + фурнитура + комплектация + полки: {total_price:.2f} руб.")

def add_to_cart():
    """Добавляет выбранный модуль в корзину"""
    mod = module_var.get()
    cat = category_var.get()
    typ = type_var.get()
    fill = filling_var.get()
    kompl_value = kompl_var.get()
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
        total_price = float(total_price_var.get())
    except ValueError:
        total_price = 0.0

    total_price_qty = total_price * qty

    if not mod:
        return

    cart.append((mod, cat, typ, fill, kompl_value, height, width, depth, qty, total_price_qty))

    for item in tree.get_children():
        tree.delete(item)

    sum_total = 0
    for m, c, t, f, k, h, w, d, q, total_p in cart:
        tree.insert("", "end", values=(m, c, t, f, k, h, w, d, q, f"{total_p:.2f}"))
        sum_total += total_p

    total_label.configure(text=f"Итоговая сумма: {sum_total:.2f} руб.")

def remove_selected():
    """Удаляет выделенный элемент из корзины"""
    selected_item = tree.selection()
    if not selected_item:
        return
    index = tree.index(selected_item)
    del cart[index]
    tree.delete(selected_item)
    
    sum_total = sum(item[-1] for item in cart)
    total_label.configure(text=f"Итоговая сумма: {sum_total:.2f} руб.")

# -----------------
# Привязки (реакция на изменения переменных)
# -----------------
category_var.trace_add("write", update_module_list)
type_var.trace_add("write", update_module_list)
filling_var.trace_add("write", update_module_list)

color_var.trace_add("write", update_price)
height_var.trace_add("write", update_price)
width_var.trace_add("write", update_price)
depth_var.trace_add("write", update_price)
height_case_var.trace_add("write", update_price)

module_var.trace_add("write", update_module_defaults)
module_var.trace_add("write", update_kompl_list)
module_var.trace_add("write", update_price)
polki_count_var.trace_add("write", update_price)
polki_type_var.trace_add("write", update_price)

kompl_var.trace_add("write", update_price)
collection_var.trace_add("write", update_frez_list)
frez_var.trace_add("write", update_thickness_list)
frez_var.trace_add("write", update_facade_type_list)  # ← добавили

collection_var.trace_add("write", update_price)
facade_color_var.trace_add("write", update_price)
facade_thickness_var.trace_add("write", update_price)
facade_type_var.trace_add("write", update_price)
# -----------------
# Кнопки
# -----------------
add_btn = ctk.CTkButton(app, text="Добавить в корзину", command=add_to_cart)
add_btn.pack(pady=5)

remove_btn = ctk.CTkButton(app, text="Удалить выделенный модуль", command=remove_selected)
remove_btn.pack(pady=5)

# -----------------
# Инициализация
# -----------------
if df.iloc[:, 1].dropna().tolist():
    category_var.set(df.iloc[:, 1].dropna().astype(str).unique().tolist()[0])
    update_module_list()
    update_module_defaults()
    # Инициализация списка фрезеровок
if collection_options:
    update_frez_list()


app.mainloop()