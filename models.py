from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean

class Services(Base):
    __tablename__ = "services"
    service_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category = Column(String)
    is_available = Column(Boolean, default=True)


class Bookings(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    service_id = Column(Integer)
    booking_date = Column(String)
    status = Column(String)


class Customers(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

