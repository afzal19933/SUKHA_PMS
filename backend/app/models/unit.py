from typing import Optional
from sqlmodel import SQLModel, Field


# ======================================================
# UNIT MODEL
# Works for Hotel Rooms + Apartments (New & Old)
# ======================================================

class Unit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Property name
    # Example:
    # "Sukha Retreats"
    # "Sukha Paradise"
    property_name: str

    # Actual room/apartment number
    # Examples:
    # 102, 307, B101, C103, A103
    unit_number: str = Field(index=True)

    # room | apartment
    unit_type: str = Field(index=True)

    # Floor number (1,2,3...)
    floor_number: int

    # Building block (A,B,C or None for hotel rooms)
    building_block: Optional[str] = None

    # New Building / Old Building / None
    building_name: Optional[str] = None

    # daily | monthly
    billing_mode: str = "daily"

    # active / maintenance / occupied
    status: str = "active"

    # ======================================================
    # DISPLAY NAME (Used everywhere in UI & API)
    # ======================================================

    def display_name(self) -> str:
        """
        Returns formatted unit name.

        Hotel Room:
            307

        New Apartment:
            B101 (New Building)

        Old Apartment:
            A103 (Old Building)
        """

        if self.unit_type == "apartment" and self.building_name:
            return f"{self.unit_number} ({self.building_name})"

        return self.unit_number
