from datetime import datetime
import Compartment from Compartments

class AccessToken:
    """Token for accessing a locker compartment"""

    def __init__(self, code: str, expiry: datetime, compartment: Compartment):
        """
        Args:
            code: Unique access code
            expiry: Expiration time of the token
            compartment: Associated compartment object
        """
        self.code = code
        self.expiry = expiry
        self.compartment = compartment

    def is_expired(self) -> bool:
        """Check if token has expired"""
        return datetime.now() > self.expiry

    def get_code(self) -> str:
        """Get the access code"""
        return self.code

    def get_compartment(self):
        """Get the associated compartment"""
        return self.compartment

    def __repr__(self) -> str:
        return f"AccessToken(code={self.code}, compartment={self.compartment})"
