from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, BaseStateGroup
from prog.config import bot
from prog.database.routes import RoutesRepository

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule([239072798, 388543929, 312934096, 324942433])]

class Asend(BaseStateGroup):
    WRITE = 0

@admin_labeler.message(command="adm")
@admin_labeler.message(payload={"adm": "menu"})
async def halt(message: Message):
    if await bot.state_dispenser.get(message.peer_id) is not None:
        await bot.state_dispenser.delete(message.peer_id)
    keyboard = Keyboard()
    keyboard.add(Text("Добавить направление", {"adm": "route"}))

    await message.answer("Ты админ!", keyboard=keyboard)


@admin_labeler.private_message(payload={"adm": "route"})
async def all_sending(message: Message):
    await bot.state_dispenser.set(message.peer_id, Asend.WRITE)
    keyboard = Keyboard()
    keyboard.add(Text("Отмена", {"adm": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer("Введите название направленя:", keyboard=keyboard)


@admin_labeler.private_message(state=Asend.WRITE)
async def add_route(message: Message):
    await RoutesRepository.create(name=message.text)
    await bot.state_dispenser.delete(message.peer_id)
    await message.answer("Добавлено.")
