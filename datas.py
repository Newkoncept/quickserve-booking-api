from models import Service, Customer, Booking


services = [
    Service(1, "Backend API Development", "Build secure REST APIs using FastAPI, Python, and clean backend architecture.", 250.0, "development", True),
    Service(2, "Frontend Website Development", "Create responsive websites using modern frontend tools and clean UI design.", 300.0, "development", True),
    Service(3, "API Bug Fixing", "Debug and fix broken API endpoints, validation errors, and server-side issues.", 80.0, "development", False),
    Service(4, "Railway Deployment Setup", "Deploy backend applications to Railway using GitHub integration and environment variables.", 100.0, "deployment", True),
    Service(5, "Postman API Testing", "Test API endpoints with Postman and create organized collections for documentation.", 70.0, "testing", True),
    Service(6, "Database Integration", "Connect backend applications to PostgreSQL or MySQL databases with proper models.", 180.0, "database", True),
    Service(7, "Authentication System", "Add user registration, login, password hashing, and JWT authentication to backend apps.", 220.0, "security", True),
    Service(8, "Payment Gateway Integration", "Integrate payment flows such as Paystack transaction initialization and verification.", 200.0, "payment", False),
    Service(9, "Webhook Endpoint Setup", "Create webhook endpoints for receiving and processing third-party service events.", 150.0, "integration", True),
    Service(10, "API Documentation", "Write clear API documentation with endpoint descriptions, request examples, and response formats.", 60.0, "documentation", True),
]

bookings = [
    Booking(1, 1, 1, "2026-05-20", "pending"),
    Booking(2, 1, 4, "2026-05-21", "confirmed"),
    Booking(3, 1, 7, "2026-05-22", "completed"),

    Booking(4, 2, 3, "2026-05-23", "pending"),
    Booking(5, 2, 6, "2026-05-24", "confirmed"),

    Booking(6, 3, 10, "2026-05-25", "cancelled"),
    Booking(7, 3, 2, "2026-05-26", "pending"),

    Booking(8, 4, 9, "2026-05-27", "confirmed"),
    Booking(9, 4, 5, "2026-05-28", "completed"),

    Booking(10, 5, 8, "2026-05-29", "pending"),
    Booking(11, 5, 1, "2026-05-30", "confirmed"),

    Booking(12, 6, 4, "2026-06-01", "completed"),

    Booking(13, 7, 6, "2026-06-02", "pending"),
    Booking(14, 7, 7, "2026-06-03", "confirmed"),
    Booking(15, 7, 9, "2026-06-04", "pending"),

    Booking(16, 8, 2, "2026-06-05", "cancelled"),

    Booking(17, 9, 5, "2026-06-06", "completed"),
    Booking(18, 9, 10, "2026-06-07", "confirmed"),

    Booking(19, 10, 3, "2026-06-08", "pending"),
    Booking(20, 10, 8, "2026-06-09", "confirmed")
]

customers = [
    Customer(1, "Emmanuel Taiwo", "emmanuel@example.com"),
    Customer(2, "Sarah Johnson", "sarah.johnson@example.com"),
    Customer(3, "David Smith", "david.smith@example.com"),
    Customer(4, "Aisha Bello", "aisha.bello@example.com"),
    Customer(5, "Michael Brown", "michael.brown@example.com"),
    Customer(6, "Grace Williams", "grace.williams@example.com"),
    Customer(7, "Daniel Okafor", "daniel.okafor@example.com"),
    Customer(8, "Sophia Miller", "sophia.miller@example.com"),
    Customer(9, "James Carter", "james.carter@example.com"),
    Customer(10, "Amaka Nwosu", "amaka.nwosu@example.com"),
]

