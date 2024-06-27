from vkbottle.bot import BotLabeler, Message, rules
from prog.config import bot

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule([239072798, 388543929, 312934096, 324942433])]


      

@admin_labeler.message(command="halt")
async def halt(message: Message):
    await message.answer("Ты админ!")



      
