import pandas as pd
import json

# Путь к файлу XLSX
XLSX_FILE = "app/seed/data/ukr-populated-places.xlsx"

# Лист с населёнными пунктами
SHEET_NAME = "Populated Places"

# Путь для сохранения JSON
JSON_FILE = "app/seed/data/ukr-populated-places.json"

# Читаем нужный лист
df = pd.read_excel(XLSX_FILE, sheet_name=SHEET_NAME)

columns_to_drop = [
    "ADM3_CAPITAL",
    "ADM2_CAPITAL",
    "ADM1_CAPITAL",
    "ADM0_CAPITAL",
    "TYPE_EN",
    "ADM3_EN",
    "ADM3_PCODE",
    "ADM2_EN",
    "ADM2_PCODE",
    "ADM1_EN",
    "ADM1_PCODE",
    "ADM0_EN",
    "ADM0_PCODE",
]
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Переименовываем колонки под единый формат
df = df.rename(
    columns={
        "ADM4_PCODE": "id",
        "ADM4_UK": "name",
        "ADM4_EN": "name_en",
        "TYPE_UK": "city_type",
        "LAT": "lat",
        "LON": "lon",
        "ADM0_UK": "country",
        "ADM1_UK": "region",
        "ADM2_UK": "district",
        "ADM3_UK": "community",
    }
)

# Заполняем пустые значения None
df = df.where(pd.notnull(df), None)

# Конвертируем в список словарей
records = df.to_dict(orient="records")

# Сохраняем в JSON
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"✅ Сохранено {len(records)} записей в {JSON_FILE}")
