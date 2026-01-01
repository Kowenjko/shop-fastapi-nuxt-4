import json
from app.schemas.city import CityCreate
from app.services.city_service import CityService

JSON_FILE = "app/seed/data/ukr-populated-places.json"
BATCH_SIZE = 500  # можно увеличить при необходимости


async def seed_cities(session):
    service = CityService(session)

    with open(JSON_FILE, encoding="utf-8") as f:
        data = json.load(f)

    def normalize(item: dict) -> dict | None:
        # id обязателен
        if not item.get("id"):
            return None

        for key, value in item.items():
            # NaN → None
            if value != value:
                item[key] = None

        return item

    cities = []

    skipped = 0
    for item in data:
        normalized = normalize(item)
        if not normalized:
            skipped += 1
            continue
        # if skipped < 5:
        #     print("Skipped example:", item)
        cities.append(CityCreate(**normalized))
    if skipped < 5:
        print("Skipped example:", item)

    print(f"🏙️ Seeding {len(cities)} cities in batches of {BATCH_SIZE}...")
    await service.seed_cities_batch(cities, batch_size=BATCH_SIZE)
    print("🎉 All cities seeded successfully!")
