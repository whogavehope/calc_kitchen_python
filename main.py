from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import uvicorn
from typing import Optional
import json

#uvicorn main:app --reload

app = FastAPI(title="Калькулятор модулей")

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# -----------------
# Загрузка данных из Excel
# -----------------
try:
    df = pd.read_excel("data.xlsx", sheet_name="modules")
    kf_korp = pd.read_excel("data.xlsx", sheet_name="kf_korp")
    furn = pd.read_excel("data.xlsx", sheet_name="furn")
    kompl = pd.read_excel("data.xlsx", sheet_name="kompl")
    polki = pd.read_excel("data.xlsx", sheet_name="polki")
    color_korp = pd.read_excel("data.xlsx", sheet_name="color_korp")
    color_fasades = pd.read_excel("data.xlsx", sheet_name="color_fasades")
    frez = pd.read_excel("data.xlsx", sheet_name="frez")
    price_collections = pd.read_excel("data.xlsx", sheet_name="price_collections")
    grass = pd.read_excel("data.xlsx", sheet_name="grass")
    
    polki_types = polki["Изделие"].dropna().astype(str).unique().tolist()
    color_options = color_korp["Цвета"].dropna().astype(str).tolist()
    collection_options = price_collections["Коллекция"].dropna().astype(str).unique().tolist()
    # После загрузки данных добавь:
    print("=== КОЛЛЕКЦИИ В price_collections ===")
    print(price_collections["Коллекция"].dropna().astype(str).unique().tolist())

    print("=== КОЛЛЕКЦИИ В color_fasades ===") 
    print(color_fasades["Коллекция"].dropna().astype(str).unique().tolist())
except Exception as e:
    print(f"Ошибка загрузки данных: {e}")
    # Создаем пустые DataFrame чтобы избежать ошибок
    df = pd.DataFrame()
    kf_korp = pd.DataFrame()
    furn = pd.DataFrame()
    kompl = pd.DataFrame()
    polki = pd.DataFrame()
    color_korp = pd.DataFrame()
    color_fasades = pd.DataFrame()
    frez = pd.DataFrame()
    price_collections = pd.DataFrame()
    grass = pd.DataFrame()
    polki_types = []
    color_options = []
    collection_options = []

# Глобальная переменная для корзины
cart = []

# -----------------
# Вспомогательные функции
# -----------------

def calculate_facade_area(selected_module: str, height: float, width: float, depth: float, nisha_height: float = 0.0) -> float:
    """Рассчитывает площадь фасада по формуле из Excel"""
    if not selected_module:
        return 0.0

    row = df[df.iloc[:, 0] == selected_module]
    if row.empty:
        return 0.0

    formula_col_name = "Формула_расчета_фасадов"
    if formula_col_name not in df.columns:
        return 0.0

    formula_raw = row.iloc[0][formula_col_name]
    if pd.isna(formula_raw) or str(formula_raw).strip().lower() in ["", "нет", "nan"]:
        return 0.0

    formula = str(formula_raw).strip()
    
    eval_vars = {
        "height": height,
        "width": width,
        "depth": depth,
        "nisha": nisha_height
    }

    try:
        area = eval(formula, {"__builtins__": {}}, eval_vars)
        return float(area)
    except Exception:
        return 0.0

def calculate_facade_price(collection: str, frez_type: str, color: str, thickness: str, 
                          facade_type: str, grass_color: str, facade_area: float) -> float:
    """Рассчитывает цену фасада с учётом всех параметров"""
    if not all([collection, frez_type, color, thickness, facade_type]) or facade_area <= 0:
        return 0.0

    # Определяем ценовую группу и скидку
    price_group = None
    discount = 0.0
    
    if collection == "Softline Marine":
        price_group = frez_type.strip()
        film_category = ""
    else:
        color_row = color_fasades[
            (color_fasades["Коллекция"].astype(str).str.strip() == collection.strip()) &
            (color_fasades["Номер цвета"].astype(str).str.strip() == color.strip())
        ]
        if color_row.empty:
            return 0.0

        price_group_raw = color_row.iloc[0].get("Ценовая группа")
        film_category_raw = color_row.iloc[0].get("Категория пленки")
        discount_raw = color_row.iloc[0].get("Скидка")

        if pd.isna(price_group_raw) or str(price_group_raw).strip().lower() in ["", "nan"]:
            return 0.0
            
        price_group = str(price_group_raw).strip()
        film_category = str(film_category_raw).strip() if pd.notna(film_category_raw) else ""

        if pd.notna(discount_raw):
            try:
                discount = float(discount_raw)
                discount = max(0.0, min(1.0, discount))
            except (ValueError, TypeError):
                discount = 0.0

    # Находим строку в price_collections
    filtered_pc = price_collections[
        (price_collections["Коллекция"].astype(str).str.strip() == collection.strip()) &
        (price_collections["Ценовая группа"].astype(str).str.strip() == price_group.strip())
    ]
    
    if collection != "Softline Marine" and film_category:
        filtered_pc = filtered_pc[
            filtered_pc["Категория пленки"].astype(str).str.strip() == film_category.strip()
        ]

    if filtered_pc.empty:
        return 0.0

    row = filtered_pc.iloc[0]

    # Определяем столбец цены по толщине и типу фасада
    try:
        thickness_val = int(float(thickness))
    except (ValueError, TypeError):
        thickness_val = 19
        
    col = None
    if facade_type == "Глухая":
        if thickness_val == 16:
            col = "Цена глухих 16 мм"
        elif thickness_val in (18, 19):
            col = "Цена глухих 18_19 мм"
        elif thickness_val in (20, 22):
            col = "Цена глухих 22 мм"
        else:
            col = "Цена глухих 18_19 мм"
    elif facade_type == "Витрина":
        if thickness_val == 16:
            col = "Цена витрин 16 мм"
        elif thickness_val in (18, 19):
            col = "Цена витрин 18_19 мм"
        elif thickness_val in (20, 22):
            col = "Цена витрин 22 мм"
        else:
            col = "Цена витрин 18_19 мм"
    elif facade_type == "Решетка":
        if thickness_val == 16:
            col = "Цена глухих 16 мм"
        elif thickness_val in (18, 19):
            col = "Цена глухих 18_19 мм"
        elif thickness_val in (20, 22):
            col = "Цена глухих 22 мм"
        else:
            col = "Цена глухих 18_19 мм"

    if col not in row or pd.isna(row[col]):
        return 0.0
        
    base_price_per_m2 = float(row[col])
    discounted_price_per_m2 = base_price_per_m2 * (1 - discount)

    # Доплата за фрезеровку
    frez_row = frez[
        (frez["Коллекция"].astype(str).str.strip() == collection.strip()) &
        (frez["Фрезеровка"].astype(str).str.strip() == frez_type.strip())
    ]
    
    frez_surcharge = 0.0
    is_complex_frez = False

    if facade_type == "Решетка":
        is_complex_frez = True
    elif not frez_row.empty:
        frez_type_val = frez_row.iloc[0].get("Тип Фрезеровки")
        if pd.notna(frez_type_val) and str(frez_type_val).strip().lower() == "сложная":
            is_complex_frez = True
            
        surcharge_val = frez_row.iloc[0].get("Доплата_руб_м2")
        if pd.notna(surcharge_val):
            try:
                frez_surcharge = float(surcharge_val)
            except (ValueError, TypeError):
                frez_surcharge = 0.0

    # Наценка за сложную фрезеровку
    complex_frez_surcharge_per_m2 = 0.0
    if is_complex_frez:
        complex_frez_surcharge_per_m2 = discounted_price_per_m2 * 0.25

    total_price_per_m2 = discounted_price_per_m2 + frez_surcharge + complex_frez_surcharge_per_m2
    total_price_before_grass = total_price_per_m2 * facade_area

    # Цена стекла
    grass_price = 0.0
    if facade_type in ["Витрина", "Решетка"] and grass_color:
        grass_row = grass[grass["Цвет стекла"].astype(str).str.strip() == grass_color.strip()]
        if not grass_row.empty:
            grass_price_per_m2_raw = grass_row.iloc[0]["Цена"]
            if pd.notna(grass_price_per_m2_raw):
                try:
                    grass_price_per_m2 = float(grass_price_per_m2_raw)
                    grass_price = grass_price_per_m2 * facade_area
                except ValueError:
                    grass_price = 0.0

    total_price = total_price_before_grass + grass_price
    return total_price

def calculate_module_price(selected_module: str, selected_color: str, selected_kompl: str,
                          height: float, width: float, depth: float, nisha_height: float,
                          polki_count: int, polki_type: str) -> dict:
    """Рассчитывает цену модуля"""
    if not selected_module:
        return {
            "price_corp": 0.0,
            "price_furn": 0.0,
            "price_kompl": 0.0,
            "price_polki": 0.0,
            "total_price": 0.0
        }

    price_row = df[df.iloc[:, 0] == selected_module]
    if price_row.empty:
        return {
            "price_corp": 0.0,
            "price_furn": 0.0,
            "price_kompl": 0.0,
            "price_polki": 0.0,
            "total_price": 0.0
        }

    # Определяем категорию цвета
    color_row = color_korp[color_korp["Цвета"] == selected_color]
    color_category = "Базовый"
    if not color_row.empty:
        color_category = color_row.iloc[0]["Категория"].strip()

    # Базовая цена корпуса
    base_price_col = 12 if color_category == "Базовый" else 13
    base_price = price_row.iloc[0, base_price_col]
    if pd.isna(base_price):
        base_price = 0.0

    # Базовые размеры
    baz_height = price_row.iloc[0, 14]
    baz_width = price_row.iloc[0, 15]
    baz_depth = price_row.iloc[0, 16]

    # Коэффициенты
    coeff_height = price_row.iloc[0, 17]
    coeff_width = price_row.iloc[0, 18]
    coeff_depth = price_row.iloc[0, 19]

    # Цена корпуса
    price_corp = base_price
    price_corp += ((base_price * coeff_width - base_price) / 100) * round(width - baz_width, 0)
    price_corp += ((base_price * coeff_height - base_price) / 100) * round(height - baz_height, 0)
    if (depth - baz_depth) > 0 and coeff_depth != 0:
        price_corp += ((base_price * coeff_depth - base_price) / 100) * round(depth - baz_depth, 0)

    # Цена фурнитуры
    price_furn = 0.0
    if not kf_korp.empty:
        kf_rows = kf_korp[kf_korp['name_module'] == selected_module]
        for _, row in kf_rows.iterrows():
            try:
                name_furn = row['name_furn']
                quantity = row['quanity']
                condition = row.get('condition', '')
                if isinstance(condition, str) and condition.strip():
                    if eval(condition, {}, {
                        "actual_width": width,
                        "actual_height": height,
                        "actual_depth": depth
                    }):
                        if pd.notna(row.get('name_furn_changed')):
                            name_furn = row['name_furn_changed']
                        if pd.notna(row.get('changed_quantity')):
                            quantity = row['changed_quantity']
                furn_row = furn[furn['name_furn'].astype(str).str.strip() == str(name_furn).strip()]
                if not furn_row.empty:
                    furn_price = furn_row.iloc[0]['price']
                    if pd.isna(furn_price):
                        furn_price = 0.0
                    price_furn += furn_price * quantity
            except Exception:
                continue

    # Цена комплектации
    price_kompl = 0.0
    if not kompl.empty and selected_kompl:
        kompl_rows = kompl[
            (kompl["name_module"].astype(str).str.strip() == str(selected_module).strip()) &
            (kompl["number_kompl"].astype(str).str.strip() == selected_kompl.strip())
        ]

        for _, row in kompl_rows.iterrows():
            try:
                name_furn = row['name_furn']
                quantity = row['quanity']  # ← базовое количество ВСЕГДА берётся
                condition = row.get('condition', '')

                # Если условие есть — пытаемся его обработать, чтобы ПОМЕНЯТЬ параметры
                if isinstance(condition, str) and condition.strip():
                    eval_vars = {
                        "actual_width": width,
                        "actual_height": height,
                        "actual_depth": depth,
                        "nisha_height": nisha_height
                    }

                    if "case_1:" in condition or "case_2:" in condition:
                        parts = condition.split("case_2:")
                        case_1_expr = parts[0].replace("case_1:", "").strip()
                        case_2_expr = parts[1].strip() if len(parts) > 1 else ""

                        case_1 = eval(case_1_expr, {}, eval_vars) if case_1_expr else False
                        case_2 = eval(case_2_expr, {}, eval_vars) if case_2_expr else False

                        # Меняем количество ТОЛЬКО если условие выполнилось и есть новое значение
                        if case_1 and pd.notna(row.get('changed_quantity')):
                            quantity = row['changed_quantity']
                        elif case_2 and pd.notna(row.get('changed_quantity_case_2')):
                            quantity = row['changed_quantity_case_2']
                        # Если ни одно условие не выполнилось — оставляем БАЗОВОЕ количество
                        # ← НИКАКОГО should_include = False!

                    else:
                        # Обычное условие (не case_1/case_2)
                        if eval(condition, {}, eval_vars):
                            if pd.notna(row.get('name_furn_changed')):
                                name_furn = row['name_furn_changed']
                            if pd.notna(row.get('changed_quantity')):
                                quantity = row['changed_quantity']
                        else:
                            # ← Даже если условие ложно — всё равно оставляем базовое количество!
                            # Потому что в старой логике условие было "дополнительным", а не "обязательным"
                            pass  # ← НИЧЕГО НЕ ДЕЛАЕМ, но НЕ ПРОПУСКАЕМ

                # В ЛЮБОМ случае (с условием или без) — добавляем позицию
                furn_row = furn[furn['name_furn'].astype(str).str.strip() == str(name_furn).strip()]
                if not furn_row.empty:
                    furn_price = furn_row.iloc[0]['price']
                    if pd.isna(furn_price):
                        furn_price = 0.0
                    price_kompl += furn_price * quantity

            except Exception as e:
                print(f"Ошибка при обработке комплектации: {e}")
                continue
    # Цена полок
    price_polki = 0.0
    try:
        if polki_count > 0 and polki_type:
            if polki_type == "ЛДСП":
                col_name = 'Формула_расчета_полок'
            else:
                col_name = 'Формула_расчета_стеклянных_полок'

            formula = str(price_row.iloc[0][col_name]).strip()
            if not formula or formula.lower() in ["нет", "", "nan"]:
                formula = "0"

            eval_vars = {
                "width": width,
                "depth": depth,
                "height": height
            }

            try:
                area = eval(formula, {}, eval_vars)
            except Exception:
                area = 0

            row_polka = polki[polki["Изделие"].astype(str).str.strip() == polki_type.strip()]
            if not row_polka.empty:
                try:
                    price_m2 = float(row_polka.iloc[0]["Цена,м2"])
                    price_polki = area * price_m2 * polki_count
                except Exception:
                    price_polki = 0
    except Exception:
        price_polki = 0

    total_price = price_corp + price_furn + price_kompl + price_polki

    return {
        "price_corp": round(price_corp, 2),
        "price_furn": round(price_furn, 2),
        "price_kompl": round(price_kompl, 2),
        "price_polki": round(price_polki, 2),
        "total_price": round(total_price, 2)
    }

# -----------------
# API endpoints
# -----------------

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    """Главная страница с калькулятором"""
    categories = df.iloc[:, 1].dropna().astype(str).unique().tolist() if not df.empty else []
    default_category = categories[0] if categories else ""
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "categories": categories,
        "color_options": color_options,
        "collection_options": collection_options,
        "polki_types": polki_types,
        "default_category": default_category
    })

@app.get("/api/types")
async def get_types(category: str):
    """Получить типы для выбранной категории"""
    if df.empty:
        return {"types": []}
    
    filtered_df = df[df.iloc[:, 1] == category]
    types = filtered_df.iloc[:, 3].dropna().astype(str).unique().tolist()
    return {"types": types}

@app.get("/api/fillings")
async def get_fillings(category: str, type_val: str):
    """Получить наполнения для выбранной категории и типа"""
    if df.empty:
        return {"fillings": []}
    
    filtered_df = df[(df.iloc[:, 1] == category) & (df.iloc[:, 3] == type_val)]
    fillings = filtered_df.iloc[:, 5].dropna().astype(str).unique().tolist()
    return {"fillings": fillings}

@app.get("/api/modules")
async def get_modules(category: str, type_val: str, filling: str):
    """Получить модули для выбранной категории, типа и наполнения"""
    if df.empty:
        return {"modules": []}
    
    filtered_df = df[(df.iloc[:, 1] == category) & (df.iloc[:, 3] == type_val) & (df.iloc[:, 5] == filling)]
    modules = filtered_df.iloc[:, 0].dropna().astype(str).unique().tolist()
    return {"modules": modules}

@app.get("/api/module_defaults")
async def get_module_defaults(module: str):
    """Получить настройки по умолчанию для выбранного модуля"""
    if df.empty or not module:
        return {"error": "Модуль не найден"}
    
    row = df[df.iloc[:, 0] == module]
    if row.empty:
        return {"error": "Модуль не найден"}
    
    module_data = row.iloc[0]
    
    # Базовые размеры
    defaults = {
        "height": float(module_data[14]) if pd.notna(module_data[14]) else 0,
        "width": float(module_data[15]) if pd.notna(module_data[15]) else 0,
        "depth": float(module_data[16]) if pd.notna(module_data[16]) else 0,
    }
    
    # Доступные ширины
    width_options_str = str(module_data[28]).strip()
    if width_options_str and width_options_str.lower() not in ["", "nan", "нет"]:
        try:
            width_options = sorted(set(int(x.strip()) for x in width_options_str.split(",")))
            defaults["width_options"] = width_options
        except Exception:
            defaults["width_options"] = None
    else:
        defaults["width_options"] = None
    
    # Настройки ниши
    nisha_required = str(module_data[20]).strip().lower() == "да"
    defaults["nisha_required"] = nisha_required
    
    if nisha_required:
        size_options_str = str(module_data[27]).strip()
        if size_options_str and size_options_str.lower() not in ["", "nan", "нет"]:
            try:
                nisha_options = sorted(set(int(x.strip()) for x in size_options_str.split(",")))
                defaults["nisha_options"] = nisha_options
                defaults["nisha_default"] = nisha_options[0]
            except Exception:
                defaults["nisha_options"] = None
                defaults["nisha_default"] = ""
        else:
            defaults["nisha_options"] = None
            defaults["nisha_default"] = ""
    
    # Настройки полок
    min_polki = int(module_data[22]) if pd.notna(module_data[22]) else 0
    max_polki = int(module_data[23]) if pd.notna(module_data[23]) else 0
    default_polki = int(module_data[24]) if pd.notna(module_data[24]) else max_polki
    
    if default_polki < min_polki:
        default_polki = min_polki
    elif default_polki > max_polki:
        default_polki = max_polki
        
    defaults["polki_min"] = min_polki
    defaults["polki_max"] = max_polki
    defaults["polki_default"] = default_polki
    
    # Доступные типы полок
    glass_access = str(module_data[25]).strip().lower() == "да"
    available_polki_types = polki_types.copy()
    if not glass_access:
        available_polki_types = [t for t in available_polki_types if t != "Стекло"]
    
    defaults["available_polki_types"] = available_polki_types
    
    return defaults

@app.get("/api/kompl")
async def get_kompl(module: str):
    """Получить комплектации для выбранного модуля"""
    if kompl.empty or not module:
        return {"kompl_options": ["Комплектация №2"]}
    
    rows = kompl[kompl["name_module"].astype(str).str.strip() == str(module).strip()]
    if rows.empty:
        kompl_options = ["Комплектация №2"]
    else:
        kompl_options = sorted(rows["number_kompl"].dropna().astype(str).unique().tolist())
        if not kompl_options:
            kompl_options = ["Комплектация №2"]
    
    return {"kompl_options": kompl_options}

@app.get("/api/frez")
async def get_frez(collection: str):
    """Получить фрезеровки для выбранной коллекции"""
    if frez.empty or not collection:
        return {"frez_options": ["Без фрезеровки"]}
    
    filtered_frez = frez[
        frez["Коллекция"].astype(str).str.strip() == collection.strip()
    ]
    frez_options = filtered_frez["Фрезеровка"].dropna().astype(str).unique().tolist() if not filtered_frez.empty else ["Без фрезеровки"]
    
    return {"frez_options": frez_options}

@app.get("/api/facade_colors")
async def get_facade_colors(collection: str):
    """Получить цвета фасада для выбранной коллекции"""
    if color_fasades.empty or not collection:
        return {"color_options": ["Без цвета"]}
    
    # ДЛЯ ДЕБАГА - посмотрим что есть в данных
    print(f"=== ЗАПРОС ЦВЕТОВ ДЛЯ КОЛЛЕКЦИИ: '{collection}' ===")
    print("Все коллекции в color_fasades:", color_fasades["Коллекция"].astype(str).str.strip().unique().tolist())
    
    filtered_colors = color_fasades[
        color_fasades["Коллекция"].astype(str).str.strip() == collection.strip()
    ]
    
    print(f"Найдено строк: {len(filtered_colors)}")
    
    if filtered_colors.empty:
        color_options = ["Без цвета"]
    else:
        color_options = filtered_colors["Номер цвета"].dropna().astype(str).unique().tolist()
        if not color_options:
            color_options = ["Без цвета"]
    
    print(f"Возвращаемые цвета: {color_options}")
    print("===")
    
    return {"color_options": color_options}

@app.get("/api/thickness")
async def get_thickness(collection: str, frez_type: str):
    """Получить толщины для выбранной коллекции и фрезеровки"""
    if frez.empty or not collection or not frez_type:
        return {"thickness_options": ["19"]}
    
    filtered = frez[
        (frez["Коллекция"].astype(str).str.strip() == collection.strip()) &
        (frez["Фрезеровка"].astype(str).str.strip() == frez_type.strip())
    ]
    
    if filtered.empty:
        thickness_options = ["19"]
    else:
        thicknesses = set()
        for _, row in filtered.iterrows():
            t1 = row.get("Толщина 1")
            t2 = row.get("Толщина 2")
            
            if pd.notna(t1) and str(t1).strip().lower() not in ["", "nan"]:
                try:
                    thicknesses.add(str(int(float(t1))))
                except (ValueError, TypeError):
                    pass
            
            if pd.notna(t2) and str(t2).strip().lower() not in ["", "nan", "0"]:
                try:
                    thicknesses.add(str(int(float(t2))))
                except (ValueError, TypeError):
                    pass
        
        thickness_options = sorted(thicknesses, key=int) if thicknesses else ["19"]
    
    return {"thickness_options": thickness_options}

@app.get("/api/facade_types")
async def get_facade_types(collection: str, frez_type: str):
    """Получить типы фасада для выбранной коллекции и фрезеровки"""
    options = []
    
    if collection.strip().lower() != "frame":
        options.append("Глухая")
    
    if not frez.empty and collection and frez_type:
        filtered = frez[
            (frez["Коллекция"].astype(str).str.strip() == collection.strip()) &
            (frez["Фрезеровка"].astype(str).str.strip() == frez_type.strip())
        ]
        if not filtered.empty:
            has_vitrina = (filtered["Наличие_витрин"].astype(str).str.strip().str.lower().eq("да").any())
            has_reshetka = (filtered["Наличие_решеток"].astype(str).str.strip().str.lower().eq("да").any())
            if has_vitrina:
                options.append("Витрина")
            if has_reshetka:
                options.append("Решетка")
    
    return {"facade_types": options}

@app.get("/api/grass_colors")
async def get_grass_colors(facade_type: str):
    """Получить цвета стекла для выбранного типа фасада"""
    if facade_type in ["Витрина", "Решетка"]:
        grass_color_options = grass["Цвет стекла"].dropna().astype(str).unique().tolist()
        return {"grass_colors": grass_color_options}
    else:
        return {"grass_colors": []}

@app.post("/api/calculate_price")
async def calculate_total_price(
    module: str = Form(...),
    color: str = Form(...),
    kompl: str = Form(...),
    height: float = Form(...),
    width: float = Form(...),
    depth: float = Form(...),
    nisha_height: float = Form(0.0),
    polki_count: int = Form(0),
    polki_type: str = Form(""),
    collection: str = Form(""),
    frez_type: str = Form(""),
    facade_color: str = Form(""),
    facade_thickness: str = Form(""),
    facade_type: str = Form(""),
    grass_color: str = Form("")
):
    """Рассчитать общую цену"""
    try:
        # Цена модуля
        module_prices = calculate_module_price(
            module, color, kompl, height, width, depth, 
            nisha_height, polki_count, polki_type
        )
        
        # Площадь и цена фасада
        facade_area = calculate_facade_area(module, height, width, depth, nisha_height)
        facade_price = calculate_facade_price(
            collection, frez_type, facade_color, facade_thickness,
            facade_type, grass_color, facade_area
        )
        
        total_price = module_prices["total_price"] + facade_price
        
        return {
            "module_prices": module_prices,
            "facade_area": round(facade_area, 2),
            "facade_price": round(facade_price, 2),
            "total_price": round(total_price, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка расчета: {str(e)}")

@app.post("/api/add_to_cart")
async def add_to_cart(
    request: Request,
    module: str = Form(...),
    category: str = Form(...),
    type_val: str = Form(...),
    filling: str = Form(...),
    kompl_val: str = Form(...),
    height: float = Form(...),
    width: float = Form(...),
    depth: float = Form(...),
    qty: int = Form(...),
    total_price: float = Form(...)
):
    """Добавить модуль в корзину"""
    global cart
    
    cart.append({
        "module": module,
        "category": category,
        "type": type_val,
        "filling": filling,
        "kompl": kompl_val,
        "height": height,
        "width": width,
        "depth": depth,
        "qty": qty,
        "total_price": total_price
    })
    
    return {"success": True, "cart_size": len(cart)}

@app.get("/api/cart")
async def get_cart():
    """Получить содержимое корзины"""
    return {"cart": cart}

@app.post("/api/remove_from_cart")
async def remove_from_cart(index: int = Form(...)):
    """Удалить элемент из корзины"""
    global cart
    
    if 0 <= index < len(cart):
        cart.pop(index)
        return {"success": True, "cart_size": len(cart)}
    else:
        raise HTTPException(status_code=400, detail="Неверный индекс")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)