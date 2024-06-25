from models import Rules
from psycopg import AsyncConnection

class RulesRepository():
    def __init__(self, conn: AsyncConnection):
        self._conn = conn

    async def create(self, id_rule: int, name: str, functional: str):
        async with self._conn.cursor() as cursor:
            try:
                await cursor.execute("""
                    INSERT INTO Rules (id_rule, name, functional)
                    VALUES (%s, %s, %s)
                """, (id_rule, name, functional))
                await self._conn.commit()
            except Exception as e:
                await self._conn.rollback()
                raise e

    async def get_id(self, id_rule: int) -> Rules | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Rules
                WHERE id_rule = %s
            """, (id_rule))
            result = await cursor.fetchone()
            if result is None:
                return None
            return Rules(
                id_rule=result[0],########
            )

    async def get_name(self, name: str) -> Rules | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Rules
                WHERE name = %s
            """, (name))
            result = await cursor.fetchone()
            if result is None:
                return None
            return Rules(
                name=result[0],#########
            )


    async def get_list(self, limit: int, offset: int = 0) -> list[Rules]:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Rules
                LIMIT %s
                OFFSET %s
            """, (limit, offset))
            result = await cursor.fetchall()
            return [Rules(
                peer_ids=row[0],########
            ) for row in result]