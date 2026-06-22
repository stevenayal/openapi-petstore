from datetime import datetime, timezone
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import verify_api_key
from app.models import Order, Pet
from app.schemas import OrderSchema

router = APIRouter(tags=["store"])


def _order_to_schema(order: Order) -> OrderSchema:
    return OrderSchema(
        id=order.id,
        petId=order.pet_id,
        quantity=order.quantity,
        shipDate=order.ship_date,
        status=order.status,
        complete=order.complete,
    )


@router.get(
    "/store/inventory",
    summary="Returns pet inventories by status",
    operation_id="getInventory",
    responses={200: {"description": "successful operation"}},
)
def get_inventory(
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    pets = db.query(Pet).all()
    inventory: Dict[str, int] = {}
    for pet in pets:
        status = pet.status or "unknown"
        inventory[status] = inventory.get(status, 0) + 1
    return inventory


@router.post(
    "/store/order",
    summary="Place an order for a pet",
    operation_id="placeOrder",
    response_model=OrderSchema,
    response_model_by_alias=True,
    responses={
        200: {"description": "successful operation"},
        400: {"description": "Invalid Order"},
    },
)
def place_order(
    order_data: OrderSchema,
    db: Session = Depends(get_db),
):
    if order_data.pet_id is None:
        raise HTTPException(status_code=400, detail="petId is required")
    order = Order(
        pet_id=order_data.pet_id,
        quantity=order_data.quantity or 1,
        ship_date=order_data.ship_date or datetime.now(timezone.utc),
        status=order_data.status or "placed",
        complete=order_data.complete or False,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return _order_to_schema(order)


@router.get(
    "/store/order/{order_id}",
    summary="Find purchase order by ID",
    operation_id="getOrderById",
    response_model=OrderSchema,
    response_model_by_alias=True,
    responses={
        200: {"description": "successful operation"},
        400: {"description": "Invalid ID supplied"},
        404: {"description": "Order not found"},
    },
)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
):
    if order_id < 1 or order_id > 5:
        raise HTTPException(status_code=400, detail="Order ID must be between 1 and 5")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_to_schema(order)


@router.delete(
    "/store/order/{order_id}",
    summary="Delete purchase order by ID",
    operation_id="deleteOrder",
    responses={
        400: {"description": "Invalid ID supplied"},
        404: {"description": "Order not found"},
    },
)
def delete_order(
    order_id: str,
    db: Session = Depends(get_db),
):
    try:
        oid = int(order_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order ID")
    order = db.query(Order).filter(Order.id == oid).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
