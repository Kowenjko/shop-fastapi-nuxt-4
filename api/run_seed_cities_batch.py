# run_seed_cities_batch.py
import asyncio
from app.core.db_helper import db_helper
from app.seed.cities_seed_batch import seed_cities


async def main():
    async_session_maker = db_helper.session_factory

    async with async_session_maker() as session:
        await seed_cities(session)

    await db_helper.engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
