class Service:
    service_id: int
    name: str
    description: str
    price: float
    category: str
    is_available: bool

    def __init__(self, service_id, name, description, price, category, is_available):
        self.service_id = service_id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.is_available = is_available



class Booking:
    booking_id: int
    customer_id: int
    service_id: int
    booking_date: str 
    status: str

    def __init__(self, booking_id, customer_id, service_id, booking_date, status):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.service_id = service_id
        self.booking_date = booking_date
        self.status = status



class Customer:
    customer_id: int
    name: str
    email: str

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email