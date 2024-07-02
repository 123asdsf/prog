from prog.config import labeler
from vkbottle.bot import Message
from prog.database.group import GroupsRepository
from datetime import date

async def group_handler(group_repo: GroupsRepository):
    @labeler.chat_message(text=["/reg <group>", "/reg"])
    async def _(message: Message, group=None):
        if group is not None:
            if await group_repo.get_id(message.peer_id) is None:
                await group_repo.create((message.peer_id), group, group[4], (date.today().year-int(group[2]))%10)
                await message.answer("Успено зарегистрирован.")
            else:
                await message.answer("Данный чат уже зарегистрирован.")
        else:
            await message.answer("Вы не ввели номер группы.")