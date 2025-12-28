from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order
from app.models.product import Product
from app.models.order_product_association import OrderProductAssociation
from app.enums import OrderStatus


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    """Создать новый заказ для пользователя с опциональным промокодом."""

    async def create(self, user_id: int, promocode: str | None = None):
        order = Order(
            user_id=user_id, promocode=promocode, status=OrderStatus.DRAFT.value
        )
        self.session.add(order)
        await self.session.flush()
        return order

    """Получить заказ по ID, с возможностью подгрузки продуктов и блокировки."""

    async def get_by_id(
        self,
        order_id: int,
        *,
        load_products: bool = False,
        for_update: bool = False,
    ) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)

        if load_products:
            stmt = stmt.options(
                selectinload(Order.products_details).selectinload(
                    OrderProductAssociation.product
                )
            )

        if for_update:
            stmt = stmt.with_for_update()

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    """Получить все заказы пользователя, отсортированные по дате создания."""

    async def get_by_user(self, user_id: int) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .options(
                selectinload(Order.products_details).selectinload(
                    OrderProductAssociation.product
                )
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    """Получить все заказы, отсортированные по дате создания."""

    async def get_all(self) -> list[Order]:
        stmt = (
            select(Order)
            .order_by(Order.created_at.desc())
            .options(
                selectinload(Order.products_details).selectinload(
                    OrderProductAssociation.product
                )
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    """Удалить заказ из базы данных."""

    async def delete(self, order: Order) -> None:
        await self.session.delete(order)

    """Добавить продукт к заказу с указанным количеством."""

    async def add_product(
        self,
        order: Order,
        product: Product,
        count: int = 1,
    ) -> OrderProductAssociation:
        association = OrderProductAssociation(
            order_id=order.id,
            product_id=product.id,
            count=count,
            unit_price=int(product.price),
        )
        self.session.add(association)
        await self.session.flush()
        return association

    """Добавить несколько продуктов к заказу."""

    async def add_products(
        self,
        order: Order,
        products: list[tuple[Product, int]],
    ) -> list[OrderProductAssociation]:

        associations: list[OrderProductAssociation] = []

        for product, count in products:
            assoc = OrderProductAssociation(
                order_id=order.id,
                product_id=product.id,
                count=count,
                unit_price=int(product.price),
            )
            associations.append(assoc)

        self.session.add_all(associations)
        await self.session.flush()

        return associations

    """Получить ассоциацию продукта с заказом по ID заказа и продукта."""

    async def get_product(
        self,
        order_id: int,
        product_id: int,
    ) -> OrderProductAssociation | None:
        stmt = select(OrderProductAssociation).where(
            OrderProductAssociation.order_id == order_id,
            OrderProductAssociation.product_id == product_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    """Обновить количество продукта в заказе."""

    async def update_product_count(
        self,
        order_id: int,
        product_id: int,
        count: int,
    ) -> None:
        association = await self.get_product(order_id, product_id)
        if association:
            association.count = count
            await self.session.flush()

    """Удалить продукт из заказа."""

    async def remove_product(
        self,
        order: Order,
        product_id: int,
    ) -> None:
        order.products_details = [
            assoc for assoc in order.products_details if assoc.product_id != product_id
        ]
