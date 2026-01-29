from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
from database import create_db_and_tables, get_session
from models import User, Product, Order, OrderItem, OrderStatus
from schemas import (
    UserCreate, User, UserLogin, ProductCreate, Product, ProductUpdate,
    OrderCreate, Order, Token
)
from auth import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash, get_user_by_email
)

app = FastAPI(title="E-commerce API", description="A modern e-commerce sales API")

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

# Authentication routes
@app.post("/register", response_model=User)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check if user already exists
    db_user = await get_user_by_email(user.email, session)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Product routes
@app.get("/products", response_model=List[Product])
async def get_products(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Product).where(Product.is_active == True).offset(skip).limit(limit))
    products = result.scalars().all()
    return products

@app.post("/products", response_model=Product)
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_product = Product(**product.dict())
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    result = await session.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product

# Order routes
@app.post("/orders", response_model=Order)
async def create_order(
    order: OrderCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    # Check stock availability and calculate total
    total_amount = 0
    order_items = []
    
    for item in order.items:
        result = await session.execute(select(Product).where(Product.id == item.product_id))
        product = result.scalar_one_or_none()
        if not product or not product.is_active:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        unit_price = product.price
        total_price = unit_price * item.quantity
        total_amount += total_price
        
        order_items.append(OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=unit_price,
            total_price=total_price
        ))
        
        # Update stock
        product.stock_quantity -= item.quantity
        session.add(product)
    
    # Create order
    db_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        items=order_items
    )
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)
    
    return db_order

@app.get("/orders", response_model=List[Order])
async def get_user_orders(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    result = await session.execute(
        select(Order).where(Order.user_id == current_user.id)
    )
    orders = result.scalars().all()
    return orders

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    result = await session.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    return order

# Webhook for payment updates (simplified example)
@app.post("/webhooks/payment")
async def payment_webhook(payment_data: dict):
    # This is a simplified webhook handler
    # In a real application, you'd verify the webhook signature
    order_id = payment_data.get("order_id")
    status = payment_data.get("status")
    
    if status == "paid":
        # Update order status to paid
        # You'd implement this logic here
        pass
    
    return {"message": "Webhook received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
