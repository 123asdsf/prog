from prog.config import labeler
from vkbottle.bot import Message

@labeler.chat_message(text=["/reg <group>", "/reg"])
async def reg_group(message: Message, group=None):
    if group is not None:
        await message.answer("Вы ввели номер группы.") 

         #добавить в базу данных номер группы и ид 
    else:
        await message.answer("Вы не ввели номер группы.") 
# Добавить проверки на повторы peer_ids надо вытащить и минус 2000000000