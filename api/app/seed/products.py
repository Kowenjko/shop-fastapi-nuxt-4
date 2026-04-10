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
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Wireless%20Headphones.jpg?w=400",
        },
        {
            "name": "Smart Watch Pro",
            "description": "Advanced smartwatch with fitness tracking, heart rate monitor, and GPS. Water resistant up to 50m. Compatible with iOS and Android.",
            "price": 399.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Smart%20Watch%20Pro.jpg?w=400",
        },
        {
            "name": "Laptop Stand",
            "description": "Ergonomic aluminum laptop stand. Adjustable height and angle. Improves posture and reduces neck strain. Compatible with all laptop sizes.",
            "price": 49.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Laptop%20Stand.jpg?w=400",
        },
        {
            "name": "USB-C Hub",
            "description": "Multi-port USB-C hub with HDMI, USB 3.0, and SD card reader. Fast data transfer and 4K video output. Compact design perfect for travel.",
            "price": 79.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/USB-C_Hub.jpg?w=400",
        },
        {
            "name": "Wireless Keyboard",
            "description": "Compact wireless keyboard with mechanical switches. Long battery life and ergonomic design. Perfect for both work and gaming.",
            "price": 89.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Wireless%20Keyboard.jpg?w=400",
        },
        {
            "name": "ASUS Vivobook 15 F1504",
            "description": "The ASUS Vivobook lineup offers plenty of machines in different price categories. One of the laptops is the ASUS Vivobook 15 F1504 (X1504). This fella doesn’t cost much but it’s loaded with an adequate amount of features and performance for the class.",
            "price": 979.99,
            "category_id": categories["electronics"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/ASUS%20Vivobook%2015%20F1504.jpg?w=400",
        },
        # Clothing
        {
            "name": "Running Shoes",
            "description": "Comfortable running shoes with excellent cushioning. Breathable mesh upper and durable rubber sole. Perfect for jogging and gym workouts.",
            "price": 129.99,
            "category_id": categories["clothing"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Running%20Shoes.jpg?w=400",
        },
        {
            "name": "Under Armour",
            "description": "Comfortable running shoes with excellent cushioning. Breathable mesh upper and durable rubber sole. Perfect for jogging and gym workouts.",
            "price": 89.95,
            "category_id": categories["clothing"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Under%20Armour.jpg?w=400",
        },
        # Books
        {
            "name": "Python Programming Guide",
            "description": "Comprehensive guide to Python programming. From basics to advanced topics. Includes practical examples and exercises. Perfect for beginners and intermediate programmers.",
            "price": 45.99,
            "category_id": categories["books"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Python%20Programming%20Guide.jpg?w=400",
        },
        {
            "name": "The Art of Design",
            "description": "Inspirational book about design principles and creative thinking. Beautiful illustrations and case studies from famous designers.",
            "price": 39.99,
            "category_id": categories["books"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/The%20Art%20of%20Design.png?w=400",
        },
        {
            "name": "Cooking Masterclass",
            "description": "Professional cooking techniques and recipes. Step-by-step instructions with beautiful photography. Learn from world-class chefs.",
            "price": 49.99,
            "category_id": categories["books"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Cooking%20Masterclass.jpg?w=400",
        },
        # Home & Garden
        {
            "name": "Plant Pot Set",
            "description": "Set of 3 ceramic plant pots with drainage holes. Modern design perfect for indoor plants. Includes saucers to protect furniture.",
            "price": 34.99,
            "category_id": categories["home-garden"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Plant%20Pot%20Set.jpg?w=400",
        },
        {
            "name": "LED Desk Lamp",
            "description": "Adjustable LED desk lamp with touch control. Multiple brightness levels and color temperatures. Energy efficient and eye-friendly.",
            "price": 59.99,
            "category_id": categories["home-garden"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/LED%20Desk%20Lamp.jpg?w=400",
        },
        {
            "name": "Throw Pillow Set",
            "description": "Set of 2 decorative throw pillows. Soft and comfortable with removable covers. Perfect for sofa or bed decoration.",
            "price": 39.99,
            "category_id": categories["home-garden"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Throw%20Pillow%20Set.jpg?w=400",
        },
        {
            "name": "Garden Tool Kit",
            "description": "Complete garden tool kit with 10 essential tools. Durable stainless steel construction. Includes carrying bag for easy storage.",
            "price": 79.99,
            "category_id": categories["home-garden"].id,
            "image_url": "https://pozagofeuacsjsfslmtd.supabase.co/storage/v1/object/public/Nuxt-shop/Garden%20Tool%20Kit.jpg?w=400",
        },
    ]

    # Создаем товары
    print("📦 Creating products...")
    for data in products_data:
        product = ProductCreate(**data)
        await service.create_product(product)
    await session.commit()  # ✅ один commit в конце

    print(f"✅ Created {len(products_data)} products")
