"""検証モデル

pydanticを使用した検証モデルの実装モジュール

検証モデルを実装したスキーマオブジェクトは、
ペイロードのデータ型を定義すると同時に、
データ検証の機能が作り込まれたものとなる。
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, conint, validator, conlist


class Size(Enum):
    small = "small"
    medium = "medium"
    big = "big"


class StatusEnum(Enum):
    created = "created"
    paid = "paid"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"


class OrderItemSchema(BaseModel):
    """注文商品スキーマ

    Args:
        BaseModel (_type_): _description_

    Mmeber:
        product: 商品名
        size: 大きさ
        quantity: 個数（オプション）
    """
    product: str
    size: Size
    quantity: Optional[conint(ge=1, strict=True)] = 1

    @validator("quantity")
    def quantity_non_nullable(cls, value):
        """_summary_

        Args:
            value (_type_): _description_

        Returns:
            _type_: _description_
        """
        assert value is not None, "quantity may not be None"
        return value


class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_length=1)


class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: StatusEnum


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]
