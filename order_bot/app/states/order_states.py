from aiogram.fsm.state import State, StatesGroup

class ShippingInvoice(StatesGroup):
    photo = State()
    screenshot = State()

class PaymentReceipt(StatesGroup):
    photo = State()
    screenshot = State()
    text = State()

class NovaPoshtaTtn(StatesGroup):
    photo = State()
    screenshot = State()
    text = State()

class ReceivedInvoiceScreenshot(StatesGroup):
    screenshot = State()

class GetOpen(StatesGroup):
    user = State()


class GetClose(StatesGroup):
    user = State()