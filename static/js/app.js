// Глобальные переменные
let currentCart = [];

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
    if (!module) return;
    
    const response = await axios.get(`/api/module_defaults?module=${encodeURIComponent(module)}`);
    const defaults = response.data;
    
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
        document.getElementById('width').value = defaults.width_options[0];
    } else {
        widthContainer.innerHTML = `<input type="number" id="width" step="0.1" value="${defaults.width}" onchange="updatePrice()">`;
    }
    
    // Обрабатываем нишу
    const nishaContainer = document.getElementById('nisha-container');
    const nishaInputContainer = document.getElementById('nisha-input-container');
    if (defaults.nisha_required) {
        nishaContainer.style.display = 'block';
        if (defaults.nisha_options) {
            nishaInputContainer.innerHTML = `
                <select id="nisha_height" onchange="updatePrice()">
                    ${defaults.nisha_options.map(n => `<option value="${n}">${n}</option>`).join('')}
                </select>
            `;
            document.getElementById('nisha_height').value = defaults.nisha_default;
        } else {
            nishaInputContainer.innerHTML = `<input type="number" id="nisha_height" step="0.1" onchange="updatePrice()">`;
        }
    } else {
        nishaContainer.style.display = 'none';
    }
    
    // Обрабатываем полки
    document.getElementById('polki_count').value = defaults.polki_default;
    document.getElementById('polki_count').min = defaults.polki_min;
    document.getElementById('polki_count').max = defaults.polki_max;
    
    const polkiTypeSelect = document.getElementById('polki_type');
    polkiTypeSelect.innerHTML = '';
    defaults.available_polki_types.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        polkiTypeSelect.appendChild(option);
    });
    
    // Обновляем комплектации
    updateKompl();
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

// Функции для фасадов
async function updateFrez() {
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
    
    updateThickness();
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

// Работа с корзиной
async function addToCart() {
    const formData = new FormData();
    formData.append('module', document.getElementById('module').value);
    formData.append('category', document.getElementById('category').value);
    formData.append('type_val', document.getElementById('type').value);
    formData.append('filling', document.getElementById('filling').value);
    formData.append('kompl_val', document.getElementById('kompl').value);
    formData.append('height', document.getElementById('height').value);
    formData.append('width', document.getElementById('width').value);
    formData.append('depth', document.getElementById('depth').value);
    formData.append('qty', document.getElementById('qty').value);
    formData.append('total_price', document.getElementById('total_price').textContent.replace(' руб.', '').replace(/\s/g, ''));
    
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

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    updateTypes();
    updateFrez();
    updateFacadeColors();
});