from typing import Optional, TYPE_CHECKING
from enums import Size, LockerStatus

if TYPE_CHECKING:
    from AccessToken import AccessToken


class Compartment:
    """A single compartment in a locker"""

    def __init__(self, size: Size) -> None:
        """
        Args:
            size: Size of the compartment
        """
        self.size: Size = size
        self.status: LockerStatus = LockerStatus.AVAILABLE
        self.access_token: Optional["AccessToken"] = None

    def can_fit_package(self, package_size: Size) -> bool:
        """Check if package size matches compartment size"""
        return package_size == self.size

    def book(self, package_size: Size) -> bool:
        """
        Book the compartment for a package

        Args:
            package_size: Size of the package to store

        Returns:
            True if booking successful, False otherwise
        """
        if not self.can_fit_package(package_size):
            return False

        if self.status != LockerStatus.AVAILABLE:
            return False

        self.status = LockerStatus.RESERVED
        return True

    def get_size(self) -> Size:
        """Get compartment size"""
        return self.size

    def get_status(self) -> LockerStatus:
        """Get compartment status"""
        return self.status

    def mark_occupied(self) -> None:
        """Mark compartment as occupied (package inside)"""
        self.status = LockerStatus.OCCUPIED

    def mark_available(self) -> None:
        """Mark compartment as available"""
        self.status = LockerStatus.AVAILABLE
        self.access_token = None

    def set_access_token(self, token: "AccessToken") -> None:
        """Set access token for this compartment"""
        self.access_token = token

    def get_access_token(self) -> Optional["AccessToken"]:
        """Get access token for this compartment"""
        return self.access_token

    def __repr__(self) -> str:
        return f"Compartment(size={self.size.value}, status={self.status.value})"
