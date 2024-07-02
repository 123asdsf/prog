from prog.database.models import Users
from psycopg import AsyncConnection

class UsersRepository():
    def __init__(self, conn: AsyncConnection):
        self._conn = conn

    async def create(self,  peer_id: int,
                            name: str,
                            surname: str,
                            last_name: str,
                            rule: int):
        async with self._conn.cursor() as cursor:
            try:
                await cursor.execute("""
                    INSERT INTO Users (peer_id, name, surname, last_name, rule)
                    VALUES (%s, %s, %s, %s, %s)
                """, (peer_id, name, surname, last_name, rule))
                await self._conn.commit()
            except Exception as e:
                await self._conn.rollback()
                raise e

    async def get_ids_by_role(self, rule: int) -> list[int]:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT peer_id
                FROM Users
                WHERE rule = %s
            """, (rule,))
            result = await cursor.fetchall()
            if result is None:
                return []
            peer_ids = [row[0] for row in result]
            return peer_ids


    async def get_list(self, limit: int, offset: int = 0) -> list[Users]:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Users
                LIMIT %s
                OFFSET %s
            """, (limit, offset))
            result = await cursor.fetchall()
            return [Users(
                peer_id=row[0], name=row[1], surname=row[2], last_name=row[3], rule=row[4]
            ) for row in result]