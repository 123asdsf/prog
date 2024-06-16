from vkbottle.bot import BotLabeler, Message, rules

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule([239072798, 1])]

@admin_labeler.message(command="halt")
async def halt(message: Message):
    await message.answer("Ты админ!")