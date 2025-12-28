from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order
from app.enums import OrderStatus

from app.repositories.order_repository import OrderRepository
from app.models.order_product_association import OrderProductAssociation
from app.repositories.product_repository import ProductRepository
from app.schemas.order import (
    OrderResponse,
    OrderUserResponse,
    OrderCreate,
    OrderProductUpdate,
    OrderItem,
    OrderProductsAdd,
    OrderProductsReplace,
)


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repository = OrderRepository(session)
        self.product_repository = ProductRepository(session)

    """Создать новый заказ пользователя."""

    async def create_order(self, user_id: int, data: OrderCreate) -> OrderResponse:
        order = await self.order_repository.create(user_id, promocode=data.promocode)
        await self.session.commit()
        order = await self.order_repository.get_by_id(
            order.id, load_products=True, for_update=False
        )
        return self._to_order_response(order)

    """Получить заказ по ID."""

    async def get_order_by_id(self, order_id: int) -> OrderResponse:
        order = await self.order_repository.get_by_id(
            order_id, load_products=True, for_update=False
        )

        self._not_order(order)
        return self._to_order_response(order)

    """Получить список заказов пользователя."""

    async def get_user_orders(self, user_id: int) -> list[OrderUserResponse]:
        orders = await self.order_repository.get_by_user(user_id)

        return [
            OrderUserResponse(
                id=order.id,
                status=order.status,
                items=self._to_order_items(order),
                total_items=order.total_items,
                total_price=order.total_price,
            )
            for order in orders
        ]

    """Добавить продукт в заказ или увеличить его количество."""

    async def add_product_to_order(
        self,
        order_id: int,
        product_id: int,
        count: int = 1,
    ) -> OrderResponse:

        order = await self.order_repository.get_by_id(
            order_id,
            load_products=True,
            for_update=True,
        )

        self._not_order(order)
        self._ensure_draft(order)

        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        for assoc in order.products_details:
            if assoc.product_id == product_id:
                assoc.count += count
                break
        else:
            order.products_details.append(
                OrderProductAssociation(
                    product_id=product.id,
                    count=count,
                    unit_price=int(product.price),
                )
            )

        await self.session.commit()

        return self._to_order_response(order)

    """Добавить несколько продуктов в заказ."""

    async def add_products_to_order(
        self,
        data: OrderProductsAdd,
    ) -> OrderResponse:

        order = await self.order_repository.get_by_id(
            data.order_id,
            load_products=True,
            for_update=True,
        )

        self._not_order(order)
        self._ensure_draft(order)

        product_ids = [p.product_id for p in data.products]
        products = await self.product_repository.get_multiple_by_ids(product_ids)
        products_map = {p.id: p for p in products}

        missing = set(product_ids) - products_map.keys()
        if missing:
            raise HTTPException(
                status_code=404,
                detail=f"Products not found: {list(missing)}",
            )

        associations = {a.product_id: a for a in order.products_details}

        for item in data.products:
            if item.product_id in associations:
                associations[item.product_id].count += item.count
            else:
                order.products_details.append(
                    OrderProductAssociation(
                        product_id=item.product_id,
                        count=item.count,
                        unit_price=int(products_map[item.product_id].price),
                    )
                )

        await self.session.commit()

        return self._to_order_response(order)

    """Обновить количество продукта в заказе."""

    async def update_product_count(
        self,
        order_id: int,
        product_id: int,
        data: OrderProductUpdate,
    ) -> OrderResponse:
        order = await self.order_repository.get_by_id(
            order_id, load_products=True, for_update=False
        )

        self._not_order(order)
        self._ensure_draft(order)

        if data.count < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Count must be >= 0",
            )

        if data.count == 0:
            await self.order_repository.remove_product(order_id, product_id)
        else:
            await self.order_repository.update_product_count(
                order_id,
                product_id,
                data.count,
            )

        await self.session.commit()

        return self._to_order_response(order)

    """Полностью заменить список продуктов в заказе."""

    async def replace_products_in_order(
        self,
        data: OrderProductsReplace,
    ) -> OrderResponse:

        order = await self.order_repository.get_by_id(
            data.order_id,
            load_products=True,
            for_update=True,
        )

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        self._ensure_draft(order)

        product_ids = [p.product_id for p in data.products]
        products = await self.product_repository.get_multiple_by_ids(product_ids)
        products_map = {p.id: p for p in products}

        missing = set(product_ids) - products_map.keys()
        if missing:
            raise HTTPException(
                status_code=404,
                detail=f"Products not found: {list(missing)}",
            )

        order.products_details.clear()

        order.products_details.extend(
            OrderProductAssociation(
                product_id=item.product_id,
                count=item.count,
                unit_price=int(products_map[item.product_id].price),
            )
            for item in data.products
        )

        await self.session.commit()

        return self._to_order_response(order)

    """Удалить продукт из заказа."""

    async def remove_product_from_order(
        self,
        order_id: int,
        product_id: int,
    ) -> OrderResponse:

        order = await self.order_repository.get_by_id(
            order_id,
            load_products=True,
        )

        self._not_order(order)
        self._ensure_draft(order)

        await self.order_repository.remove_product(order, product_id)
        await self.session.commit()
        return self._to_order_response(order)

    """Отменить заказ пользователя."""

    async def cancel_order(self, user_id: int, order_id: int) -> OrderResponse:
        order = await self.order_repository.get_by_id(
            order_id,
            load_products=True,
        )

        self._not_order(order)
        self._not_access(order, user_id)
        self._ensure_draft(order)

        if order.status != OrderStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only draft orders can be canceled",
            )

        order.status = OrderStatus.CANCELED

        await self.session.commit()
        return self._to_order_response(order)

    """Оплатить (оформить) заказ."""

    async def checkout_order(self, user_id: int, order_id: int) -> OrderResponse:
        order = await self.order_repository.get_by_id(
            order_id,
            load_products=True,
        )

        self._not_order(order)
        self._not_access(order, user_id)
        self._ensure_draft(order)

        if not order.products_details:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot checkout an empty order",
            )

        # Меняем статус на PAID
        order.status = OrderStatus.PAID

        await self.session.commit()
        return self._to_order_response(order)

    """Проверка, что заказ существует."""

    def _not_order(self, order: Order):
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

    """Проверка прав доступа пользователя к заказу."""

    def _not_access(self, order: Order, user_id: int):
        if order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access to order",
            )

    """Проверка, что заказ находится в статусе DRAFT."""

    def _ensure_draft(self, order: Order):
        if order.status != OrderStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Order in status '{order.status}' cannot be modified",
            )

    """Преобразовать продукты заказа в список OrderItem."""

    def _to_order_items(self, order: Order) -> list[OrderItem]:
        items = [
            OrderItem.model_validate(
                {
                    "product_id": item.product.id,
                    "name": item.product.name,
                    "unit_price": item.unit_price,
                    "count": item.count,
                    "total": item.unit_price * item.count,
                }
            )
            for item in order.products_details
            if item.product is not None
        ]
        return items

    """Преобразовать заказ в OrderResponse."""

    def _to_order_response(self, order: Order) -> OrderResponse:

        return OrderResponse.model_validate(
            {
                "id": order.id,
                "promocode": order.promocode,
                "status": order.status,  # добавлено
                "created_at": order.created_at,  # добавлено
                "total_items": order.total_items,
                "total_price": order.total_price,
                "items": self._to_order_items(order),
            }
        )
