import asyncio
import sqlalchemy as sa
from databases import Database

metadata = sa.MetaData()
tbl = sa.Table(
    'tbl', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('val', sa.String(255)),
)

async def create_table(conn):
    await conn.execute('DROP TABLE IF EXISTS tbl')
    await conn.execute('''CREATE TABLE tbl (id serial PRIMARY KEY, val varchar(255))''')

async def main():
    database = Database(
        'postgresql://postgres:helloworld@127.0.0.1:15432/testing'
    )
    await database.connect()
    async with database.connection() as conn:
        async with conn.transaction():
            await create_table(conn)
    async with database.connection() as conn:
        async with conn.transaction():
            await conn.execute(query=tbl.insert(), values={'val': 'abc'})
            for row in await conn.fetch_all(query=tbl.select()):
                print(row['id'], row['val'])
    await database.disconnect()

asyncio.run(main())