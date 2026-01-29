# E-commerce API

A modern, high-performance e-commerce sales API built with FastAPI, featuring async operations, JWT authentication, and comprehensive product and order management.

## Features

- **Product Catalog**: Full CRUD operations for products with stock management
- **Order Processing**: Secure checkout with stock verification and total calculation
- **Authentication**: OAuth2 with JWT tokens and password hashing
- **User Management**: Registration and login with role-based access
- **Payment Integration**: Webhook endpoint for payment status updates
- **Auto-documentation**: Interactive API docs at `/docs`
- **Frontend Pages**: Modern HTML pages for user store and admin dashboard

## Tech Stack

- **Backend**: FastAPI with async operations
- **Database**: PostgreSQL or SQLite with SQLModel ORM
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt with passlib
- **Validation**: Pydantic
- **Frontend**: Vanilla JavaScript with Tailwind CSS

## Project Structure

```
ecommerce_api/
├── __init__.py
├── main.py          # FastAPI application and routes
├── models.py        # SQLModel database models
├── schemas.py       # Pydantic schemas for request/response
├── auth.py          # Authentication utilities
├── database.py      # Database configuration
├── requirements.txt # Python dependencies
├── user.html        # User store/checkout page
├── admin.html       # Admin dashboard page
└── README.md        # This file
```

## Installation

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables (optional):
   ```bash
   export DATABASE_URL="postgresql+asyncpg://user:password@localhost/ecommerce"
   # Or use SQLite (default): export DATABASE_URL="sqlite:///./ecommerce.db"
   ```

## Running the API

Start the development server:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Key Endpoints

### Authentication
- `POST /register` - User registration
- `POST /token` - Login and get access token

### Products (Admin only)
- `GET /products` - List all products
- `POST /products` - Create new product
- `PUT /products/{id}` - Update product

### Orders
- `POST /orders` - Create new order (checkout)
- `GET /orders` - List user's orders
- `GET /orders/{id}` - Get specific order details

### Webhooks
- `POST /webhooks/payment` - Payment status updates

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (admin/customer)
- Input validation with Pydantic
- Secure order processing with stock verification

## Example Usage

1. Register a user:
   ```bash
   curl -X POST "http://localhost:8000/register" \
        -H "Content-Type: application/json" \
        -d '{"email":"user@example.com","password":"password","full_name":"John Doe"}'
   ```

2. Login to get token:
   ```bash
   curl -X POST "http://localhost:8000/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=user@example.com&password=password"
   ```

3. Create a product (admin only):
   ```bash
   curl -X POST "http://localhost:8000/products" \
        -H "Authorization: Bearer YOUR_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"name":"Product","description":"Description","price":29.99,"stock_quantity":100}'
   ```

4. Create an order:
   ```bash
   curl -X POST "http://localhost:8000/orders" \
        -H "Authorization: Bearer YOUR_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"items":[{"product_id":1,"quantity":2}]}'
   ```

## Frontend Pages

The project includes two modern HTML pages built with Tailwind CSS and vanilla JavaScript:

### User Store Page (`user.html`)
- **Features**: Product catalog grid, shopping cart modal, order checkout, order status display
- **Design**: Dark mode, mobile-first responsive design
- **Functionality**: Add to cart, quantity management, secure checkout with stock verification
- **Integration**: Commented fetch functions ready for API integration

### Admin Dashboard (`admin.html`)
- **Features**: Sales dashboard cards, detailed sales table, inventory management
- **Design**: Professional SaaS-style dark theme, mobile-responsive tables
- **Functionality**: View sales metrics, update order status, edit products, manage stock
- **Integration**: Commented fetch functions for admin API endpoints

### How to Use Frontend Pages

1. Start the FastAPI server as described above
2. Open `user.html` in your browser for the store experience
3. Open `admin.html` in your browser for the admin dashboard
4. Update the commented fetch URLs in the JavaScript code to point to your API endpoints

## Production Considerations

- Change the SECRET_KEY in auth.py
- Use a production database (PostgreSQL recommended)
- Implement proper webhook signature verification
- Add rate limiting and CORS configuration
- Set up proper logging and monitoring
