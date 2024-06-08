import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN

vk_session = vk_api.VkApi(token=TOKEN) #для людей поместивших токен в config
vk_api.VkApi(token='Ваш токен') #Для остальных
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
