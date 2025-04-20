from aiogram.fsm.state import StatesGroup, State

class RoomState(StatesGroup):
    waiting_for_name = State()
    waiting_for_length = State()
    waiting_for_width = State()

class OpeningState(StatesGroup):
    waiting_for_type = State()
    waiting_for_name = State()
    waiting_for_width = State()
    waiting_for_height = State()

class MaterialState(StatesGroup):
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_unit = State()
    waiting_for_price = State()

class MaterialCalculationState(StatesGroup):
    waiting_for_room = State()
    waiting_for_material = State()
    waiting_for_quantity = State() 