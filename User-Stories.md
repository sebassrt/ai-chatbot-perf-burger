# User Stories for PerfBurger AI Chatbot API

## Core Features Epic (v1.0)

**Epic Description:** As a user of the PerfBurger system, I need to manage my account and interact with the chatbot.

**Stories:**

1. **User Registration**
**Persona:** New Customer  
**Story Statement:** As a new customer, I want to register an account so I can place orders and track my purchases.  
**Acceptance Criteria:**
- User provides email, password, first name, and last name
- Registration returns a 201 status and a JWT access token
- Response contains user details matching the request
- Duplicate registration returns an error

**Mapped Endpoint:**  
`POST /users/register`  
Content-Type: application/json
Request Body:
```json
{
  "email": "test@perfburger.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

2. **User Login**
**Persona:** Returning Customer  
**Story Statement:** As a returning customer, I want to log in to access my profile and previous orders.  
**Acceptance Criteria:**
- User provides valid credentials
- Login returns a 200 status and a JWT access token
- Response contains user details and token
- Invalid credentials return a 401 error

**Mapped Endpoint:**  
`POST /users/login`  
Content-Type: application/json
Request Body:
```json
{
  "email": "test@perfburger.com",
  "password": "password123"
}
```

3. **Menu Inquiries**
**Persona:** Hungry Customer  
**Story Statement:** As a customer, I want to ask about menu items and prices.  
**Acceptance Criteria:**
- User can ask about specific menu items or dietary options
- Response includes relevant menu items and prices
- Response uses knowledge base data
- User must be authenticated

**Mapped Endpoint:**  
`POST /chat`  
Content-Type: application/json  
Authorization: Bearer token required
Request Body:
```json
{
  "message": "What vegetarian options do you have under $15?"
}
```

4. **View Orders**
**Persona:** Frequent Customer  
**Story Statement:** As a customer, I want to view all my past orders.  
**Acceptance Criteria:**
- User can retrieve all their orders
- Response includes order details and status
- Pagination is supported for large order histories
- Only authenticated users can access their orders

**Mapped Endpoint:**  
`GET /orders`  
Authorization: Bearer token required

5. **Order Tracking**
**Persona:** Active Customer  
**Story Statement:** As a customer, I want to check my order status and tracking.  
**Acceptance Criteria:**
- User can check order status by ID
- Response includes current status and details
- User can view tracking history and estimated delivery
- Only authenticated users can access their orders

**Mapped Endpoints:**  
1. Get Order Status: `GET /orders/{orderId}`  
   Authorization: Bearer token required
2. Track Order: `GET /orders/{orderId}/tracking`  
   Authorization: Bearer token required
