# User Stories for PerfBurger AI Chatbot API

[## 6. View All Orders]

**Persona:** Frequent Customer  
**Story Statement:** As a frequent customer, I want to view a list of all my past orders so I can review my purchase history.  

## 1. User Registration
- User requests all orders.
- Response contains an array of orders with details.
- Pagination info is included if there are many orders.
- Only authenticated users can access their orders.

**Mapped Endpoint:**  
`GET /orders`

<<<<<<< HEAD
----
=======
---
>>>>>>> 836622ebb56fa3d9be57a694cdd748f3d72aa05a

[## 7. View Chat Sessions]

**Persona:** Returning User  
**Story Statement:** As a user, I want to view all my previous chat sessions so I can continue conversations or review information provided by the chatbot.  

**Persona:** New Customer  
- User requests chat sessions.
- Response contains an array of sessions with details.
- Only authenticated users can access their sessions.

**Mapped Endpoint:**  
`GET /chat/sessions`

<<<<<<< HEAD
----
=======
---
>>>>>>> 836622ebb56fa3d9be57a694cdd748f3d72aa05a
**Story Statement:** As a new customer, I want to register an account so I can place orders and track my purchases.  
**Benefit:** Enables personalized service and order history tracking.  
**Acceptance Criteria:**
- User provides email, password, first name, and last name.
- Registration returns a 201 status and a JWT access token.
- Response contains user details matching the request.
- Duplicate registration returns an error.

**Mapped Endpoint:**  
`POST /users/register`

<<<<<<< HEAD
----
=======
---
>>>>>>> 836622ebb56fa3d9be57a694cdd748f3d72aa05a

## 2. User Login

**Persona:** Returning Customer  
**Story Statement:** As a returning customer, I want to log in so I can access my profile and previous orders.  
**Benefit:** Secure access to personal data and order management.  
**Acceptance Criteria:**
- User provides valid credentials.
- Login returns a 200 status and a JWT access token.
- Response contains user details and token.
- Invalid credentials return a 401 error.

**Mapped Endpoint:**  
`POST /users/login`

<<<<<<< HEAD
----
=======
---
>>>>>>> 836622ebb56fa3d9be57a694cdd748f3d72aa05a

## 3. Chatbot Menu Inquiry

**Persona:** Hungry Visitor  
**Story Statement:** As a visitor, I want to ask the chatbot about vegetarian options under $15 so I can decide what to order.  
**Benefit:** Quick, conversational access to menu information.  
**Acceptance Criteria:**
- User sends a chat message about menu options.
- Response includes relevant menu items and prices.
- Response uses knowledge base data.
- Response time is under 5 seconds.

**Mapped Endpoint:**  
`POST /chat`

<<<<<<< HEAD
----
=======
---
>>>>>>> 836622ebb56fa3d9be57a694cdd748f3d72aa05a

## 4. Order Status Tracking

**Persona:** Active Customer  
**Story Statement:** As a customer, I want to check the status and tracking of my order so I know when it will arrive.  
**Benefit:** Reduces uncertainty and improves customer satisfaction.  
**Acceptance Criteria:**
- User requests order status by ID.
- Response includes order details and current status.
- User can view tracking history and estimated delivery.
- Only authenticated users can access their orders.

**Mapped Endpoints:**  
`GET /orders/{orderId}`  
`GET /orders/{orderId}/tracking`

<<<<<<< HEAD
----
=======
---
>>>>>>> 836622ebb56fa3d9be57a694cdd748f3d72aa05a

## 5. Report Order Issue

**Persona:** Disappointed Customer  
**Story Statement:** As a customer, I want to report an issue with my order so it can be resolved quickly.  
**Benefit:** Ensures problems are addressed and improves service recovery.  
**Acceptance Criteria:**
- User submits issue type and description for an order.
- Response returns a 201 status and issue details.
- Issue status is set to "reported".
- Only authenticated users can report issues.

**Mapped Endpoint:**  
`POST /orders/{orderId}/issues`


