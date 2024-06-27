from prog.database.models import Groups
from psycopg import AsyncConnection

class GroupsRepository():
    def __init__(self, conn: AsyncConnection):
        self._conn = conn

    async def create(self, peer_ids: int,
                     group_number: str,
                     route: int,
                     kurs: str):
        async with self._conn.cursor() as cursor:
            try:
                await cursor.execute("""
                    INSERT INTO Groups (peer_ids, group_number, route, kurs)
                    VALUES (%s, %s, %s, %s)
                """, (peer_ids, group_number, route, kurs))
                await self._conn.commit()
            except Exception as e:
                await self._conn.rollback()
                raise e

    async def get_group(self, group_number: str) -> Groups | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Groups
                WHERE group_number = %s
            """, (group_number))
            result = await cursor.fetchone()
            if result is None:
                return None
            return Groups(
                peer_ids=result[0],########
            )

    async def get_route(self, route: int) -> Groups | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Groups
                WHERE route = %s
            """, (route))
            result = await cursor.fetchone()
            if result is None:
                return None
            return Groups(
                peer_ids=result[0],#########
            )

    async def get_kurs(self, kurs: str) -> Groups | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Groups
                WHERE kurs = %s
            """, (kurs))
            result = await cursor.fetchone()
            if result is None:
                return None
            return Groups(
                peer_ids=result[0],###########
            )

    async def get_list(self, limit: int, offset: int = 0) -> list[Groups]:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Groups
                LIMIT %s
                OFFSET %s
            """, (limit, offset))
            result = await cursor.fetchall()
            return [Groups(
                peer_ids=row[0],##########
            ) for row in result]