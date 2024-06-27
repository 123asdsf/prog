
from prog.config import bot, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from prog.message import labelers
from prog.database.users import UsersRepository
from prog.database.routes import RoutesRepository
from prog.database.group import GroupsRepository
from prog.database.rules import RulesRepository
import psycopg
import asyncio

async def app():
    for labeler in labelers:
        bot.labeler.load(labeler)

    conn: psycopg.AsyncConnection = await psycopg.AsyncConnection.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)  
    
    user_repo = UsersRepository(conn)
    route_repo = RoutesRepository(conn)
    group_repo = GroupsRepository(conn)
    rule_repo = RulesRepository(conn)

    await bot.run_polling()



def main():
    asyncio.run(app())

if __name__ == "__main__":
    main()