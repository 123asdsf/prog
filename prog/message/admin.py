from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import CtxStorage
from vkbottle import BaseStateGroup
from prog.config import bot

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule([239072798, 388543929, 312934096, 324942433])]

ctx = CtxStorage()

class RegData(BaseStateGroup):

	NAME = 0
      

@admin_labeler.message(command="halt")
async def halt(message: Message):
    await message.answer("Ты админ!")


@admin_labeler.message(text="Запиши")
async def in_name(message: Message):
    await bot.state_dispenser.set(message.peer_id, RegData.NAME)
    return "Введите ваше имя"

@admin_labeler.message(state=RegData.NAME)
async def about_handler(message: Message):
	ctx.set("name", message.text)
	return await bot.state_dispenser.delete(message.peer_id), "Готово"

    
@admin_labeler.message(text="Имя")
async def out_name(message: Message):
      name = ctx.get("name")
      await message.answer(f"{name}")


      
