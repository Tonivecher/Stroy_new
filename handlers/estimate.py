from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.main import get_main_keyboard
from keyboards.materials import get_material_categories_keyboard, get_materials_keyboard
from data.room import Room, RoomEstimate
from data.materials import get_materials_by_category

router = Router()

class EstimateStates(StatesGroup):
    """States for estimate creation process."""
    waiting_for_room_name = State()
    waiting_for_room_length = State()
    waiting_for_room_width = State()
    waiting_for_material_category = State()
    waiting_for_material = State()
    waiting_for_material_quantity = State()

@router.message(F.text == "📝 Новое помещение")
async def start_estimate(message: Message, state: FSMContext):
    """Start the estimate creation process."""
    await message.answer(
        "Введите название помещения:",
        reply_markup=get_main_keyboard()
    )
    await state.set_state(EstimateStates.waiting_for_room_name)

@router.message(EstimateStates.waiting_for_room_name)
async def process_room_name(message: Message, state: FSMContext):
    """Process room name and ask for length."""
    await state.update_data(name=message.text)
    await message.answer(
        "Введите длину помещения в метрах (например: 5.5):",
        reply_markup=get_main_keyboard()
    )
    await state.set_state(EstimateStates.waiting_for_room_length)

@router.message(EstimateStates.waiting_for_room_length)
async def process_room_length(message: Message, state: FSMContext):
    """Process room length and ask for width."""
    try:
        length = float(message.text.replace(',', '.'))
        if length <= 0:
            await message.answer("Длина должна быть положительным числом. Попробуйте снова:")
            return
        
        await state.update_data(length=length)
        await message.answer(
            "Введите ширину помещения в метрах:",
            reply_markup=get_main_keyboard()
        )
        await state.set_state(EstimateStates.waiting_for_room_width)
    
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число. Например: 5.5")

@router.message(EstimateStates.waiting_for_room_width)
async def process_room_width(message: Message, state: FSMContext):
    """Process room width and ask for material category."""
    try:
        width = float(message.text.replace(',', '.'))
        if width <= 0:
            await message.answer("Ширина должна быть положительным числом. Попробуйте снова:")
            return
        
        data = await state.get_data()
        room = Room(
            name=data['name'],
            length=data['length'],
            width=width
        )
        
        await state.update_data(room=room)
        await message.answer(
            "Выберите категорию материалов:",
            reply_markup=get_material_categories_keyboard()
        )
        await state.set_state(EstimateStates.waiting_for_material_category)
    
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число. Например: 3.5")

@router.message(EstimateStates.waiting_for_material_category)
async def process_material_category(message: Message, state: FSMContext):
    """Process material category and show available materials."""
    category = message.text.lower()
    materials = get_materials_by_category(category)
    
    if not materials:
        await message.answer(
            "Категория не найдена. Выберите категорию из списка:",
            reply_markup=get_material_categories_keyboard()
        )
        return
    
    await state.update_data(current_category=category)
    await message.answer(
        "Выберите материал:",
        reply_markup=get_materials_keyboard(category)
    )
    await state.set_state(EstimateStates.waiting_for_material)

@router.message(EstimateStates.waiting_for_material)
async def process_material(message: Message, state: FSMContext):
    """Process material selection and ask for quantity."""
    data = await state.get_data()
    category = data['current_category']
    materials = get_materials_by_category(category)
    
    if message.text not in [m.name for m in materials.values()]:
        await message.answer(
            "Материал не найден. Выберите материал из списка:",
            reply_markup=get_materials_keyboard(category)
        )
        return
    
    material_id = next(
        (id for id, m in materials.items() if m.name == message.text),
        None
    )
    
    if material_id:
        await state.update_data(current_material=material_id)
        room = data['room']
        area = getattr(room, f"{category}_area")
        
        await message.answer(
            f"Введите количество материала в {materials[material_id].unit}\n"
            f"(площадь поверхности: {area:.2f} {materials[material_id].unit}):",
            reply_markup=get_main_keyboard()
        )
        await state.set_state(EstimateStates.waiting_for_material_quantity)

@router.message(EstimateStates.waiting_for_material_quantity)
async def process_material_quantity(message: Message, state: FSMContext):
    """Process material quantity and update estimate."""
    try:
        quantity = float(message.text.replace(',', '.'))
        if quantity <= 0:
            await message.answer("Количество должно быть положительным числом. Попробуйте снова:")
            return
        
        data = await state.get_data()
        room = data['room']
        category = data['current_category']
        material_id = data['current_material']
        
        if 'estimate' not in data:
            data['estimate'] = RoomEstimate(room)
        
        estimate = data['estimate']
        estimate.add_material(category, material_id, quantity)
        
        await message.answer(
            "Материал добавлен в смету.\n\n"
            "Выберите следующее действие:",
            reply_markup=get_material_categories_keyboard()
        )
        await state.set_state(EstimateStates.waiting_for_material_category)
    
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.") 