from models import User
from psycopg import AsyncConnection

class UserRepository():
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
                    INSERT INTO User (peer_id, name, surname, last_name, rule)
                    VALUES (%s, %s, %s, %s, %s)
                """, (peer_id, name, surname, last_name, rule))
                await self._conn.commit()
            except Exception as e:
                await self._conn.rollback()
                raise e

    async def get(self, peer_id: int) -> User | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM User
                WHERE peer_id = %s
            """, (peer_id))
            result = await cursor.fetchone()
            if result is None:
                return None
            return User(
                peer_id=result[0],########
            )


    async def get_list(self, limit: int, offset: int = 0) -> list[User]:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM User
                LIMIT %s
                OFFSET %s
            """, (limit, offset))
            result = await cursor.fetchall()
            return [User(
                peer_id=row[0],########
            ) for row in result]