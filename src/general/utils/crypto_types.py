"""This module defines custom types and classes for handling hexadecimal
    strings with specific constraints.
Classes:
    HexStr64: A class representing a hexadecimal string of fixed length 64.
    HexStr128: A class representing a hexadecimal string of fixed length 128.
    DjangoAdminAccount: A class representing an account in the Django admin system,
        inheriting from HexStr64.
    SigningKey: A class representing a signing key, inheriting from HexStr64.
    Signature: A class representing a signature, inheriting from HexStr128.
    HexStr (Annotated[str, StringConstraints]): A type alias for a hexadecimal
        string with a specific pattern constraint.
"""

from pydantic import StringConstraints
from typing_extensions import Annotated

HexStr = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]+$", strict=True)]


class HexStr64(HexStr):  # type: ignore
    """
    HexStr64 is a subclass of HexStr that represents a hexadecimal
        string with a fixed length of 64 characters.

    Attributes:
        min_length (int): The minimum length of the hexadecimal string, set to 64.
        max_length (int): The maximum length of the hexadecimal string, set to 64.
    """
    min_length = 64
    max_length = 64


class HexStr128(HexStr):  # type: ignore
    """
    A class representing a hexadecimal string of fixed length 128.

    This class inherits from `HexStr` and enforces that the hexadecimal string
    must have a minimum and maximum length of 128 characters.

    Attributes:
        min_length (int): The minimum length of the hexadecimal string (128).
        max_length (int): The maximum length of the hexadecimal string (128).
    """

    min_length = 128
    max_length = 128


# @Annotated
class DjangoAdminAccount(HexStr64):  # type: ignore
    """
    DjangoAdminAccount class that inherits from HexStr64.

    This class represents an account in the Django admin system. It extends the
    HexStr64 class, which is presumably a custom class for handling 64-character
    hexadecimal strings.

    Attributes:
        Inherits all attributes from HexStr64.

    Methods:
        Inherits all methods from HexStr64.
    """


# @Annotated
class SigningKey(HexStr64):
    """
    SigningKey class that inherits from HexStr64.

    This class represents a signing key in hexadecimal string format with a length of 64 characters.

    Attributes:
        None

    Methods:
        None
    """


# @Annotated
class Signature(HexStr128):
    """
    A class representing a 128-bit hexadecimal string signature.

    This class inherits from `HexStr128` and does not add any additional functionality
    or attributes. It is used to represent a specific type of hexadecimal string
    signature in the application.
    """
