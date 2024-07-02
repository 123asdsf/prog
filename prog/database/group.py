from prog.database.models import Groups
from psycopg import AsyncConnection

class GroupsRepository():
    def __init__(self, conn: AsyncConnection):
        self._conn = conn

    async def create(self, peer_ids: int,
                     group_number: str,
                     route: int,
                     course: int):
        async with self._conn.cursor() as cursor:
            try:
                await cursor.execute("""
                    INSERT INTO Groups (peer_ids, group_number, route, course)
                    VALUES (%s, %s, %s, %s)
                """, (peer_ids, group_number, route, course,))
                await self._conn.commit()
            except Exception as e:
                await self._conn.rollback()
                raise e

    async def get_id(self, peer_ids: int) -> int | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT peer_ids
                FROM Groups
                WHERE peer_ids = %s
            """, (peer_ids, ))
            result = await cursor.fetchone()
            if result is None:
                return None
            return result
        
    async def get_all_id(self) -> list[int] | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT peer_ids
                FROM Groups
            """)
            result = await cursor.fetchall()
            if result is None:
                return None
            peer_ids = [row[0] for row in result]
            return peer_ids

    async def get_peer_id_by_group(self, group_number: str) -> int:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT peer_ids
                FROM Groups
                WHERE group_number = %s
            """, (group_number, ))
            result = await cursor.fetchone()
            if result is None:
                return -1
            return result[0]

    async def get_id_by_route(self, route: int) -> list[int] | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT peer_ids
                FROM Groups
                WHERE route = %s
            """, (route,))
            result = await cursor.fetchall()
            if result is None:
                return None
            peer_ids = [row[0] for row in result]
            return peer_ids

    async def get_id_by_course(self, course: list[int]) -> list[int] | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT peer_ids
                FROM Groups
                WHERE course in (%s, %s, %s, %s)
            """, (course[0], course[1], course[2], course[3]))
            result = await cursor.fetchall()
            if result is None:
                return None
            peer_ids = [row[0] for row in result]
            return peer_ids

    async def get_list(self, limit: int, offset: int = 0) -> list[Groups] | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute("""
                SELECT *
                FROM Groups
                LIMIT %s
                OFFSET %s
            """, (limit, offset))
            result = await cursor.fetchall()
            return [Groups(
                peer_ids=row[0], 
                group_number=row[1], 
                route=row[2], 
                course=row[3]
            ) for row in result]