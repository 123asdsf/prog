from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, BaseStateGroup
from prog.config import bot

teacher_labeler = BotLabeler()
teacher_labeler.auto_rules = [rules.FromPeerRule(239072798)]


class send(BaseStateGroup):
    WRITE = 0

#Кнопки ЕЩЁ, ОТПРАВИТЬ, ОТМЕНА

# keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
# keyboard.add(Text("Ввести текст", {"cmd": "sending"}), color=KeyboardButtonColor.POSITIVE)
# keyboard.add(Text("Ещё"), color=KeyboardButtonColor.PRIMARY)


group = ["1", "2", "3", "4", "5", "1", "2", "3", "4", "5", "1", "2", "3", "4", "5"]
#Задание групп в клаву
def keyb_group():
    keyboard = Keyboard()
    count = 0
    for i in group:
        if count % 5 == 0 and count != 0:
            keyboard.row()

        keyboard.add(Text(i), {"cmd": "group_sending"})
        count += 1
        # Реализовать проверку на нажатие и отжатие
    return keyboard


#Начальный этап рассылки
@teacher_labeler.private_message(text = "Начать рассылку")
@teacher_labeler.private_message(payload={"cmd": "menu"})
async def start_sending(message: Message):
    if await bot.state_dispenser.get(message.peer_id) is not None:
        await bot.state_dispenser.delete(message.peer_id)
    keyboard = Keyboard()
    keyboard.add(Text("Общая рассылка", {"cmd": "all_sending"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Рассылка по группам", {"cmd": "group_sending"}))
    keyboard.row()
    keyboard.add(Text("Рассылка по курсам", {"cmd": "kurs_sending"}))
    keyboard.add(Text("Рассылка по направлению", {"cmd": "route_sending"}))

    await message.answer("Выберите тип рассылки", keyboard=keyboard)


@teacher_labeler.private_message(payload={"cmd": "group_sending"})
async def group_sending(message: Message):
    keyboard = keyb_group()
    keyboard.row()
    keyboard.add(Text("Ещё"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Ввести текст", {"cmd": "sending"}), color=KeyboardButtonColor.POSITIVE)
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
    keyboard.add(Text("Ввести текст", {"cmd": "sending"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    # Рализовать бесконечный выбор и отмена выбора курсов.
    await message.answer("Выберите курсы:", keyboard=keyboard)


@teacher_labeler.private_message(payload={"cmd": "route_sending"})
async def route_sending(message: Message):
    pass


@teacher_labeler.private_message(payload={"cmd": "all_sending"})
async def all_sending(message: Message):
    await bot.state_dispenser.set(message.peer_id, send.WRITE)
    # await bot.api.messages.send(chat_id=1, random_id=0, message="Это пишет бот текст во все группы")
    keyboard = Keyboard()
    keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer("Введите сообщение:", keyboard=keyboard)


@teacher_labeler.private_message(payload={"cmd": "sending"})
async def pre_sending(message: Message):
    await bot.state_dispenser.set(message.peer_id, send.WRITE)
    # await bot.api.messages.send(chat_id=1, random_id=0, message="Это пишет бот текст в группу")
    keyboard = Keyboard()
    keyboard.add(Text("Отмена", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer("Введите сообщение:", keyboard=keyboard)

@teacher_labeler.private_message(state=send.WRITE)
async def sending(message: Message):

    await bot.api.messages.send(chat_id=1, random_id=0, message=message.get_doc_attachments())
    await bot.api.messages.send(chat_id=1, random_id=0, message=message.text)
    await bot.api.messages.send(chat_id=1, random_id=0, attachment=message.attachments)

    await bot.state_dispenser.delete(message.peer_id)
    await message.answer("Отправлено.")


# {'group_id': 226187583, 'type': 'message_new', 'event_id': 'f702b2dc72331f3b8cafffa1b487655098ac1e41', 'v': '5.130', 'object': 
# {'message': 
# {'date': 1719338930, 
# 'from_id': 239072798, 
# 'id': 516, 
# 'out': 0, 
# 'version': 10001306, 
# 'attachments': [{
#     'type': 'doc', 'doc': {
#         'id': 677432111, 'owner_id': 239072798, 'title': 'Dockerfile.txt', 
#         'size': 169, 'ext': 'txt', 'date': 1719338928, 'type': 1, 
#         'url': 'https://vk.com/doc239072798_677432111?hash=PqCx0fr3nEU8Vid1x43qyOgVWy3DOa0Hu8qxbv3ITkg&dl=Um8nABE0mEyJixfJO1TGqGmHpoZy9drhN8J5PSkqrBH&api=1&no_preview=1', 
#         'is_unsafe': 0, 'access_key': 'Qt0OWW0NCrhEAO2zmVUbSilThiwebYZDHzDSFM9RhIs', 'can_manage': True}}],
# 
# attachment=message.attachments
# audio=None 
# audio_message=None 
# call=None 
# doc=DocsDoc(access_key='spPeBlNk2V8DKNYf9SeZiEZWNZHCB2SPEZZWSJabXB0', 
#             date=1719341824, ext='txt', id=677433743, is_licensed=None, 
#             owner_id=239072798, preview=None, size=169, tags=None, 
#             title='Dockerfile.txt', type=1, 
#             url='https://vk.com/doc239072798_677433743?hash=cCOOm3IgI7xwGohmsGQAjKG3FnGHkyKRWZRcZD8XtbP&dl=Y9jNmizN7cTP1eXfXRaHIxScJBqzV5yOJR8ZDJqcsNg&api=1&no_preview=1') 
# gift=None 
# graffiti=None 
# market=None 
# market_market_album=None 
# photo=None 
# poll=None 
# sticker=None 
# story=None 
# type=<MessagesMessageAttachmentType.DOC: 'doc'> 
# video=None 
# 
# get_doc_attachments
# [DocsDoc(
#     access_key='hTxVeCIasoeNgZPZJrM8z3TYPnksrZxGQDmz3Z8sOn0', 
#     date=1719342946, ext='txt', id=677434402, is_licensed=None, 
#     owner_id=239072798, preview=None, size=169, tags=None, 
#     title='Dockerfile.txt', type=1, 
#     url='https://vk.com/doc239072798_677434402?hash=WhOWmmRr6NAXu7V0Q96rjQMamXqNncSeZMPN908zsNo&dl=fzZYiAnFhYz2yzqOvJLHzdzWz2bEak6F3HRcNsgho5L&api=1&no_preview=1')]

# message
# action=None admin_author_id=None 
# attachments=[MessagesMessageAttachment(audio=None, audio_message=None, call=None, doc=DocsDoc(access_key='YYztfVQAAhZELyjPC8mkNHS9lpHzd2F1xhUNPbKGU7w', date=1719343080, ext='txt', id=677434470, is_licensed=None, owner_id=239072798, preview=None, size=169, tags=None, title='Dockerfile.txt', type=1, url='https://vk.com/doc239072798_677434470?hash=6zP6VWatBEjzAyAotMzgIRMNLcJPVBmeWu6bIaHus08&dl=Iba0Ck5YZwsz04UR6IkzESHjPR8SbhkBCjw53gyBu7D&api=1&no_preview=1'), gift=None, graffiti=None, market=None, market_market_album=None, photo=None, poll=None, sticker=None, story=None, type=<MessagesMessageAttachmentType.DOC: 'doc'>, video=None, wall_reply=None, group_call_in_progress=None, link=None, wall=None, mini_app=None)] 
# conversation_message_id=594 date=1719343081 deleted=None 
# from_id=239072798 fwd_messages=[] geo=None id=624 
# important=False is_cropped=None is_hidden=False is_silent=None 
# keyboard=None members_count=None out=<BaseBoolInt.no: 0> payload=None 
# peer_id=239072798 pinned_at=None random_id=0 ref=None ref_source=None reply_message=None 
# text='dadawdwa' update_time=None was_listened=None 
# unprepared_ctx_api=<API token_generator=<<class 'vkbottle.api.token_generator.single.SingleTokenGenerator'>>...> 
# state_peer=StatePeer(peer_id=239072798, state='send:0', payload={}) replace_mention=False group_id=226187583 
# client_info=ClientInfoForBots(button_actions=[<MessagesTemplateActionTypeNames.TEXT: 'text'>, <MessagesTemplateActionTypeNames.VKPAY: 'vkpay'>, <MessagesTemplateActionTypeNames.OPEN_APP: 'open_app'>, <MessagesTemplateActionTypeNames.LOCATION: 'location'>, <MessagesTemplateActionTypeNames.OPEN_LINK: 'open_link'>, <MessagesTemplateActionTypeNames.CALLBACK: 'callback'>, <MessagesTemplateActionTypeNames.INTENT_SUBSCRIBE: 'intent_subscribe'>, <MessagesTemplateActionTypeNames.INTENT_UNSUBSCRIBE: 'intent_unsubscribe'>], carousel=True, inline_keyboard=True, keyboard=True, lang_id=0)