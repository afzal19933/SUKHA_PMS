from enum import Enum

class Role(str, Enum):
    admin = "admin"        # 👈 ADD THIS LINE
    owner = "owner"
    manager = "manager"
    reception = "reception"
    housekeeping = "housekeeping"
