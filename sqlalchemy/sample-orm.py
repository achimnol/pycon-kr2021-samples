import asyncio
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class A(Base):
    __tablename__ = "a"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    val = Column(String(255))
    created_at = Column(sa.DateTime, server_default=sa.func.now())

async def create_table(conn):
    await conn.run_sync(Base.metadata.drop_all)
    await conn.run_sync(Base.metadata.create_all)

async def main():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:helloworld@127.0.0.1:15432/testing",
    )
    async with engine.begin() as conn:
        await create_table(conn)
    async_session = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [A(val="abc"), A(val="def")]
            )
            await session.commit()
    async with async_session() as session:
        result = await session.execute(sa.select(A))
        for a in result.scalars():
            print(a.id, a.val, a.created_at)
    await engine.dispose()

asyncio.run(main())