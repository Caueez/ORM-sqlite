

from enum import StrEnum


class DataType(StrEnum):
    NULL = "NULL"
    INTEGER = "INTEGER"
    REAL = "REAL"
    TEXT = "TEXT"
    BLOB = "BLOB"

class Constraints(StrEnum):
    PRIMARY_KEY = "PRIMARY KEY"
    AUTOINCREMENT = "AUTOINCREMENT"
    NOT_NULL = "NOT NULL"
    NULL = "NULL"
    UNIQUE = "UNIQUE"
    DEFAULT = "DEFAULT"
    FOREIGN_KEY = "FOREIGN KEY"


class Column:
    def __init__(self, name: str, data_type: DataType, constraints: list[Constraints] = []):
        self.name = name
        self.data_type = data_type
        self.constraints = constraints

    def _validate(self) -> None:
        try:
            self._name_validation()
            self._constraints_validation()
        except ValueError as e:
            raise ValueError(f"Column validation failed: {e}")

    def _name_validation(self):
        if len(self.name) < 1:
            raise ValueError("The column name must have at least 1 character.")

    def _constraints_validation(self):
        if Constraints.PRIMARY_KEY and Constraints.UNIQUE in self.constraints:
            raise ValueError("A column cannot have both PRIMARY KEY and UNIQUE constraints.")

        if Constraints.NOT_NULL and Constraints.DEFAULT in self.constraints:
            raise ValueError("A column cannot have both NOT NULL and DEFAULT constraints.")
        
        if Constraints.AUTOINCREMENT and not Constraints.PRIMARY_KEY in self.constraints:
            raise ValueError("AUTOINCREMENT constraint can only be used with PRIMARY KEY constraint.")
        
        if Constraints.AUTOINCREMENT and Constraints.PRIMARY_KEY in self.constraints and self.data_type != DataType.INTEGER:
            raise ValueError("AUTOINCREMENT constraint can only be used with INTEGER data type.")

        if Constraints.NOT_NULL and Constraints.DEFAULT in self.constraints:
            raise ValueError("A column cannot have both NOT NULL and DEFAULT constraints.")

    def __repr__(self):
        return f"Column(name={self.name}, data_type={self.data_type})"


class Table:
    def __init__(self, name: str, primary_key: str, columns: list[str]):
        self._validate()
        
        self.name = name
        self.primary_key = primary_key
        self.columns = columns

    def _validate(self) -> None:
        try:
            self._name_validation()
            self._pk_validation()
            self._columns_validation()
        except ValueError as e:
            raise ValueError(f"Table validation failed: {e}")

    def _name_validation(self):
        if len(self.name) < 1:
            raise ValueError("The table name must have at least 1 character.")

    def _pk_validation(self):
        if self.primary_key not in self.columns:
            raise ValueError(f"Primary key '{self.primary_key}' is not in the list of columns: {self.columns}")

    def _columns_validation(self):
        if len(self.columns) < 1:
            raise ValueError("The table must have at least 1 column.")

    def alter_table(self, new_columns: list[str]):
        self.columns = new_columns

    def __repr__(self):
        return f"Table(name={self.name}, columns={self.columns})"