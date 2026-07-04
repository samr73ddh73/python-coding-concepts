from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enums import Size, LockerStatus
from Compartments import Compartment
from AccessToken import AccessToken
import uuid


class Locker:
    """Amazon Locker - stores and manages compartments for package delivery"""

    def __init__(self, locker_id: str):
        """
        Args:
            locker_id: Unique identifier for the locker
        """
        self.locker_id = locker_id
        self.compartments: List[Compartment] = []
        self.compartment_by_id: Dict[str, Compartment] = {}
        self.access_tokens: Dict[str, AccessToken] = {}

    def add_compartment(self, size: Size, quantity: int = 1) -> None:
        """
        Add compartments of a specific size

        Args:
            size: Size of compartments to add
            quantity: Number of compartments to add
        """
        for _ in range(quantity):
            compartment = Compartment(size)
            self.compartments.append(compartment)
            # Use index as compartment ID
            comp_id = f"{self.locker_id}_C{len(self.compartments) - 1}"
            self.compartment_by_id[comp_id] = compartment

    def find_available_compartment(self, package_size: Size) -> Optional[Compartment]:
        """
        Find an available compartment for a package

        Args:
            package_size: Size of package to store

        Returns:
            Available compartment or None if not found
        """
        for compartment in self.compartments:
            if (compartment.get_status() == LockerStatus.AVAILABLE and
                compartment.can_fit_package(package_size)):
                return compartment
        return None

    def deliver_package(self, package_size: Size, expiry_hours: int = 24) -> Optional[AccessToken]:
        """
        Deliver a package to the locker

        Args:
            package_size: Size of the package
            expiry_hours: Hours until access token expires

        Returns:
            AccessToken for pickup or None if no available compartment
        """
        compartment = self.find_available_compartment(package_size)
        if not compartment:
            return None

        # Book the compartment
        if not compartment.book(package_size):
            return None

        # Mark as occupied
        compartment.mark_occupied()

        # Generate access token
        code = str(uuid.uuid4())[:6].upper()
        expiry = datetime.now() + timedelta(hours=expiry_hours)
        token = AccessToken(code, expiry, compartment)

        # Store token
        self.access_tokens[code] = token
        compartment.set_access_token(token)

        return token

    def pickup_package(self, access_code: str) -> bool:
        """
        Pick up a package using access code

        Args:
            access_code: Access code from delivery

        Returns:
            True if pickup successful, False otherwise
        """
        if access_code not in self.access_tokens:
            return False

        token = self.access_tokens[access_code]

        # Check if token expired
        if token.is_expired():
            return False

        # Get compartment and mark as available
        compartment = token.get_compartment()
        compartment.mark_available()

        # Remove token
        del self.access_tokens[access_code]

        return True

    def get_available_compartments_count(self) -> int:
        """Get number of available compartments"""
        return sum(1 for c in self.compartments if c.get_status() == LockerStatus.AVAILABLE)

    def get_occupied_compartments_count(self) -> int:
        """Get number of occupied compartments"""
        return sum(1 for c in self.compartments if c.get_status() == LockerStatus.OCCUPIED)

    def get_compartments_by_size(self, size: Size) -> List[Compartment]:
        """Get all compartments of a specific size"""
        return [c for c in self.compartments if c.get_size() == size]

    def get_all_compartments_status(self) -> Dict[str, int]:
        """Get count of compartments by status"""
        status_count = {}
        for compartment in self.compartments:
            status = compartment.get_status().value
            status_count[status] = status_count.get(status, 0) + 1
        return status_count

    def __repr__(self) -> str:
        return (f"Locker(id={self.locker_id}, "
                f"compartments={len(self.compartments)}, "
                f"available={self.get_available_compartments_count()})")


# ============================================================
# DEMO USAGE
# ============================================================

if __name__ == "__main__":
    # Create a locker
    locker = Locker("LOC-001")

    # Add compartments of different sizes
    locker.add_compartment(Size.SMALL, 5)
    locker.add_compartment(Size.MEDIUM, 3)
    locker.add_compartment(Size.LARGE, 2)

    print(f"Locker created: {locker}")
    print(f"Status: {locker.get_all_compartments_status()}\n")

    # Deliver packages
    print("Delivering packages:")
    token1 = locker.deliver_package(Size.SMALL)
    print(f"  Package 1 (SMALL): {token1.get_code() if token1 else 'Failed'}")

    token2 = locker.deliver_package(Size.LARGE)
    print(f"  Package 2 (LARGE): {token2.get_code() if token2 else 'Failed'}")

    print(f"\nStatus after delivery: {locker.get_all_compartments_status()}")

    # Pick up packages
    print("\nPickup packages:")
    success = locker.pickup_package(token1.get_code())
    print(f"  Pickup 1: {'Success' if success else 'Failed'}")

    success = locker.pickup_package(token2.get_code())
    print(f"  Pickup 2: {'Success' if success else 'Failed'}")

    print(f"\nFinal status: {locker.get_all_compartments_status()}")
