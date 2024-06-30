from prog.database.models import Routes
from psycopg import AsyncConnection

class RoutesRepository():
    def __init__(self, conn: AsyncConnection):
        self._conn = conn

    async def create(self, name: str):
        async with self._conn.cursor() as cursor:
            try:
                await cursor.execute("""
                    INSERT INTO Routes (name)
                    VALUES (%s)
                """, (name,))
                await self._conn.commit()
            except Exception as e:
                await self._conn.rollback()
                raise e

    async def get_id(self, id_route: str) -> Routes | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Routes
                WHERE id_route = %s
            """, (id_route))
            result = await cursor.fetchone()
            if result is None:
                return None
            return Routes(
                id_route=result[0], name=result[1]
            )

    # async def get_name(self, name: str) -> Routes | None:
    #     async with self._conn.cursor() as cursor:
    #         await cursor.execute("""
    #             SELECT *
    #             FROM Routes
    #             WHERE name = %s
    #         """, (name))
    #         result = await cursor.fetchone()
    #         if result is None:
    #             return None
    #         return Routes(
    #             id_route=result[0], name=result[1]
    #         )


    async def get_list(self, limit: int, offset: int = 0) -> list[Routes]:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Routes
                LIMIT %s
                OFFSET %s
            """, (limit, offset))
            result = await cursor.fetchall()
            return [Routes(
                id_route=row[0], name=row[1]
            ) for row in result]