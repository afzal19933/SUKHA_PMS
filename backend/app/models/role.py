from enum import Enum

class Role(str, Enum):
    owner = "owner"
    manager = "manager"
    reception = "reception"
    housekeeping = "housekeeping"
