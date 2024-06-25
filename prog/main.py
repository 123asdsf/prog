
from prog.config import labeler, bot, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from prog.message import labelers
import psycopg
import asyncio

async def app():
    for labeler in labelers:
        bot.labeler.load(labeler)

    conn: psycopg.AsyncConnection = await psycopg.AsyncConnection.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)  

    await bot.run_polling()



def main():
    asyncio.run(app())

if __name__ == "__main__":
    main()