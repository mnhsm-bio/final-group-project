from . import orders, order_details, customers, payment, resource_management, promotions, reviews, sandwiches



def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(customers.router)
    app.include_router(payment.router)
    app.include_router(reviews.router)
    app.include_router(resource_management.router)
    app.include_router(sandwiches.router)
    app.include_router(promotions.router)
    app.include_router(reviews.router)
