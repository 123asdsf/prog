from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD 
from prog.config import labeler


@labeler.message(text="Начать")
async def all_message(message: Message):
    keyboard = Keyboard()

    keyboard.add(Text("RED"), color=KeyboardButtonColor.NEGATIVE)
    keyboard.add(Text("GREEN"), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text("BLUE"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("WHITE"))
    
    await message.answer("Keyboard", keyboard=keyboard)