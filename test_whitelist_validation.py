"""Test script to validate whitelist functionality"""

import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.users.services import UserService


def test_whitelist_validation():
    """Test the whitelist validation functionality"""

    # Test with an email that should be in the whitelist
    whitelisted_email = "nolan@gmail.com"
    result = UserService._is_email_in_whitelist(whitelisted_email)
    print(f"Email '{whitelisted_email}' is in whitelist: {result}")

    # Test with an email that should NOT be in the whitelist
    non_whitelisted_email = "test@example.com"
    result = UserService._is_email_in_whitelist(non_whitelisted_email)
    print(f"Email '{non_whitelisted_email}' is in whitelist: {result}")

    # Test case sensitivity
    case_test_email = "NOLAN@GMAIL.COM"
    result = UserService._is_email_in_whitelist(case_test_email)
    print(f"Email '{case_test_email}' (case test) is in whitelist: {result}")


if __name__ == "__main__":
    test_whitelist_validation()
