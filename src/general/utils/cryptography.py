""" This module contains utility functions for cryptographic operations. """

from typing import NamedTuple

from nacl.signing import SigningKey as NaClSigningKey

from .crypto_types import DjangoAdminAccount, HexStr, SigningKey


class KeyPair(NamedTuple):
    """
    A NamedTuple representing a cryptographic key pair.

    Attributes:
        private (str): The private key as a string.
        public (str): The public key as a string.
    """

    private: str
    public: str


def bytes_to_hex(bytes_: bytes) -> HexStr:
    """
    Convert a bytes object to a hexadecimal string.

    Args:
        bytes_ (bytes): The bytes object to convert.

    Returns:
        hexstr: The resulting hexadecimal string.
    """
    return HexStr(bytes(bytes_).hex())


def derive_public_key(signing_key: SigningKey) -> DjangoAdminAccount:
    """
    Derives a public key from the given signing key and returns a DjangoAdminAccount instance.

    Args:
        signing_key (SigningKey): The signing key from which to derive the public key.

    Returns:
        DjangoAdminAccount: An instance of DjangoAdminAccount containing the derived public key.
    """
    return DjangoAdminAccount(bytes_to_hex(NaClSigningKey(hex_to_bytes(signing_key)).verify_key))


def generate_key_pair() -> KeyPair:
    """
    Generates a new NaCl key pair for signing and verification.

    Returns:
        KeyPair: An object containing the generated private and public keys in hexadecimal format.
    """
    signing_key = NaClSigningKey.generate()
    return KeyPair(
        private=bytes_to_hex(bytes(signing_key)),
        public=bytes_to_hex(signing_key.verify_key),
    )


def hex_to_bytes(hex_string: HexStr) -> bytes:
    """
    Convert a hexadecimal string to bytes.

    Args:
        hex_string (hexstr): The hexadecimal string to convert.

    Returns:
        bytes: The resulting bytes from the hexadecimal string.
    """
    return bytes.fromhex(hex_string)
