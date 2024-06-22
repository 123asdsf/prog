
from vkbottle import Bot
from prog.config import api, labeler
from prog.message import labelers

bot = Bot(
    api=api,
    labeler=labeler,
)

for labeler in labelers:
    bot.labeler.load(labeler)


bot.run_forever()