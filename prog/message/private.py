from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD

teacher_labeler = BotLabeler()
teacher_labeler.auto_rules = [rules.FromPeerRule(239072798)]

#Кнопки ЕЩЁ, ОТПРАВИТЬ, ОТМЕНА

# keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
# keyboard.add(Text("Отправить"), color=KeyboardButtonColor.POSITIVE)
# keyboard.add(Text("Ещё"), color=KeyboardButtonColor.PRIMARY)


group = ["1", "2", "3", "4", "5", "1", "2", "3", "4", "5", "1", "2", "3", "4", "5"]
#Задание групп в клаву
def keyb_group():
    keyboard = Keyboard()
    count = 0
    for i in group:
        if count % 5 == 0 and count != 0:
            keyboard.row()        
        keyboard.add(Text(i))
        count += 1
        print(count % 5)
    return keyboard


#Начальный этап рассылки
@teacher_labeler.private_message(text = "Начать рассылку")
@teacher_labeler.private_message(payload={"cmd": "menu"})
async def start_sending(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("Общая рассылка", {"cmd": "all_sending"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Рассылка по группам", {"cmd": "group_sending"}))
    keyboard.row()
    keyboard.add(Text("Рассылка по курсам", {"cmd": "kurs_sending"}))
    keyboard.add(Text("Рассылка по направлению", {"cmd": "route_sending"}))

    await message.answer("Выберите тип рассылки", keyboard=keyboard)



@teacher_labeler.private_message(payload={"cmd": "all_sending"})
async def all_sending(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer("Введите текст:", keyboard=keyboard)

# реализовать ожидание текста и отправить

    await message.answer("Отправлено всем!")


@teacher_labeler.private_message(payload={"cmd": "group_sending"})
async def group_sending(message: Message):
    keyboard = keyb_group()
    keyboard.row()
    keyboard.add(Text("Ещё"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Отправить"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    # Рализовать бесконечный выбор и отмена выбора групп.
    await message.answer("Выберите группы:", keyboard=keyboard)


@teacher_labeler.private_message(payload={"cmd": "kurs_sending"})
async def kurs_sending(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("1 курс"))
    keyboard.add(Text("2 курс"))
    keyboard.add(Text("3 курс"))
    keyboard.add(Text("4 курс"))
    keyboard.row()
    keyboard.add(Text("1 курс магистратуры"))
    keyboard.add(Text("2 курс магистратуры"))
    keyboard.row()
    keyboard.add(Text("Отправить"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    # Рализовать бесконечный выбор и отмена выбора групп.
    await message.answer("Выберите курсы:", keyboard=keyboard)

@teacher_labeler.private_message(payload={"cmd": "route_sending"})
async def route_sending(message: Message):
    pass