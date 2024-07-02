from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, BaseStateGroup
from prog.config import bot
from prog.database.routes import RoutesRepository
from prog.database.users import UsersRepository
from prog.message.private import up_teacher_ids

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(239072798)]

class Asend(BaseStateGroup):
    WRITE = 0
    TEACHER = 0



async def admins_handler(route_repo: RoutesRepository, user_repo: UsersRepository):
    

    def start_keyboard():
        keyboard = Keyboard()
        keyboard.add(Text("Добавить направление", {"adm": "route"}))
        keyboard.add(Text("Добавить учителя"))
        keyboard.row()
        keyboard.add(Text("Перейти к рассылке", {"cmd": "menu"}))
        return keyboard


    @admin_labeler.message(command="adm")
    @admin_labeler.message(payload={"adm": "menu"})
    async def _(message: Message):
        if await bot.state_dispenser.get(message.peer_id) is not None:
            await bot.state_dispenser.delete(message.peer_id)

        await message.answer("Ты админ!", keyboard=start_keyboard().get_json())


    @admin_labeler.private_message(payload={"adm": "route"})
    async def _(message: Message):
        await bot.state_dispenser.set(message.peer_id, Asend.WRITE)
        keyboard = Keyboard()
        keyboard.add(Text("Отмена", {"adm": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Введите название направленияя:", keyboard=keyboard.get_json())


    @admin_labeler.private_message(state=Asend.WRITE)
    async def _(message: Message):
        await route_repo.create(name=message.text)
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer("Добавлено.", keyboard=start_keyboard().get_json())


    @admin_labeler.private_message(text="Добавить учителя")
    async def _(message: Message):
        await message.answer("Что бы добавить учителя введите /new_teacher id_vk фамилия имя отчество:")
    

    @admin_labeler.private_message(text=["/new_teacher <peer_id> <surname> <name> <last_name>", "/new_teacher"])
    async def _(message: Message, peer_id=None, surname=None, last_name=None, name=None):

        if peer_id!=None and surname!=None and last_name!=None and name!=None:
            if peer_id[0] == "i":
                await message.answer("Введите id_vk без id.")
            else:
                await user_repo.create(peer_id=peer_id, name=name, surname=surname, last_name=last_name, rule=1)
                await message.answer("Преподователь добавлен.")

                up_teacher_ids(await user_repo.get_ids_by_role(1))
        else:
            await message.answer("Неверный формат ввода.")