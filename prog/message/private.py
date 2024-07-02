from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, BaseStateGroup
from prog.config import bot
from vkbottle_types.objects import DocsDoc, PhotosPhoto, MessagesMessage
from vkbottle.tools import DocMessagesUploader, PhotoMessageUploader
import requests
import redis.asyncio
from prog.database.routes import RoutesRepository
from prog.database.group import GroupsRepository
from prog.database.rules import RulesRepository
from re import split

teacher_ids: list[int] = [239072798]

def up_teacher_ids(ids: list[int]):
    global teacher_ids 
    teacher_ids = ids
        


teacher_labeler = BotLabeler()
teacher_labeler.auto_rules = [rules.FromPeerRule(teacher_ids)]
doc_uploader = DocMessagesUploader(bot.api)
photo_uploader = PhotoMessageUploader(bot.api)

class send(BaseStateGroup):
    WRITE = 0
    GRUPS = 1
    KURS = 2
    ROUTE = 3
#Кнопки ЕЩЁ, ОТПРАВИТЬ, ОТМЕНА

# keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
# keyboard.add(Text("Ввести текст", {"cmd": "input"}), color=KeyboardButtonColor.POSITIVE)
# keyboard.add(Text("Ещё"), color=KeyboardButtonColor.PRIMARY)
async def private_handler(r: redis.asyncio.StrictRedis, route_repo: RoutesRepository,
                            group_repo: GroupsRepository):
    

    # возврат адекватного массива из редиса
    async def out_redis(id: str) -> list[int]:

        out = split(r"[[\,\ \'\]]+", str(await r.lrange(id, 0, -1))) # type: ignore
        out = [i for i in out if i]
        out = list(map(int, out))
        return out
    
    # Функция отправки сообщения
    async def sendig_message(message: list[MessagesMessage],  id: str):
        
        select_group = await out_redis(id)

        types = await r.get(id+"s")
        if  types == "all":
            print(f"\n\n\n\n\n\n\n\n\n\n\n ВСЕОБЩАЯ \n\n\n\n\n\n\n\n")
            select_group = await group_repo.get_all_id()
        elif types == "course":
            print(f"\n\n\n\n\n\n\n\n\n\n\n ПО КУРСАМ \n\n\n\n\n\n\n\n")
            select_group = await group_repo.get_id_by_course([item if item in select_group else -1 for item in [1, 2, 4, 3]])
        elif types == "route":
            print(f"\n\n\n\n\n\n\n\n\n\n\n ПО направлениям \n\n\n\n\n\n\n\n")
            select_group = await(group_repo.get_id_by_route(select_group))
        elif types == "group":
            print(f"\n\n\n\n\n\n\n\n\n\n\n ПО группам \n\n\n\n\n\n\n\n")

        if type(select_group) != list:
            return
        
        if message[0].text != '':
            await bot.api.messages.send(peer_ids=select_group, random_id=0, message=message[0].text)

        attachments = message[0].attachments
        if attachments is not None:
            for attachment in attachments:
                
                doc: list[DocsDoc]|None  = attachment.doc
                if doc is not None:
                    url = doc.url
                    title= doc.title
                    response = requests.get(str(url))
                    docs = await doc_uploader.upload(title=title, file_source=response.content, peer_id=select_group[0])
                    await bot.api.messages.send(peer_ids=select_group, random_id=0, attachment=str(docs))

                photos: list[PhotosPhoto]|None = attachment.photo
                if photos is not None:
                    photo = photos.sizes[0]
                    if photo is not None:
                        url = photo.url.split("&from")[0]
                        response = requests.get(str(url))
                        photo = await photo_uploader.upload(file_source=response.content)
                        await bot.api.messages.send(random_id=0, peer_ids=select_group, attachment=str(photo))

    async def select_but(peer_id: str, text: str):
        select_kurs = await out_redis(peer_id)
        state = await r.get(str(peer_id+'s'))
        if state == "group":
            ids = await group_repo.get_peer_id_by_group(text)
            if ids in select_kurs:
                await r.lrem(name=peer_id, count=0, value=str(ids))# type: ignore
            else: await r.lpush(peer_id, ids) # type: ignore

        elif state == "route":
            print(f"\n\n\n\n\n\n\n\n\n\n\n {text}\n\n\n\n\n\n\n\n")
            ids = await route_repo.get_id_by_name(text)
            print(f"\n\n\n\n\n\n\n\n\n\n\n {ids}\n\n\n\n\n\n\n\n")
            if ids in select_kurs:
                print(f"\n\n\n\n\n\n\n\n\n\n\nДобавил\n\n\n\n\n\n\n\n")
                await r.lrem(name=peer_id, count=0, value=str(ids)) # type: ignore
            else: await r.lpush(peer_id, ids)# type: ignore

        else:
            if int(text[0]) in select_kurs:
                await r.lrem(name=peer_id, count=0, value=text[0]) # type: ignore
            else: await r.lpush(peer_id, text[0])# type: ignore






    #Задание групп в клаву
    async def keyb_group(id: str):
        keyboard = Keyboard()
        count = 0
        select = await out_redis(id)
        groups = await group_repo.get_list(35)
        
        if not groups:
            return Keyboard()
        elif type(select) != list:
            return Keyboard()
        else:
            for group in groups:
                if count % 5 == 0 and count != 0:
                    keyboard.row()
                    
                if group.peer_ids in select:
                    keyboard.add(Text(group.group_number), color=KeyboardButtonColor.PRIMARY)
                else:
                    keyboard.add(Text(group.group_number))
                count += 1
                
            return keyboard
        
    #Задание направления в клаву
    async def keyb_route(id: str):
        keyboard = Keyboard()
        count = 0
        select = await out_redis(id)

        routes = await route_repo.get_list(14)
        
        if not routes:
            return Keyboard()
        elif type(select) != list:
            return Keyboard()
        else:
            for route in routes:
                if count != 0:
                    keyboard.row()
                if route.id_route in select:
                    keyboard.add(Text(route.name), color=KeyboardButtonColor.PRIMARY)
                else:
                    keyboard.add(Text(route.name))
                count += 1
                
            return keyboard

    # Задаем курс в клавиатуру
    async def keyb_kurs(id: str):
        courses = [1, 2, 3, 4]
        keyboard = Keyboard()
        select_kurs = await out_redis(id)
        if type(select_kurs) != list:
            return Keyboard()
        
        for course in courses:
            if course in select_kurs:
                keyboard.add(Text(f'{course} курс'), color=KeyboardButtonColor.PRIMARY)
            else:
                keyboard.add(Text(f'{course} курс'))

        return keyboard

    # Меню клавиатуры
    def keyb_menu():
        keyboard = Keyboard()
        keyboard.add(Text("Общая рассылка", {"cmd": "all_sending"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Рассылка по группам", {"cmd": "group_sending"}))
        keyboard.row()
        keyboard.add(Text("Рассылка по курсам", {"cmd": "kurs_sending"}))
        keyboard.add(Text("Рассылка по направлению", {"cmd": "route_sending"}))
        return keyboard
    

    #Начальный этап рассылки
    @teacher_labeler.private_message(text = "Начать рассылку")
    @teacher_labeler.private_message(payload={"cmd": "menu"})
    async def _(message: Message):

        await r.delete(str(message.peer_id))

        if await bot.state_dispenser.get(message.peer_id) is not None:
            await bot.state_dispenser.delete(message.peer_id)
        
        keyboard = keyb_menu()
        await message.answer("Выберите тип рассылки", keyboard=keyboard.get_json())


    # Ввод текста
    @teacher_labeler.private_message(payload={"cmd": "input"})
    async def _(message: Message):
        await bot.state_dispenser.set(message.peer_id, send.WRITE)

        keyboard = Keyboard()
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        # добавить что типо выбраны 
        await message.answer("Введите сообщение для рассылки:", keyboard=keyboard.get_json())

    # Подтверждение рассылки
    @teacher_labeler.private_message(state=send.WRITE)
    async def _(message: Message):
        
        keyboard = Keyboard()
        keyboard.add(Text("Отправить", {"cmd": "sending"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer("Вы действительно хотите отправить данное сообщение?", keyboard=keyboard.get_json())
        
    # Начала рассылки по группам
    @teacher_labeler.private_message(payload={"cmd": "group_sending"})
    async def _(message: Message):
        await r.set(str(message.peer_id)+'s', "group")
        keyboard = await keyb_group(str(message.peer_id))
        keyboard.row()
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Выберите группы:", keyboard=keyboard.get_json())
        await bot.state_dispenser.set(message.peer_id, send.GRUPS)

    # Выбор групп на рассылку
    @teacher_labeler.private_message(state=send.GRUPS)
    async def _(message: Message):
        await select_but(str(message.peer_id), message.text)

        keyboard = await keyb_group(str(message.peer_id))
        keyboard.row()
        keyboard.add(Text("Ввести текст", {"cmd": "input"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Выберите группы:", keyboard=keyboard.get_json())

    # Начало рассылки по курсам
    @teacher_labeler.private_message(payload={"cmd": "kurs_sending"})
    async def _(message: Message):
        await r.set(str(message.peer_id)+'s', "course")

        keyboard = await keyb_kurs(str(message.peer_id))
        keyboard.row()
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Выберите курсы:", keyboard=keyboard.get_json())
        await bot.state_dispenser.set(message.peer_id, send.KURS)

    # Выбор курсов для рассылки
    @teacher_labeler.private_message(state=send.KURS)
    async def _(message: Message):
        await select_but(str(message.peer_id), message.text[0])

        keyboard = await keyb_kurs(str(message.peer_id))
        keyboard.row()
        keyboard.add(Text("Ввести текст", {"cmd": "input"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Выберите курсы:", keyboard=keyboard.get_json())

    # Начало рассылки по направлениям
    @teacher_labeler.private_message(payload={"cmd": "route_sending"})
    async def _(message: Message):
        await r.set(str(message.peer_id)+'s', "route")

        keyboard = await keyb_route(str(message.peer_id))
        keyboard.row()
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Выберите направление:", keyboard=keyboard.get_json())
        await bot.state_dispenser.set(message.peer_id, send.ROUTE)

    # Выбор направлений для рассылки
    @teacher_labeler.private_message(state=send.ROUTE)
    async def _(message: Message):
        await select_but(str(message.peer_id), message.text)

        keyboard = await keyb_route(str(message.peer_id))
        keyboard.row()
        keyboard.add(Text("Ввести текст", {"cmd": "input"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Выберите направления:", keyboard=keyboard.get_json())


    @teacher_labeler.private_message(payload={"cmd": "all_sending"})
    async def _(message: Message):
        await r.set(str(message.peer_id)+'s', "all")
        await bot.state_dispenser.set(message.peer_id, send.WRITE)

        keyboard = Keyboard()
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Введите сообщение для рассылки по всем группам:", keyboard=keyboard.get_json())


    

    @teacher_labeler.private_message(payload={"cmd": "sending"})
    async def _(message: Message):
        
        x = await bot.api.messages.get_history(count=1, peer_id=message.peer_id, start_message_id=message.id-2)
        x = x.items
        if x is not None:
            await sendig_message(x, str(message.peer_id))

        await message.answer("Отправлено!")

        await r.delete(str(message.peer_id))

        keyboard = keyb_menu()
        await message.answer("Выберите тип рассылки", keyboard=keyboard.get_json())
        



