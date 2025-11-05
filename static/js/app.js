// Глобальные переменные
let currentCart = [];
let currentModuleDefaults = null;
// Функции обновления списков
async function updateTypes() {
    const category = document.getElementById('category').value;
    const response = await axios.get(`/api/types?category=${encodeURIComponent(category)}`);
    const types = response.data.types;
    
    const typeSelect = document.getElementById('type');
    typeSelect.innerHTML = '';
    types.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        typeSelect.appendChild(option);
    });
    
    updateFillings();
}

async function updateFillings() {
    const category = document.getElementById('category').value;
    const type = document.getElementById('type').value;
    const response = await axios.get(`/api/fillings?category=${encodeURIComponent(category)}&type_val=${encodeURIComponent(type)}`);
    const fillings = response.data.fillings;
    
    const fillingSelect = document.getElementById('filling');
    fillingSelect.innerHTML = '';
    fillings.forEach(filling => {
        const option = document.createElement('option');
        option.value = filling;
        option.textContent = filling;
        fillingSelect.appendChild(option);
    });
    
    updateModules();
}

async function updateModules() {
    const category = document.getElementById('category').value;
    const type = document.getElementById('type').value;
    const filling = document.getElementById('filling').value;
    const response = await axios.get(`/api/modules?category=${encodeURIComponent(category)}&type_val=${encodeURIComponent(type)}&filling=${encodeURIComponent(filling)}`);
    const modules = response.data.modules;
    
    const moduleSelect = document.getElementById('module');
    moduleSelect.innerHTML = '';
    modules.forEach(module => {
        const option = document.createElement('option');
        option.value = module;
        option.textContent = module;
        moduleSelect.appendChild(option);
    });
    
    updateModuleDefaults();
}

async function updateModuleDefaults() {
    const module = document.getElementById('module').value;
    if (!module) {
        currentModuleDefaults = null;
        return;
    }
    
    const response = await axios.get(`/api/module_defaults?module=${encodeURIComponent(module)}`);
    const defaults = response.data;
    currentModuleDefaults = defaults; // ← сохраняем!   
    // Устанавливаем размеры
    document.getElementById('height').value = defaults.height;
    document.getElementById('width').value = defaults.width;
    document.getElementById('depth').value = defaults.depth;
    
    // Обрабатываем ширину
    const widthContainer = document.getElementById('width-container');
    if (defaults.width_options) {
        widthContainer.innerHTML = `
            <select id="width" onchange="updatePrice()">
                ${defaults.width_options.map(w => `<option value="${w}">${w}</option>`).join('')}
            </select>
        `;
    } else {
        widthContainer.innerHTML = `<input type="number" id="width" step="0.1" value="${defaults.width}" onchange="updatePrice()">`;
    }
    
    // Обрабатываем нишу
    const nishaContainer = document.getElementById('nisha-container');
    const nishaInputContainer = document.getElementById('nisha-input-container');
    if (defaults.nisha_required) {
        nishaContainer.style.display = 'block';
        let element;
        if (defaults.nisha_options) {
            const select = document.createElement('select');
            select.id = 'nisha_height';
            defaults.nisha_options.forEach(n => {
                const option = document.createElement('option');
                option.value = n;
                option.textContent = n;
                select.appendChild(option);
            });
            select.value = defaults.nisha_default;
            element = select;
        } else {
            const input = document.createElement('input');
            input.type = 'number';
            input.id = 'nisha_height';
            input.step = '0.1';
            input.value = defaults.nisha_default || '';
            element = input;
        }

        element.addEventListener('change', updatePrice);
        if (element.tagName === 'INPUT') {
            element.addEventListener('input', updatePrice);
        }

        nishaInputContainer.innerHTML = '';
        nishaInputContainer.appendChild(element);
    } else {
        nishaContainer.style.display = 'none';
    }
    
    // Обрабатываем полки
    const polkiCountEl = document.getElementById('polki_count');
    polkiCountEl.value = defaults.polki_default;
    polkiCountEl.min = defaults.polki_min;
    polkiCountEl.max = defaults.polki_max;
    
    const polkiTypeSelect = document.getElementById('polki_type');
    polkiTypeSelect.innerHTML = '';
    defaults.available_polki_types.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        polkiTypeSelect.appendChild(option);
    });
    
    // 🔥 КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: дожидаемся загрузки комплектаций!
    await updateKompl();
    
    // Теперь можно обновлять цену — в #kompl уже есть options
    updatePrice();
}

async function updateKompl() {
    const module = document.getElementById('module').value;
    const response = await axios.get(`/api/kompl?module=${encodeURIComponent(module)}`);
    const komplOptions = response.data.kompl_options;
    
    const komplSelect = document.getElementById('kompl');
    komplSelect.innerHTML = '';
    komplOptions.forEach(kompl => {
        const option = document.createElement('option');
        option.value = kompl;
        option.textContent = kompl;
        komplSelect.appendChild(option);
    });
}

async function updateFrez() {
    console.log('🔴 updateFrez начал работу');
    const collection = document.getElementById('collection').value;
    const response = await axios.get(`/api/frez?collection=${encodeURIComponent(collection)}`);
    const frezOptions = response.data.frez_options;
    
    const frezSelect = document.getElementById('frez');
    frezSelect.innerHTML = '';
    frezOptions.forEach(frez => {
        const option = document.createElement('option');
        option.value = frez;
        option.textContent = frez;
        frezSelect.appendChild(option);
    });
    
    console.log('🔴 Вызываю updateFacadeColors...');
    await updateFacadeColors();
    console.log('🔴 updateFacadeColors завершен');
    
    await updateThickness();
    console.log('🔴 updateFrez завершил работу');
}

async function updateThickness() {
    const collection = document.getElementById('collection').value;
    const frez = document.getElementById('frez').value;
    const response = await axios.get(`/api/thickness?collection=${encodeURIComponent(collection)}&frez_type=${encodeURIComponent(frez)}`);
    const thicknessOptions = response.data.thickness_options;
    
    const thicknessSelect = document.getElementById('thickness');
    thicknessSelect.innerHTML = '';
    thicknessOptions.forEach(thickness => {
        const option = document.createElement('option');
        option.value = thickness;
        option.textContent = thickness;
        thicknessSelect.appendChild(option);
    });
    
    updateFacadeTypes();
}

async function updateFacadeTypes() {
    const collection = document.getElementById('collection').value;
    const frez = document.getElementById('frez').value;
    const response = await axios.get(`/api/facade_types?collection=${encodeURIComponent(collection)}&frez_type=${encodeURIComponent(frez)}`);
    const facadeTypes = response.data.facade_types;
    
    const facadeTypeSelect = document.getElementById('facade_type');
    facadeTypeSelect.innerHTML = '';
    facadeTypes.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        facadeTypeSelect.appendChild(option);
    });
    
    updateGrassColors();
}

async function updateGrassColors() {
    const facadeType = document.getElementById('facade_type').value;
    const response = await axios.get(`/api/grass_colors?facade_type=${encodeURIComponent(facadeType)}`);
    const grassColors = response.data.grass_colors;
    
    const grassColorSelect = document.getElementById('grass_color');
    grassColorSelect.innerHTML = '';
    if (grassColors.length > 0) {
        grassColors.forEach(color => {
            const option = document.createElement('option');
            option.value = color;
            option.textContent = color;
            grassColorSelect.appendChild(option);
        });
    } else {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'Не требуется';
        grassColorSelect.appendChild(option);
    }
    
    updatePrice();
}

async function updateFacadeColors() {
    const collection = document.getElementById('collection').value;
    const response = await axios.get(`/api/facade_colors?collection=${encodeURIComponent(collection)}`);
    const colorOptions = response.data.color_options;
    
    const colorSelect = document.getElementById('facade_color');
    colorSelect.innerHTML = '';
    colorOptions.forEach(color => {
        const option = document.createElement('option');
        option.value = color;
        option.textContent = color;
        colorSelect.appendChild(option);
    });
    
    updatePrice();
}

// Расчет цены
async function updatePrice() {
    const formData = new FormData();
    formData.append('module', document.getElementById('module').value);
    formData.append('color', document.getElementById('color').value);
    formData.append('kompl', document.getElementById('kompl').value);
    formData.append('height', document.getElementById('height').value);
    formData.append('width', document.getElementById('width').value);
    formData.append('depth', document.getElementById('depth').value);
    formData.append('nisha_height', document.getElementById('nisha_height') ? document.getElementById('nisha_height').value : '0');
    formData.append('polki_count', document.getElementById('polki_count').value);
    formData.append('polki_type', document.getElementById('polki_type').value);
    formData.append('collection', document.getElementById('collection').value);
    formData.append('frez_type', document.getElementById('frez').value);
    formData.append('facade_color', document.getElementById('facade_color').value);
    formData.append('facade_thickness', document.getElementById('thickness').value);
    formData.append('facade_type', document.getElementById('facade_type').value);
    formData.append('grass_color', document.getElementById('grass_color').value);
    
    try {
        const response = await axios.post('/api/calculate_price', formData);
        const data = response.data;
        
        document.getElementById('price_corp').textContent = data.module_prices.price_corp.toFixed(2) + ' руб.';
        document.getElementById('price_furn').textContent = data.module_prices.price_furn.toFixed(2) + ' руб.';
        document.getElementById('price_kompl').textContent = data.module_prices.price_kompl.toFixed(2) + ' руб.';
        document.getElementById('price_polki').textContent = data.module_prices.price_polki.toFixed(2) + ' руб.';
        document.getElementById('facade_area').textContent = data.facade_area.toFixed(2) + ' м²';
        document.getElementById('facade_price').textContent = data.facade_price.toFixed(2) + ' руб.';
        document.getElementById('total_price').textContent = data.total_price.toFixed(2) + ' руб.';
    } catch (error) {
        console.error('Ошибка расчета цены:', error);
    }
}

async function addToCart() {
    const qty = parseInt(document.getElementById('qty').value) || 1;

    const priceText = document.getElementById('total_price').textContent.trim();
    let pricePerUnit = 0;

    // Очищаем строку от всего, кроме цифр, точек и запятых
    const cleaned = priceText.replace(/[^\d.,]/g, '');

    if (cleaned.includes(',')) {
        // Если есть запятая — предполагаем, что это десятичный разделитель
        pricePerUnit = parseFloat(cleaned.replace('.', '').replace(',', '.'));
    } else {
        // Если нет запятой — просто парсим как число
        pricePerUnit = parseFloat(cleaned);
    }

    pricePerUnit = pricePerUnit || 0;

    const totalPriceForCart = pricePerUnit * qty;

    console.log("Цена с экрана:", priceText);
    console.log("Очищенная строка:", cleaned);
    console.log("Цена за 1 шт:", pricePerUnit);
    console.log("Количество:", qty);
    console.log("Итоговая цена для корзины:", totalPriceForCart);

    const formData = new FormData();
    formData.append('module', document.getElementById('module').value);
    formData.append('category', document.getElementById('category').value);
    formData.append('type_val', document.getElementById('type').value);
    formData.append('filling', document.getElementById('filling').value);
    formData.append('kompl_val', document.getElementById('kompl').value);
    formData.append('height', document.getElementById('height').value);
    formData.append('width', document.getElementById('width').value);
    formData.append('depth', document.getElementById('depth').value);
    formData.append('qty', qty);
    formData.append('total_price', totalPriceForCart);
    // Добавляем фасады в корзину
    await addToFacadeCart();
    try {
        await axios.post('/api/add_to_cart', formData);
        updateCartDisplay();
    } catch (error) {
        console.error('Ошибка добавления в корзину:', error);
    }
}

async function updateCartDisplay() {
    try {
        const response = await axios.get('/api/cart');
        currentCart = response.data.cart;
        
        const cartContent = document.getElementById('cart-content');
        const cartTotal = document.getElementById('cart-total');
        
        if (currentCart.length === 0) {
            cartContent.innerHTML = '<p>Корзина пуста</p>';
            cartTotal.textContent = 'Итоговая сумма: 0.00 руб.';
            return;
        }
        
        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Модуль</th>
                        <th>Категория</th>
                        <th>Тип</th>
                        <th>Наполнение</th>
                        <th>Комплектация</th>
                        <th>Высота</th>
                        <th>Ширина</th>
                        <th>Глубина</th>
                        <th>Кол-во</th>
                        <th>Цена</th>
                        <th>Действие</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        let totalSum = 0;
        currentCart.forEach((item, index) => {
            totalSum += parseFloat(item.total_price);
            html += `
                <tr>
                    <td>${item.module}</td>
                    <td>${item.category}</td>
                    <td>${item.type}</td>
                    <td>${item.filling}</td>
                    <td>${item.kompl}</td>
                    <td>${item.height}</td>
                    <td>${item.width}</td>
                    <td>${item.depth}</td>
                    <td>${item.qty}</td>
                    <td>${parseFloat(item.total_price).toFixed(2)} руб.</td>
                    <td><button onclick="removeFromCart(${index})">Удалить</button></td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        cartContent.innerHTML = html;
        cartTotal.textContent = `Итоговая сумма: ${totalSum.toFixed(2)} руб.`;
    } catch (error) {
        console.error('Ошибка загрузки корзины:', error);
    }
}

async function removeFromCart(index) {
    try {
        const formData = new FormData();
        formData.append('index', index);
        await axios.post('/api/remove_from_cart', formData);
        updateCartDisplay();
    } catch (error) {
        console.error('Ошибка удаления из корзины:', error);
    }
}
function calculateFacadeSize(formula, height, width, depth) {
    if (!formula || typeof formula !== 'string') 
        return { height: 0, width: 0 };

    // Подготовим переменные для подстановки
    const vars = { height, width, depth };

    let heightFas = 0;
    let widthFas = 0;

    // Разбиваем строку на части по ключевым словам
    // Это более надёжный способ, чем regex
    const parts = formula.split(/height_fas\s*=|width_fas\s*=/i);

    // Находим выражения для height_fas и width_fas
    // parts[0] — до первого ключа
    // parts[1] — после height_fas =
    // parts[2] — после width_fas =
    
    // === Выражение для height_fas ===
    // Ищем строку сразу после "height_fas ="
    // Найдём индекс, где начинается "height_fas ="
    const heightIndex = formula.toLowerCase().indexOf('height_fas =');
    if (heightIndex !== -1) {
        // Найдём начало выражения (после "height_fas =")
        const start = heightIndex + 'height_fas ='.length;
        // Найдём конец — до следующего ключевого слова или конца строки
        let end = formula.length;
        const widthIndex = formula.toLowerCase().indexOf('width_fas =', start);
        if (widthIndex !== -1) {
            end = widthIndex;
        }

        let expr = formula.substring(start, end).trim();
        // Убираем лишние пробелы и ; , если есть
        expr = expr.replace(/[\s;,\n\r]+$/, '');

        // Подставляем переменные
        for (const [key, val] of Object.entries(vars)) {
            const regex = new RegExp(`\\b${key}\\b`, 'g');
            expr = expr.replace(regex, val);
        }

        try {
            heightFas = eval(expr);
        } catch (e) {
            console.warn("Ошибка вычисления высоты фасада:", expr, e);
            heightFas = 0;
        }
    }

    // === Выражение для width_fas ===
    const widthIndex = formula.toLowerCase().indexOf('width_fas =');
    if (widthIndex !== -1) {
        const start = widthIndex + 'width_fas ='.length;
        let end = formula.length;
        const heightIndex2 = formula.toLowerCase().indexOf('height_fas =', start); // если после width есть height
        if (heightIndex2 !== -1 && heightIndex2 > start) {
            end = heightIndex2;
        }

        let expr = formula.substring(start, end).trim();
        expr = expr.replace(/[\s;,\n\r]+$/, '');

        for (const [key, val] of Object.entries(vars)) {
            const regex = new RegExp(`\\b${key}\\b`, 'g');
            expr = expr.replace(regex, val);
        }

        try {
            widthFas = eval(expr);
        } catch (e) {
            console.warn("Ошибка вычисления ширины фасада:", expr, e);
            widthFas = 0;
        }
    }

    return {
        height: parseFloat(heightFas) || 0,
        width: parseFloat(widthFas) || 0
    };
}
// Функция, которая добавляет фасады в корзину фасадов
async function addToFacadeCart() {
    // === ЛОГИ В НАЧАЛЕ ФУНКЦИИ ===
    console.log("=== НАЧАЛО функции addToFacadeCart ===");

    // === ШАГ 1: Получаем текущий модуль из выпадающего списка ===
    const module = document.getElementById('module').value;
    console.log("ШАГ 1: Выбран модуль:", module);

    // === ШАГ 2: Проверяем, есть ли у нас кэшированные данные для этого модуля ===
    console.log("ШАГ 2: Проверяем, есть ли кэшированные данные (currentModuleDefaults):", currentModuleDefaults);

    // Если данных нет (например, модуль ещё не выбран или обновление не завершено), выходим
    if (!currentModuleDefaults) {
        console.warn("ШАГ 2: currentModuleDefaults пуст или не определён. Функция завершена.");
        return; // Прерываем выполнение функции
    }

    // === ШАГ 3: Получаем значения из других полей (фасад, цвет, толщина и т.д.) ===
    const collection = document.getElementById('collection').value;  // Коллекция фасада
    const frez_type = document.getElementById('frez').value;        // Тип фрезеровки
    const facade_color = document.getElementById('facade_color').value; // Цвет фасада
    const facade_thickness = document.getElementById('thickness').value; // Толщина фасада
    const facade_type = document.getElementById('facade_type').value;    // Тип фасада (глухая, витрина)
    const grass_color = document.getElementById('grass_color').value;    // Цвет стекла (если есть)
    const qty = parseInt(document.getElementById('qty').value) || 1;      // Количество (если не число, то 1)

    console.log("ШАГ 3: Получены параметры фасада:", {
        collection,
        frez_type,
        facade_color,
        facade_thickness,
        facade_type,
        grass_color,
        qty
    });

    // === ШАГ 4: Получаем размеры модуля (высота, ширина, глубина) ===
    const height = parseFloat(document.getElementById('height').value) || 0; // Высота модуля
    const width = parseFloat(document.getElementById('width').value) || 0;   // Ширина модуля
    const depth = parseFloat(document.getElementById('depth').value) || 0;   // Глубина модуля

    // Если у модуля есть ниша — получаем её высоту
    const nisha_height = document.getElementById('nisha_height') 
        ? parseFloat(document.getElementById('nisha_height').value) || 0 
        : 0;

    console.log("ШАГ 4: Размеры модуля:", { height, width, depth, nisha_height });

    // === ШАГ 5: Используем кэшированные данные, которые сохранили в updateModuleDefaults ===
    const defaults = currentModuleDefaults;
    console.log("ШАГ 5: Используем кэшированные данные модуля:", defaults);

    // === ШАГ 6: Читаем количество фасадов из кэша ===
    const facadeCount = parseInt(defaults.facade_count) || 0; // Пробуем преобразовать в число, если не получилось — будет 0
    console.log("ШАГ 6: Количество фасадов (facade_count):", defaults.facade_count, "→ преобразовано в число:", facadeCount);

    // === ШАГ 7: Проверяем, есть ли фасады у этого модуля ===
    if (facadeCount === 0) {
        console.log("ШАГ 7: Модуль не имеет фасадов (facade_count = 0). Функция завершена.");
        return; // Прерываем выполнение функции
    } else {
        console.log("ШАГ 7: У модуля есть фасады. Продолжаем.");
    }

    // === ШАГ 8: Собираем формулы для каждого фасада из кэша ===
    const facadeFormulas = []; // Массив, куда будем складывать формулы

    // Цикл: от 1 до количества фасадов (например, если facadeCount = 2, то i = 1 и i = 2)
    for (let i = 1; i <= facadeCount; i++) {
        // Формируем имя колонки: "Размеры 1 фасада", "Размеры 2 фасада" и т.д.
        const key = `Размеры ${i} фасада`;
        // Получаем значение из кэша по этому ключу
        const formula = defaults[key];

        console.log(`ШАГ 8: Формула для фасада ${i} (ключ: "${key}"):`, formula);

        // Если формула есть, и она не "nan" и не пустая строка — добавляем в массив
        if (formula && formula !== "nan" && formula !== "") {
            facadeFormulas.push(formula);
            console.log(`ШАГ 8: Формула "${formula}" добавлена в список.`);
        } else {
            console.warn(`ШАГ 8: Формула для фасада ${i} пуста или "nan". Пропускаем.`);
        }
    }

    console.log("ШАГ 8: Все собранные формулы:", facadeFormulas);

    // === ШАГ 9: Проверяем, собрали ли мы хоть какие-то формулы ===
    if (facadeFormulas.length === 0) {
        console.warn("ШАГ 9: Нет валидных формул фасадов. Функция завершена.");
        return; // Прерываем выполнение функции
    }

    // === ШАГ 10: Группируем одинаковые формулы ===
    // Это нужно, чтобы, например, если 3 фасада имеют одну и ту же формулу, не считать их по-отдельности
    const grouped = {}; // Объект, куда будем складывать: { "формула": { count: количество } }

    // Перебираем все формулы
    facadeFormulas.forEach((formula, index) => {
        // Если этой формулы ещё не было в объекте grouped
        if (!grouped[formula]) {
            grouped[formula] = { count: 0 }; // Создаём запись с нуля
        }
        grouped[formula].count += 1; // Увеличиваем счётчик на 1
    });

    console.log("ШАГ 10: Сгруппированные формулы:", grouped);

    // === ШАГ 11: Перебираем каждую уникальную формулу и обрабатываем фасады ===
    for (const [formula, data] of Object.entries(grouped)) {
        console.log(`ШАГ 11: Обрабатываем формулу "${formula}", встречается ${data.count} раз.`);

        // === ШАГ 12: Вычисляем размеры фасада по формуле ===
        // Вызываем вспомогательную функцию, которая "читает" формулу и считает высоту и ширину
        const { height: h, width: w } = calculateFacadeSize(formula, height, width, depth);
        console.log(`ШАГ 12: Вычислены размеры фасада: высота = ${h}, ширина = ${w}`);

        // === ШАГ 13: Считаем площадь одного фасада в м² ===
        const area = ((h / 1000) * (w / 1000)).toFixed(4); // мм -> м, затем умножаем
        console.log(`ШАГ 13: Площадь одного фасада: ${area} м²`);

        // === ШАГ 14: Подготавливаем данные для расчёта цены фасада ===
        const formData = new FormData();
        formData.append('module', module);
        formData.append('color', document.getElementById('color').value);
        formData.append('kompl', document.getElementById('kompl').value);
        formData.append('height', height);
        formData.append('width', width);
        formData.append('depth', depth);
        formData.append('nisha_height', nisha_height);
        formData.append('polki_count', document.getElementById('polki_count').value);
        formData.append('polki_type', document.getElementById('polki_type').value);
        formData.append('collection', collection);
        formData.append('frez_type', frez_type);
        formData.append('facade_color', facade_color);
        formData.append('facade_thickness', facade_thickness);
        formData.append('facade_type', facade_type);
        formData.append('grass_color', grass_color);

        console.log("ШАГ 14: Подготовлены данные для расчёта цены фасада:", formData);

        // === ШАГ 15: Отправляем запрос на сервер, чтобы получить цену фасада ===
        try {
            const priceResponse = await axios.post('/api/calculate_price', formData);
            console.log("ШАГ 15: Ответ от /api/calculate_price:", priceResponse.data);

            // Получаем общую цену и площадь фасадов из ответа (для расчёта цены за 1 м²)
            const totalFacadePrice = priceResponse.data.facade_price; // Цена всех фасадов (из API)
            const totalArea = priceResponse.data.facade_area;         // Площадь всех фасадов (из API)

            // Считаем цену за 1 м²
            const facadePricePerUnit = totalArea > 0 ? (totalFacadePrice / totalArea) : 0;
            console.log("ШАГ 15: Цена за 1 м² фасада:", facadePricePerUnit);

            // === РАСЧЁТ ЦЕНЫ ЗА ВСЕ ФАСАДЫ С ЭТОЙ ФОРМУЛОЙ ===
            const totalFacetPrice = facadePricePerUnit * parseFloat(area) * data.count;
            console.log(`ШАГ 15: Цена за ${data.count} шт. фасада(ов) площадью ${area} м² каждый:`, totalFacetPrice);

            // === ШАГ 16: Подготавливаем данные для добавления в корзину фасадов ===
            // === Общая площадь для всех фасадов с этой формулой ===
            const totalAreaForCart = parseFloat(area) * data.count;

            const facadeFormData = new FormData();
            facadeFormData.append('module', module);
            facadeFormData.append('collection', collection);
            facadeFormData.append('frez_type', frez_type);
            facadeFormData.append('facade_color', facade_color);
            facadeFormData.append('facade_thickness', facade_thickness);
            facadeFormData.append('facade_type', facade_type);
            facadeFormData.append('grass_color', grass_color);
            facadeFormData.append('facade_height', h); // Высота одного фасада
            facadeFormData.append('facade_width', w);  // Ширина одного фасада
            facadeFormData.append('facade_area', totalAreaForCart); // ← теперь общая площадь для всех штук
            facadeFormData.append('qty', data.count);  // Сколько штук
            facadeFormData.append('total_price', totalFacetPrice); // Цена за все штуки

            console.log("ШАГ 16: Подготовлены данные для добавления в корзину фасадов:", facadeFormData);

            // === ШАГ 17: Отправляем фасад в корзину фасадов ===
            await axios.post('/api/add_to_facade_cart', facadeFormData);
            console.log("ШАГ 17: Фасад успешно добавлен в корзину фасадов.");

        } catch (e) {
            // Если произошла ошибка — выводим её в консоль
            console.error("ШАГ 15-17: Ошибка расчёта или добавления фасада:", e);
        }
    }

    // === ШАГ 18: Обновляем отображение корзины фасадов на странице ===
    console.log("ШАГ 18: Обновляем отображение корзины фасадов.");
    updateFacadeCartDisplay();

    console.log("=== КОНЕЦ функции addToFacadeCart ===");
}

async function updateFacadeCartDisplay() {
    try {
        const response = await axios.get('/api/facade_cart');
        const facadeCart = response.data.facade_cart;

        const cartContent = document.getElementById('facade-cart-content');
        const cartTotal = document.getElementById('facade-cart-total');

        if (facadeCart.length === 0) {
            cartContent.innerHTML = '<p>Корзина фасадов пуста</p>';
            cartTotal.textContent = 'Итоговая сумма: 0.00 руб.';
            return;
        }

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Модуль</th>
                        <th>Коллекция</th>
                        <th>Фрезеровка</th>
                        <th>Цвет</th>
                        <th>Толщина</th>
                        <th>Тип</th>
                        <th>Стекло</th>
                        <th>Высота</th>
                        <th>Ширина</th>
                        <th>Площадь</th>
                        <th>Кол-во</th>
                        <th>Цена</th>
                        <th>Действие</th>
                    </tr>
                </thead>
                <tbody>
        `;

        let totalSum = 0;
        facadeCart.forEach((item, index) => {
            totalSum += parseFloat(item.total_price);
            html += `
                <tr>
                    <td>${item.module}</td>
                    <td>${item.collection}</td>
                    <td>${item.frez_type}</td>
                    <td>${item.facade_color}</td>
                    <td>${item.facade_thickness}</td>
                    <td>${item.facade_type}</td>
                    <td>${item.grass_color}</td>
                    <td>${item.facade_height.toFixed(2)}</td>
                    <td>${item.facade_width.toFixed(2)}</td>
                    <td>${item.facade_area.toFixed(2)} м²</td>
                    <td>${item.qty}</td>
                    <td>${parseFloat(item.total_price).toFixed(2)} руб.</td>
                    <td><button onclick="removeFromFacadeCart(${index})">Удалить</button></td>
                </tr>
            `;
        });

        html += '</tbody></table>';
        cartContent.innerHTML = html;
        cartTotal.textContent = `Итоговая сумма: ${totalSum.toFixed(2)} руб.`;
    } catch (error) {
        console.error('Ошибка загрузки корзины фасадов:', error);
    }
}

async function removeFromFacadeCart(index) {
    try {
        const formData = new FormData();
        formData.append('index', index);
        await axios.post('/api/remove_from_facade_cart', formData);
        updateFacadeCartDisplay();
    } catch (error) {
        console.error('Ошибка удаления из корзины фасадов:', error);
    }
}
// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    updateTypes();
    updateFrez();
    updateFacadeColors();
});