# Technical Design: Trio Coffee Shop Challenge

Author: Everton de Castro  
Email: evertoncastro.sp@gmail.com

## Objective:
The objective is to design a REST API system that allows managers to customize products and order statuses, while customers can order products from a catalog. The system should support various operations such as viewing the menu, placing new orders, viewing order details, and updating/canceling orders with a "waiting" status. Additionally, email notifications should be sent to customers when the order status changes.

## Overview:
The system will consist of a REST API that provides endpoints for different functionalities. Managers will have the ability to customize products and change order statuses, while customers can order products and customize the order. The system will handle order processing, including sending email notifications to customers when the order status changes.

## Endpoints:

#### Customer:
GET coffeeshop/api/menu  
Description: Retrieves the list of products from the catalog with their variations.

POST coffeeshop/api/orders  
Description: Place a new order with the specified details.

GET coffeeshop/api/orders/{order_id}  
Description: Retrieves the details of a specific order.

PUT coffeeshop/api/orders/{order_id}  
Description: Updates the details of an order with a "Waiting" status. Change location between “In house” and “Take away”. Cancel the order.

POST coffeeshop/api/orders/{order_id}/orde-item/  
Description: Add a new product item to the order

PUT coffeeshop/api/orders/{order_id}/orde-item/{order_item_id}  
Description: Update a product item of a specific order

DELETE coffeeshop/api/orders/{order_id}/orde-item/{order_item_id}  
Description: Remove a product item from a specific order

#### Admin:
POST coffeeshop/api/admin/products  
Description: Create a new product with its variations in the menu.

PUT coffeeshop/api/admin/products/{product_id}  
Description: Update the product properties and add new variations.

PUT coffeeshop/api/admin/products/{product_id}/variations/{variation_id}  
Description: Update a specific variation.

DELETE coffeeshop/api/admin/products/{product_id}/variations/{variation_id}  
Description: Delete a specific variation.


## Workflow:
- Managers customize products and order statuses through admin/ endpoints that can be connected to an administrative interface.
- Customers authenticate themselves and interact with the system through a JSON web token.
- Customers view the menu to see the available products and variations.
- Customers place a new order by specifying the products, variations, quantities, and consumption location.
- The system generates an order ID and sends a confirmation to the customer.
- Managers can change the order status, which triggers an email notification to the customer.
- Customers can view the details of their orders, including the product list, pricing, and order status.
- Customers can update or cancel their orders with a "Waiting" status.
- Email notifications are sent to customers when the order status changes.


## Technologies:
- Programming Language: Python
- Framework: Django
- Database: SQLite
- Authentication: JWT (JSON Web Tokens)
- Email Notification Service: MailHog
- API Documentation: Swagger


## Analysis:

### Why use Django

- Rapid Development: Django follows the principle of "don't repeat yourself" (DRY) and provides a lot of built-in functionalities, which speed up the development process. It includes features like automatic admin interface generation, form handling, and database ORM (Object-Relational Mapping), which greatly simplifies common tasks.

- Scalability and Maintainability: Django follows a clean and modular design pattern, which makes it highly scalable and maintainable. It encourages the separation of concerns, such as models for data handling, views for business logic, and templates for presentation. This promotes code reusability, making it easier to maintain and extend the application as it grows.

- Authentication and Security: Django provides a robust authentication system out-of-the-box, including user management, password hashing, and session handling. Additionally, Django supports integration with JWT for implementing token-based authentication.

- ORM and Database Support: Django's ORM simplifies database interactions by abstracting the underlying database implementation. It supports multiple databases, including PostgreSQL and MySQL, allowing flexibility in choosing the most suitable database for the project. The ORM handles tasks like query generation, data validation, and migration management, reducing the complexity of database operations.
