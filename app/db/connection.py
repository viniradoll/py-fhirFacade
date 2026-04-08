from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from config import settings

_pool: ConnectionPool | None = None

def init_pool() -> None:
    global _pool
    _pool = ConnectionPool(
        conninfo=settings.db_url,
        min_size=2,
        max_size=10,
        kwargs={"row_factory": dict_row},
    )

def close_pool() -> None:
    if _pool:
        _pool.close()

def get_db():
    with _pool.connection() as conn:
        yield conn

class QueryRunner:
    def __init__(self, conn):
        self._conn = conn

    def fetch_one(self, query: str, params: dict) -> dict | None:
        with self._conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()

    def fetch_many(self, query: str, params: dict) -> list[dict]:
        with self._conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()