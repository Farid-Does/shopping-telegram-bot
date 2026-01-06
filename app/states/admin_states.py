from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup




class StartingPoint(StatesGroup):
    start = State()

# add product operation FSM class
class AddProductFSM(StatesGroup):
    category = State()
    title = State()
    description = State()
    price = State()
    stock_quantity = State()
    image = State()


# edit product operation FSM class
class UpdateProductFSM(StatesGroup):
    category_title = State()
    product_id = State()
    new_price = State()
    discount_price = State()
    new_stock_quantity = State()
    is_active_status = State()


