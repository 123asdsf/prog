from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, BaseStateGroup
from prog.config import bot
from vkbottle_types.objects import DocsDoc, PhotosPhoto
from vkbottle.tools import DocMessagesUploader, PhotoMessageUploader
import requests
from prog.database.routes import RoutesRepository
from prog.database.group import GroupsRepository
from prog.database.rules import RulesRepository


teacher_labeler = BotLabeler()
teacher_labeler.auto_rules = [rules.FromPeerRule(239072798)]
doc_uploader = DocMessagesUploader(bot.api)
photo_uploader = PhotoMessageUploader(bot.api)

class send(BaseStateGroup):
    WRITE = 0
    GRUPS = 1
    KURS = 2

#Кнопки ЕЩЁ, ОТПРАВИТЬ, ОТМЕНА

# keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
# keyboard.add(Text("Ввести текст", {"cmd": "input"}), color=KeyboardButtonColor.POSITIVE)
# keyboard.add(Text("Ещё"), color=KeyboardButtonColor.PRIMARY)
async def private_handler(route_repo: RoutesRepository,
                            group_repo: GroupsRepository):


    #Задание групп в клаву
    async def keyb_group(select_group: list[int]):
        keyboard = Keyboard()
        count = 0

        groups = await group_repo.get_list(35)

        if not groups:
            return Keyboard()
        else:
            for group in groups:
                if count % 5 == 0 and count != 0:
                    keyboard.row()
                if group.peer_ids in select_group:
                    keyboard.add(Text(group.group_number), color=KeyboardButtonColor.PRIMARY)
                keyboard.add(Text(group.group_number))
                count += 1
                # Реализовать проверку на нажатие и отжатие
            return keyboard

    def keyb_kurs(courses: list[str], select_kurs: list[str]):
        keyboard = Keyboard()
        for course in courses:
            if course in select_kurs:
                keyboard.add(Text(course), color=KeyboardButtonColor.PRIMARY)
            else:
                keyboard.add(Text(course))
        return keyboard


    #Начальный этап рассылки
    @teacher_labeler.private_message(text = "Начать рассылку")
    @teacher_labeler.private_message(payload={"cmd": "menu"})
    async def _(message: Message):
        if await bot.state_dispenser.get(message.peer_id) is not None:
            await bot.state_dispenser.delete(message.peer_id)
        keyboard = Keyboard()
        keyboard.add(Text("Общая рассылка", {"cmd": "all_sending"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Рассылка по группам", {"cmd": "group_sending"}))
        keyboard.row()
        keyboard.add(Text("Рассылка по курсам", {"cmd": "kurs_sending"}))
        keyboard.add(Text("Рассылка по направлению", {"cmd": "route_sending"}))

        await message.answer("Выберите тип рассылки", keyboard=keyboard.get_json())

    #@teacher_labeler.private_message()
    @teacher_labeler.private_message(payload={"cmd": "group_sending"})
    async def _(message: Message):
        keyboard = await keyb_group([])
        keyboard.row()
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        # Рализовать бесконечный выбор и отмена выбора групп.
        await message.answer("Выберите группы:", keyboard=keyboard.get_json())
        await bot.state_dispenser.set(message.peer_id, send.GRUPS)


    @teacher_labeler.private_message(state=send.GRUPS)
    async def _(message: Message):
        # если отмена, то переходим дальше.
        # тут типо добавляем, что выбрали
        keyboard = await keyb_group([]) #сюда отправлем выбранные кнопки
        keyboard.row()
        # если много групп то добавить кнопку ещё
        # keyboard.add(Text("Ещё"), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Ввести текст", {"cmd": "input"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Выберите группы:", keyboard=keyboard.get_json())


    @teacher_labeler.private_message(payload={"cmd": "kurs_sending"})
    async def _(message: Message):
        courses = ["1 курс", "2 курс", "3 курс", "4 курс"]
        keyboard = keyb_kurs(courses,[])
        keyboard.row()
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        # Рализовать бесконечный выбор и отмена выбора курсов.
        await message.answer("Выберите курсы:", keyboard=keyboard.get_json())
        await bot.state_dispenser.set(message.peer_id, send.KURS)


    @teacher_labeler.private_message(state=send.KURS)
    async def _(message: Message):
        await message.answer(message=message.text)
        courses = ["1 курс", "2 курс", "3 курс", "4 курс"]
        select_kurs = []
        if message.text in courses:
            select_kurs.append(message.text)
        # если отмена, то переходим дальше.
        # тут типо добавляем, что выбрали
        keyboard = keyb_kurs(courses, select_kurs) #сюда отправлем выбранные кнопки
        keyboard.row()
        # если много групп то добавить кнопку ещё
        # keyboard.add(Text("Ещё"), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Ввести текст", {"cmd": "input"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Выберите курсы:", keyboard=keyboard.get_json())


    @teacher_labeler.private_message(payload={"cmd": "route_sending"})
    async def _(message: Message):
        pass


    @teacher_labeler.private_message(payload={"cmd": "all_sending"})
    async def _(message: Message):
        await bot.state_dispenser.set(message.peer_id, send.WRITE)
        keyboard = Keyboard()
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await message.answer("Введите сообщение для рассылки по всем группам:", keyboard=keyboard.get_json())



    @teacher_labeler.private_message(payload={"cmd": "input"})
    async def _(message: Message):
        await bot.state_dispenser.set(message.peer_id, send.WRITE)
        keyboard = Keyboard()
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        # добавить что типо выбраны 
        await message.answer("Введите сообщение для рассылки:", keyboard=keyboard.get_json())


    @teacher_labeler.private_message(state=send.WRITE)
    async def _(message: Message):
        # сохранить данные для отправки
        keyboard = Keyboard()
        keyboard.add(Text("Отправить", {"cmd": "sending"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer("Вы действительно хотите отправить данное сообщение?", keyboard=keyboard.get_json())
        

    @teacher_labeler.private_message(payload={"cmd": "sending"})
    async def _():
        pass



    # files_Photo: list[PhotosPhoto]|None = message.get_photo_attachments()

    # if files_Photo is not None:
    #     for photos in files_Photo:
    #         if photos.sizes is not None:
    #             url =  photos.sizes[0].url.split("&from")[0]
    #             response = requests.get(str(url))
    #             photo = await photo_uploader.upload(file_source=response.content)
    #             await bot.api.messages.send(chat_id=1, random_id=0, attachment=str(photo))    


    # if message.text != '':
    #     await bot.api.messages.send(chat_id=1, random_id=0, message=message.text)


    # files_Doc: list[DocsDoc]|None = message.get_doc_attachments()

    # if files_Doc is not None:
    #     for docs in files_Doc:
    #         response = requests.get(str(docs.url))
    #         doc = await doc_uploader.upload(title=docs.title, file_source=response.content, peer_id=2000000001) # peer id куда кидать
    #         await bot.api.messages.send(chat_id=1, random_id=0, attachment=str(doc))