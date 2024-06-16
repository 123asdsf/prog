from prog.config import labeler
from vkbottle.bot import Message

@labeler.chat_message(text="/reg <group>")
async def reg_group(message: Message, group=None):
    if group is not None:
        pass #добавить в базу данных номер группы и ид 
    else:
        await message.answer("Вы не ввели номер группы.") 