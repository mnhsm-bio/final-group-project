from . import orders, order_details, customers, payment, resource_management
from . import orders, order_details, customers, payment, reviews



def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(customers.router)
    app.include_router(payment.router)
    app.include_router(reviews.router)

    app.include_router(resource_management.router)