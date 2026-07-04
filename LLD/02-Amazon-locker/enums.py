from enum import Enum


class Size(Enum):
    """Locker compartment sizes"""
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    EXTRA_LARGE = "EXTRA_LARGE"


class LockerStatus(Enum):
    """Status of a locker compartment"""
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    RESERVED = "RESERVED"
    MAINTENANCE = "MAINTENANCE"


class DeliveryStatus(Enum):
    """Status of a package delivery"""
    PENDING = "PENDING"
    DELIVERED = "DELIVERED"
    PICKED_UP = "PICKED_UP"
    CANCELLED = "CANCELLED"
