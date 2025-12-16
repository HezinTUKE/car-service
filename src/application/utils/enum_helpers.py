"""
Helper functions for working with Enums in SQLAlchemy models.

This module provides utilities to create enum columns that store as VARCHAR
in the database but work as Python Enums in application code.
"""

from typing import Type
from enum import Enum
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from .type_decorators import EnumAsVarchar


def enum_column(enum_class: Type[Enum], length: int = None, **kwargs):
    """
    Create a mapped column for an Enum that stores as VARCHAR in database.

    This is a convenience function that automatically calculates the appropriate
    VARCHAR length based on the enum values if not provided.

    Args:
        enum_class: The Python Enum class to use
        length: Optional VARCHAR length. If not provided, will be calculated
                from the longest enum value + some buffer
        **kwargs: Additional arguments passed to mapped_column

    Returns:
        A mapped_column configured with EnumAsVarchar type

    Example:
        status: Mapped[MessageStatus] = enum_column(
            MessageStatus,
            nullable=False,
            default=MessageStatus.CREATED,
            index=True
        )
    """
    if length is None:
        # Calculate length based on longest enum value + buffer
        max_length = max(len(item.value) for item in enum_class)
        length = max_length + 5  # Add some buffer

    return mapped_column(
        EnumAsVarchar(enum_class, length=length),
        **kwargs
    )


def get_enum_max_length(enum_class: Type[Enum], buffer: int = 5) -> int:
    """
    Calculate the maximum length needed for an enum's VARCHAR storage.

    Args:
        enum_class: The Python Enum class
        buffer: Additional buffer to add to the max length

    Returns:
        The recommended VARCHAR length
    """
    max_length = max(len(item.value) for item in enum_class)
    return max_length + buffer
