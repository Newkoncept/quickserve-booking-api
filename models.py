from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean

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
    user_id = Column(Integer, ForeignKey("users.user_id"))
    service_id = Column(Integer, ForeignKey("services.service_id"))
    booking_date = Column(String)
    status = Column(String)


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

