import asyncio
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

metadata = sa.MetaData()
tbl = sa.Table(
    'tbl', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('val', sa.String(255)),
)

async def create_table(conn):
    await conn.run_sync(metadata.drop_all)
    await conn.run_sync(metadata.create_all)

async def main():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:helloworld@127.0.0.1:15432/testing"
    )
    async with engine.begin() as conn:
        await create_table(conn)
    async with engine.begin() as conn:
        await conn.execute(sa.insert(tbl).values(val='abc'))
        result = await conn.stream(sa.select(tbl))
        async for row in result:
            print(row.id, row.val)
    await engine.dispose()

asyncio.run(main())
