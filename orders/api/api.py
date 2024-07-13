
"""マイクロサービスAPI

Raises:
    HTTPException: 注文IDが存在しない場合に送出する。
"""
import uuid

from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema
    )

# orders: dict = {
#     'id': '1234567890',
#     'status': 'deliverd',
#     'created': datetime.utcnow(),
#     'updated': datetime.utcnow(),
#     'order': [
#         {
#             'product': 'coca coffee',
#             'size': 'small',
#             'quantity': 1
#         }
#     ]
# }

# 注文リスト
ORDERS: list = []


@app.get('/orders', response_model=GetOrdersSchema)
def get_orders():
    """全ての注文リストの取得

    Returns:
        dict: 全ての注文リスト
    """
    return {'orders': ORDERS}


@app.post('/orders',
          status_code=status.HTTP_201_CREATED,
          response_model=GetOrderSchema)
def create_order(order_details: CreateOrderSchema) -> dict:
    """注文リストの作成

    Args:
        order_details (CreateOrderSchema): 注文商品詳細

    Returns:
        dict: 作成した注文リスト(空あり)
    """

    order = order_details.dict()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.utcnow()
    order['status'] = 'created'
    ORDERS.append(order)

    return order


@app.get('/orders/{order_id}')
def get_order(order_id: UUID):
    """注文IDを指定した注文リストの取得

    Args:
        order_id (UUID): 注文ID

    Raises:
        HTTPException: 該当する「注文ID」がない場合に送出

    Returns:
        dict: 注文IDに対応した注文リスト
    """

    for order in ORDERS:
        if order['id'] == order_id:
            return order

    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    """注文の更新

    Args:
        order_id (UUID): 注文ID
        order_details (CreateOrderSchema): 注文商品詳細

    Raises:
        HTTPException: 該当する「注文ID」がない場合に送出

    Returns:
        dict: 更新済みレスポンス
    """

    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order

    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.delete('/orders/{order_id}',
            status_code=status.HTTP_201_CREATED,
            response_class=Response)
def delete_order(order_id: UUID):
    """注文の削除

    Args:
        order_id (UUID): 注文ID

    Raises:
        HTTPException: 該当する「注文ID」がない場合に送出

    Returns:
        Response: 削除済みレスポンス
    """

    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            return Response(status_code=status.HTTPStatus.NO_CONTENT.value)

    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.post('/orders/{order_id}/cancel')
def cancel_order(order_id: UUID):
    """注文のキャンセル

    Args:
        order_id (UUID): 注文ID

    Raises:
        HTTPException: 該当する「注文ID」がない場合に送出

    Returns:
        dict: キャンセル済みの注文情報
    """

    for order in ORDERS:
        if order['id'] == order_id:
            return order

    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.post('/orders/{order_id}/pay')
def pay_order(order_id: UUID):
    """注文の支払い

    Args:
        order_id (UUID): 注文ID

    Raises:
        HTTPException: 該当する「注文ID」がない場合に送出

    Returns:
        _type_: 支払い済みの注文情報
    """

    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order

    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


def test():
    pass
