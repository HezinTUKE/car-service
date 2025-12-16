from typing import Type, Optional
from enum import Enum
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator


class EnumAsVarchar(TypeDecorator):
    """
    Stores Python Enum as VARCHAR in database.

    In migrations, this will appear as sa.String(length=X) or VARCHAR,
    making it database-agnostic and not dependent on custom types.

    Usage:
        status: Mapped[MessageStatus] = mapped_column(
            EnumAsVarchar(MessageStatus, length=24),
            nullable=False,
            default=MessageStatus.CREATED,
        )
    """

    impl = String
    cache_ok = True

    def __init__(self, enum_class: Type[Enum], length: int, **kwargs):
        """
        Args:
            enum_class: The Python Enum class to use
            length: VARCHAR length for the database column
        """
        self.enum_class = enum_class
        super().__init__(length=length, **kwargs)

    def process_bind_param(self, value: Optional[Enum], dialect) -> Optional[str]:
        """Convert Python Enum to string for database storage"""
        if value is None:
            return None
        if isinstance(value, self.enum_class):
            return value.value
        # Handle case where string is passed directly
        if isinstance(value, str):
            # Validate it's a valid enum value
            try:
                self.enum_class(value)
                return value
            except ValueError:
                raise ValueError(f"'{value}' is not a valid {self.enum_class.__name__}")
        raise TypeError(f"Expected {self.enum_class.__name__} or str, got {type(value)}")

    def process_result_value(self, value: Optional[str], dialect) -> Optional[Enum]:
        """Convert database string back to Python Enum"""
        if value is None:
            return None
        try:
            return self.enum_class(value)
        except ValueError:
            raise ValueError(f"'{value}' is not a valid {self.enum_class.__name__}")

    def copy(self, **kwargs):
        """Required for proper SQLAlchemy type copying"""
        return EnumAsVarchar(self.enum_class, self.impl.length, **kwargs)

    def compare_values(self, x, y):
        """Custom comparison for Alembic migrations"""
        return x == y

    @property
    def python_type(self):
        """Return the Python type for this column"""
        return self.enum_class

    def adapt(self, cls):
        """Adapt this type to work with different SQL dialects"""
        return cls(length=self.impl.length)

    def get_col_spec(self, **kwargs):
        """Return the column specification for DDL"""
        return f"VARCHAR({self.impl.length})"

    def bind_expression(self, bindvalue):
        """Return the bind expression for this type"""
        return bindvalue

    def column_expression(self, col):
        """Return the column expression for this type"""
        return col

    def literal_processor(self, dialect):
        """Return a conversion callable for this type"""
        impl_processor = self.impl.literal_processor(dialect)
        if impl_processor:
            def process(value):
                if isinstance(value, self.enum_class):
                    value = value.value
                return impl_processor(value)
            return process
        else:
            def process(value):
                if isinstance(value, self.enum_class):
                    return f"'{value.value}'"
                return f"'{value}'"
            return process

    @classmethod
    def compare_type_for_alembic(cls, context, inspected_column, metadata_column, inspected_type, metadata_type):
        """
        Custom type comparison function for Alembic.

        This function ensures that EnumAsVarchar types are treated as String types
        in migrations, making them database-agnostic and self-contained.
        """
        # If the metadata type is EnumAsVarchar, treat it as String for comparison
        if isinstance(metadata_type, cls):
            # Get the length from the EnumAsVarchar's impl (String) type
            expected_length = metadata_type.impl.length

            # Compare the inspected type with the expected length
            if hasattr(inspected_type, 'length'):
                return inspected_type.length == expected_length

            # If we can't compare lengths, assume they're the same type family
            return str(type(inspected_type)).lower().find('string') != -1 or \
                   str(type(inspected_type)).lower().find('varchar') != -1

        # Not our type, let other handlers deal with it
        return None

    @classmethod
    def render_item_for_alembic(cls, type_, obj, autogen_context):
        """
        Custom rendering function for Alembic migrations.

        This ensures that EnumAsVarchar types are rendered as sa.String()
        in migration files instead of the custom type reference.
        """
        if isinstance(obj, cls):
            # Render as sa.String with the appropriate length
            length = obj.impl.length
            return f"sa.String(length={length})"

        # Not our type, let other handlers deal with it
        return False


# Registry of custom types that need special handling in Alembic
CUSTOM_ALEMBIC_TYPES = [
    EnumAsVarchar,
    # Add other custom types here as needed
]
