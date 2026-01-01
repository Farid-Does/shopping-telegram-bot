from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# browsing store steps
class BrowseSteps(StatesGroup):
    category_products = State()
    product_details = State()