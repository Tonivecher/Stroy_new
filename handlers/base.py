from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.main import get_main_keyboard, get_estimate_keyboard
from keyboards.materials import get_material_keyboard, get_material_categories, get_material_units
from data.materials import save_material, get_user_materials, format_material_info
from states import MaterialState

router = Router()

class RoomState(StatesGroup):
    waiting_for_name = State()
    waiting_for_length = State()
    waiting_for_width = State()
    waiting_for_height = State()

class MaterialCalculationState(StatesGroup):
    waiting_for_room = State()
    waiting_for_material = State()
    waiting_for_surface = State()
    waiting_for_quantity = State()

@router.message(CommandStart())
@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(
        "Добро пожаловать! Я помогу вам рассчитать смету ремонта. "
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    await message.answer(
        "🔍 <b>Как пользоваться ботом:</b>\n\n"
        "1. Нажмите 'Рассчитать площадь'\n"
        "2. Введите название помещения\n"
        "3. Укажите длину помещения\n"
        "4. Укажите ширину помещения\n"
        "5. Получите результат расчета\n\n"
        "Все сохраненные помещения будут доступны в разделе 'Мои помещения'.\n"
        "Используйте кнопки меню для навигации.",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "🔲 Рассчитать площадь")
async def handle_calculate_area(message: Message, state: FSMContext):
    """Handle area calculation request."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Помещение")],
            [KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        "Выберите, что хотите рассчитать:",
        reply_markup=keyboard
    )

@router.message(F.text == "🏠 Мои помещения")
async def handle_my_rooms(message: Message):
    """Handle my rooms request."""
    from data.rooms import get_user_rooms, format_room_info
    
    rooms = get_user_rooms(message.from_user.id)
    if not rooms:
        await message.answer(
            "У вас пока нет сохраненных помещений.\n"
            "Нажмите '🔲 Рассчитать площадь' чтобы добавить помещение.",
            reply_markup=get_main_keyboard()
        )
        return
    
    response_text = "📋 Ваши помещения:\n\n"
    for room in rooms:
        response_text += format_room_info(room) + "\n"
    
    await message.answer(response_text, reply_markup=get_main_keyboard())

@router.message(F.text == "📦 Материалы")
async def handle_materials(message: Message):
    await message.answer(
        "Выберите действие с материалами:",
        reply_markup=get_material_keyboard()
    )

@router.message(F.text == "📝 Добавить материал")
async def handle_add_material(message: Message, state: FSMContext):
    await message.answer(
        "Выберите категорию материала:",
        reply_markup=get_material_categories()
    )
    await state.set_state(MaterialState.waiting_for_category)

@router.message(MaterialState.waiting_for_category)
async def handle_material_category(message: Message, state: FSMContext):
    category = message.text
    if category not in ["Стены", "Потолок", "Пол", "Двери", "Окна"]:
        await message.answer("Пожалуйста, выберите категорию из предложенных вариантов")
        return
    
    await state.update_data(category=category)
    await message.answer("Введите название материала:")
    await state.set_state(MaterialState.waiting_for_name)

@router.message(MaterialState.waiting_for_name)
async def handle_material_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(
        "Выберите единицу измерения:",
        reply_markup=get_material_units()
    )
    await state.set_state(MaterialState.waiting_for_unit)

@router.message(MaterialState.waiting_for_unit)
async def handle_material_unit(message: Message, state: FSMContext):
    unit = message.text
    if unit not in ["м²", "м³", "шт", "кг", "л"]:
        await message.answer("Пожалуйста, выберите единицу измерения из предложенных вариантов")
        return
    
    await state.update_data(unit=unit)
    await message.answer("Введите цену за единицу измерения:")
    await state.set_state(MaterialState.waiting_for_price)

@router.message(MaterialState.waiting_for_price)
async def handle_material_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        if price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите положительное число")
        return
    
    data = await state.get_data()
    material = {
        "category": data["category"],
        "name": data["name"],
        "unit": data["unit"],
        "price": price
    }
    
    save_material(message.from_user.id, material)
    await message.answer(
        f"Материал успешно добавлен!\n{format_material_info(material)}",
        reply_markup=get_material_keyboard()
    )
    await state.clear()

@router.message(F.text == "📊 Показать материалы")
async def handle_show_materials(message: Message):
    materials = get_user_materials(message.from_user.id)
    if not materials:
        await message.answer("У вас пока нет сохраненных материалов")
        return
    
    text = "Ваши материалы:\n\n"
    for material in materials:
        text += format_material_info(material) + "\n\n"
    
    await message.answer(text, reply_markup=get_material_keyboard())

@router.message(F.text == "🏠 Главное меню")
async def handle_main_menu(message: Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "🏠 Помещение")
async def handle_add_room(message: Message, state: FSMContext):
    """Handle add room request."""
    await state.set_state(RoomState.waiting_for_name)
    await message.answer(
        "Введите название помещения:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🏠 Главное меню")]],
            resize_keyboard=True
        )
    )

@router.message(RoomState.waiting_for_name)
async def handle_room_name(message: Message, state: FSMContext):
    """Handle room name input."""
    if message.text == "🏠 Главное меню":
        await state.clear()
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        return
    
    await state.update_data(name=message.text)
    await state.set_state(RoomState.waiting_for_length)
    await message.answer("Введите длину помещения в метрах:")

@router.message(RoomState.waiting_for_length)
async def handle_room_length(message: Message, state: FSMContext):
    """Handle room length input."""
    try:
        length = float(message.text.replace(',', '.'))
        await state.update_data(length=length)
        await state.set_state(RoomState.waiting_for_width)
        await message.answer("Введите ширину помещения в метрах:")
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 3.5):")

@router.message(RoomState.waiting_for_width)
async def handle_room_width(message: Message, state: FSMContext):
    """Handle room width input."""
    try:
        width = float(message.text.replace(',', '.'))
        await state.update_data(width=width)
        await state.set_state(RoomState.waiting_for_height)
        await message.answer("Введите высоту помещения в метрах (стандартная высота 2.5 м):")
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 2.5):")

@router.message(RoomState.waiting_for_height)
async def handle_room_height(message: Message, state: FSMContext):
    """Handle room height input."""
    try:
        height = float(message.text.replace(',', '.'))
        data = await state.get_data()
        
        # Calculate areas
        floor_area = data['length'] * data['width']
        total_area = 2 * (data['length'] + data['width']) * height + floor_area
        
        # Create and save room
        from data.rooms import Room, save_room
        from datetime import datetime
        
        room = Room(
            name=data['name'],
            length=data['length'],
            width=data['width'],
            height=height,
            area=total_area,
            floor_area=floor_area,
            created_at=datetime.now()
        )
        save_room(message.from_user.id, room)
        
        await message.answer(
            f"✅ Помещение сохранено!\n\n"
            f"🏠 Название: {data['name']}\n"
            f"📏 Длина: {data['length']} м\n"
            f"📏 Ширина: {data['width']} м\n"
            f"📏 Высота: {height} м\n"
            f"📐 Общая площадь: {total_area:.2f} м²\n"
            f"📐 Площадь пола: {floor_area:.2f} м²",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 2.5):")

@router.message(F.text == "🧮 Расчет материалов")
async def handle_material_calculation(message: Message, state: FSMContext):
    """Handle material calculation request."""
    from data.rooms import get_user_rooms, format_room_info
    
    rooms = get_user_rooms(message.from_user.id)
    if not rooms:
        await message.answer(
            "❌ У вас пока нет сохраненных помещений.\n\n"
            "Для расчета материалов необходимо сначала добавить помещение:\n"
            "1. Нажмите '🔲 Рассчитать площадь'\n"
            "2. Введите параметры помещения\n"
            "3. После этого вы сможете рассчитать материалы",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Create keyboard with room names and their areas
    keyboard = []
    rooms_info = "📋 Ваши помещения с расчетом площади:\n\n"
    
    for room in rooms:
        if room.area > 0:  # Only show rooms with calculated area
            rooms_info += format_room_info(room) + "\n"
            keyboard.append([KeyboardButton(text=f"{room.name} ({room.area:.1f} м²)")])
    
    if not keyboard:  # If no rooms have area calculations
        await message.answer(
            "❌ У вас нет помещений с рассчитанной площадью.\n\n"
            "Для расчета материалов необходимо:\n"
            "1. Нажмите '🔲 Рассчитать площадь'\n"
            "2. Введите параметры помещения\n"
            "3. После этого вы сможете рассчитать материалы",
            reply_markup=get_main_keyboard()
        )
        return
    
    keyboard.append([KeyboardButton(text="🏠 Главное меню")])
    
    await state.set_state(MaterialCalculationState.waiting_for_room)
    await message.answer(
        rooms_info + "\n"
        "Выберите помещение, для которого хотите рассчитать материалы:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True
        )
    )

@router.message(MaterialCalculationState.waiting_for_room)
async def handle_calculation_room(message: Message, state: FSMContext):
    """Handle room selection for material calculation."""
    if message.text == "🏠 Главное меню":
        await state.clear()
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        return
    
    from data.rooms import get_user_rooms
    from data.materials import get_user_materials
    
    rooms = get_user_rooms(message.from_user.id)
    materials = get_user_materials(message.from_user.id)
    
    # Extract room name from the button text (remove area info)
    room_name = message.text.split(" (")[0]
    
    # Find selected room
    selected_room = next((room for room in rooms if room.name == room_name), None)
    if not selected_room:
        await message.answer(
            "❌ Пожалуйста, выберите помещение из списка выше.",
            reply_markup=get_main_keyboard()
        )
        return
    
    if not materials:
        await message.answer(
            "❌ У вас пока нет сохраненных материалов.\n\n"
            "Для расчета необходимо сначала добавить материалы:\n"
            "1. Нажмите '📝 Материалы'\n"
            "2. Выберите '📝 Добавить материал'\n"
            "3. После этого вы сможете рассчитать необходимое количество",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
        return
    
    # Create keyboard with material names and their units
    keyboard = []
    for material in materials:
        keyboard.append([KeyboardButton(text=f"{material.name} ({material.unit})")])
    keyboard.append([KeyboardButton(text="🏠 Главное меню")])
    
    await state.update_data(room=selected_room)
    await state.set_state(MaterialCalculationState.waiting_for_material)
    await message.answer(
        f"Вы выбрали помещение: {selected_room.name}\n\n"
        f"📏 Площадь: {selected_room.area:.2f} м²\n"
        f"📏 Объем: {selected_room.area * selected_room.height:.2f} м³\n\n"
        "Теперь выберите материал для расчета:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True
        )
    )

@router.message(MaterialCalculationState.waiting_for_material)
async def handle_calculation_material(message: Message, state: FSMContext):
    """Handle material selection for calculation."""
    if message.text == "🏠 Главное меню":
        await state.clear()
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        return
    
    from data.materials import get_user_materials
    
    materials = get_user_materials(message.from_user.id)
    
    # Extract material name from the button text (remove unit info)
    material_name = message.text.split(" (")[0]
    
    selected_material = next((m for m in materials if m.name == material_name), None)
    if not selected_material:
        await message.answer("Пожалуйста, выберите материал из списка.")
        return
    
    await state.update_data(material=selected_material)
    await state.set_state(MaterialCalculationState.waiting_for_surface)
    
    # Create keyboard with surface types
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧱 Стены")],
            [KeyboardButton(text="⬜ Пол")],
            [KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        f"Вы выбрали материал: {selected_material.name}\n\n"
        "Выберите тип поверхности для расчета:",
        reply_markup=keyboard
    )

@router.message(MaterialCalculationState.waiting_for_surface)
async def handle_calculation_surface(message: Message, state: FSMContext):
    """Handle surface type selection for material calculation."""
    if message.text == "🏠 Главное меню":
        await state.clear()
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        return
    
    if message.text not in ["🧱 Стены", "⬜ Пол"]:
        await message.answer("Пожалуйста, выберите тип поверхности из предложенных вариантов.")
        return
    
    data = await state.get_data()
    room = data['room']
    material = data['material']
    
    # Calculate area based on surface type
    if message.text == "🧱 Стены":
        area = 2 * (room.length + room.width) * room.height
    else:  # Пол
        area = room.length * room.width
    
    # Calculate required quantity based on material unit
    if material.unit == "м²":
        quantity = area
    elif material.unit == "м³":
        quantity = area * room.height
    else:
        quantity = 1  # Default for other units
    
    total_cost = quantity * material.price
    
    surface_type = "стен" if message.text == "🧱 Стены" else "пола"
    
    await message.answer(
        f"📊 Расчет для материала '{material.name}':\n\n"
        f"🏠 Помещение: {room.name}\n"
        f"📏 Площадь {surface_type}: {area:.2f} м²\n"
        f"📦 Требуемое количество: {quantity:.2f} {material.unit}\n"
        f"💰 Стоимость: {total_cost:.2f} ₽\n\n"
        f"Для расчета другого материала нажмите '🧮 Расчет материалов'.",
        reply_markup=get_main_keyboard()
    )
    await state.clear()

# Fallback handler for unrecognized text messages
@router.message(F.text)
async def handle_text(message: Message):
    """Handle unrecognized text messages."""
    await message.answer(
        "Пожалуйста, используйте команды /start или /help, "
        "или выберите действие из меню.",
        reply_markup=get_main_keyboard()
    ) 