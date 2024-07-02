
import redis.asyncio
from prog.config import bot, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from prog.message import labelers
from prog.database.users import UsersRepository
from prog.database.routes import RoutesRepository
from prog.database.group import GroupsRepository
from prog.database.rules import RulesRepository
from prog.message.admin import admins_handler
from prog.message.group import group_handler
from prog.message.private import private_handler
from prog.message.private import up_teacher_ids
import psycopg
import redis.asyncio
import asyncio


async def app():

    r = redis.asyncio.StrictRedis.from_url("redis://redis:6379/0", decode_responses=True)

    conn: psycopg.AsyncConnection = await psycopg.AsyncConnection.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)  


    user_repo = UsersRepository(conn)
    route_repo = RoutesRepository(conn)
    group_repo = GroupsRepository(conn)
    rule_repo = RulesRepository(conn)

    await admins_handler(route_repo, user_repo)
    await group_handler(group_repo)
    await private_handler(r, route_repo, group_repo)

    up_teacher_ids(await user_repo.get_ids_by_role(1))

    for labeler in labelers:
        bot.labeler.load(labeler)



    await bot.run_polling()



def main():
    asyncio.run(app())

if __name__ == "__main__":
    main()