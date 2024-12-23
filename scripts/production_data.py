"""This script is used to generate a new account and secret key for the Django project."""

import sys

from django.core.management.utils import get_random_secret_key

from src.general.utils.cryptography import generate_key_pair


def generate_account():
    """
    Generates a new account by creating a key pair and prints the signing key and account number.

    The function generates a key pair using the `generate_key_pair` function,
    then prints the private key (referred to as the signing key)
    and the public key (referred to as the account number).

    Returns:
        None
    """
    key_pair = generate_key_pair()
    print(f"SIGNING_KEY={key_pair.private}")
    print(f"ACCOUNT_NUMBER={key_pair.public}")


def generate_secret_key():
    """
    Generates a random secret key and prints it.

    This function uses the `get_random_secret_key` function to generate a
    random secret key and then prints it in the format "SECRET_KEY: <secret_key>".

    Returns:
        None
    """
    secret_key = get_random_secret_key()
    print(f"SECRET_KEY={secret_key}")


if __name__ == "__main__":
    is_file_arg = len(sys.argv) > 1 and sys.argv[1] == "--file"

    if is_file_arg:
        if len(sys.argv) > 2:
            file_name = sys.argv[2]
            with open(file_name, "w", encoding="utf-8") as f:
                sys.stdout = f
                generate_account()
                generate_secret_key()
        else:
            print("No file name provided, printing to console.")
    else:
        sys.stdout = sys.__stdout__
        print("\n" + "*" * 50 + "\n")
        generate_account()
        print("\n" + "_" * 50 + "\n")
        generate_secret_key()
        print("\n" + "*" * 50 + "\n")
