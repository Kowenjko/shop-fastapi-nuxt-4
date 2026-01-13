from app.schemas.product import ProductCreate

from app.services.category_service import CategoryService
from app.services.product_service import ProductService


async def all_categories(session):
    service = CategoryService(session)
    categories_list = await service.get_all_categories()

    # преобразуем в dict {slug: category}
    return {cat.slug: cat for cat in categories_list}


async def seed_products(session):
    categories = await all_categories(session)
    service = ProductService(session)

    print(categories)

    if not categories or len(categories) < 4:
        raise Exception("Categories must be seeded before products.")

    products_data = [
        # Electronics
        {
            "name": "Wireless Headphones",
            "description": "High-quality wireless headphones with noise cancellation. Perfect for music lovers and professionals. Battery life up to 30 hours.",
            "price": 299.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/484455057.png?w=400",
        },
        {
            "name": "Smart Watch Pro",
            "description": "Advanced smartwatch with fitness tracking, heart rate monitor, and GPS. Water resistant up to 50m. Compatible with iOS and Android.",
            "price": 399.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/5525077175.jpg?w=400",
        },
        {
            "name": "Laptop Stand",
            "description": "Ergonomic aluminum laptop stand. Adjustable height and angle. Improves posture and reduces neck strain. Compatible with all laptop sizes.",
            "price": 49.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/duchy-52224228.jpg?w=400",
        },
        {
            "name": "USB-C Hub",
            "description": "Multi-port USB-C hub with HDMI, USB 3.0, and SD card reader. Fast data transfer and 4K video output. Compact design perfect for travel.",
            "price": 79.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/euasoo-9-in-1-usb-c-hub_aqex.1024-673463522.jpg?w=400",
        },
        {
            "name": "Wireless Keyboard",
            "description": "Compact wireless keyboard with mechanical switches. Long battery life and ergonomic design. Perfect for both work and gaming.",
            "price": 89.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/k950-off-white-gallery1-front-view-amr-us-2181552335.png?w=400",
        },
        {
            "name": "ASUS Vivobook 15 F1504",
            "description": "The ASUS Vivobook lineup offers plenty of machines in different price categories. One of the laptops is the ASUS Vivobook 15 F1504 (X1504). This fella doesn’t cost much but it’s loaded with an adequate amount of features and performance for the class.",
            "price": 979.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/3-7-e1678204949389-1971156045.jpg?w=400",
        },
        # Clothing
        {
            "name": "Running Shoes",
            "description": "Comfortable running shoes with excellent cushioning. Breathable mesh upper and durable rubber sole. Perfect for jogging and gym workouts.",
            "price": 129.99,
            "category_id": categories["clothing"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/1544814212-765dfd69-66c6-4362-b548-815b9bbfe43e-2471997735.jpg?w=400",
        },
        {
            "name": "Under Armour",
            "description": "Comfortable running shoes with excellent cushioning. Breathable mesh upper and durable rubber sole. Perfect for jogging and gym workouts.",
            "price": 89.95,
            "category_id": categories["clothing"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/under-armour-womens-charged-bandit-trail-2-storm-running-shoe-p39223-454632_image-2265751954.jpg?w=400",
        },
        # Books
        {
            "name": "Python Programming Guide",
            "description": "Comprehensive guide to Python programming. From basics to advanced topics. Includes practical examples and exercises. Perfect for beginners and intermediate programmers.",
            "price": 45.99,
            "category_id": categories["books"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/1671641215_the-complete-python-coding-programming-manual-15th-edition-2022-3724808841.jpg?w=400",
        },
        {
            "name": "The Art of Design",
            "description": "Inspirational book about design principles and creative thinking. Beautiful illustrations and case studies from famous designers.",
            "price": 39.99,
            "category_id": categories["books"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/1_Axm3NzGOluy2dqbAUE-Gqw-719642391.png?w=400",
        },
        {
            "name": "Cooking Masterclass",
            "description": "Professional cooking techniques and recipes. Step-by-step instructions with beautiful photography. Learn from world-class chefs.",
            "price": 49.99,
            "category_id": categories["books"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/cook.png?w=400",
        },
        # Home & Garden
        {
            "name": "Plant Pot Set",
            "description": "Set of 3 ceramic plant pots with drainage holes. Modern design perfect for indoor plants. Includes saucers to protect furniture.",
            "price": 34.99,
            "category_id": categories["home-garden"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/71CK2RjATZL._AC_-2912321097.jpg?w=400",
        },
        {
            "name": "LED Desk Lamp",
            "description": "Adjustable LED desk lamp with touch control. Multiple brightness levels and color temperatures. Energy efficient and eye-friendly.",
            "price": 59.99,
            "category_id": categories["home-garden"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/61Qwy%2BPmZCL._AC_-1270594125.jpg?w=400",
        },
        {
            "name": "Throw Pillow Set",
            "description": "Set of 2 decorative throw pillows. Soft and comfortable with removable covers. Perfect for sofa or bed decoration.",
            "price": 39.99,
            "category_id": categories["home-garden"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/81zaUmHq6DL._AC_SL1500_-2454199951.jpg?w=400",
        },
        {
            "name": "Garden Tool Kit",
            "description": "Complete garden tool kit with 10 essential tools. Durable stainless steel construction. Includes carrying bag for easy storage.",
            "price": 79.99,
            "category_id": categories["home-garden"].id,
            "image_url": "https://696604719b7ee2acb492c452.imgix.net/71ppywKiiQL._AC_SL1500_-2152028338.jpg?w=400",
        },
    ]

    # Создаем товары
    print("📦 Creating products...")
    for data in products_data:
        product = ProductCreate(**data)
        await service.create_product(product)

    print(f"✅ Created {len(products_data)} products")
