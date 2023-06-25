# Household Plants Descriptor and Buyer

This application allows users to browse through a collection of household plants and select their preferred ones for purchase. It utilizes an API to fetch and display the plants' descriptions, prices, and images. 

To enhance user experience, the application also provides a way for users to create an account, store their personal details, and keep track of their purchases history.

The application is built using Python and Flask framework, and utilizes IBMcloudDB as its database management system. 

To ensure scalability and efficient deployment, the application is containerized using Docker and deployed using Kubernetes.

## API Endpoints

The following are the API endpoints used in the application:

1. `/api/plants` - Returns a list of all the plants in the collection.
2. `/api/plants/{id}` - Returns details of a specific plant in the collection.
3. `/api/users` - Returns a list of all the registered users.
4. `/api/users/{id}` - Returns details of a specific user.
5. `/api/orders` - Returns a list of all orders placed by users.
6. `/api/orders/{id}` - Returns details of a specific order.

## Technologies Used

- Python
- Flask
- IBMcloudDB
- Docker
- Kubernetes
