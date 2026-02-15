from typing import Optional
from datetime import date, datetime, timedelta

from sqlmodel import SQLModel, Field


# ======================================================
# STAY MODEL
# Supports:
# - Daily Sukha guests
# - Ayursiha guests
# - Monthly tenants
# - Yearly tenants
# ======================================================

class Stay(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # ======================================================
    # UNIT LINK
    # ======================================================
    unit_id: int = Field(index=True)

    # ======================================================
    # GUEST DETAILS
    # ======================================================
    guest_name: str

    # "sukha" | "ayursiha"
    guest_source: str = Field(index=True)

    # "daily" | "monthly" | "yearly"
    stay_type: str = Field(index=True)

    # ======================================================
    # DATE DETAILS
    # ======================================================
    check_in_date: date

    # Used mainly for daily guests
    check_out_date: Optional[date] = None

    # ======================================================
    # TENANT DETAILS (Monthly / Yearly)
    # ======================================================

    # Example:
    # 2 months stay → planned_months = 2
    # yearly tenant → planned_months = 12
    planned_months: Optional[int] = None

    # Monthly payment due day
    # Example: 5 → rent due every 5th
    monthly_due_day: Optional[int] = None

    # Rent amount for tenants
    monthly_rent: Optional[float] = None

    # ======================================================
    # ADVANCE PAYMENT
    # ======================================================
    advance_amount: Optional[float] = None
    advance_refunded: bool = False

    # ======================================================
    # STATUS
    # ======================================================
    # active → currently staying
    # completed → checked out
    status: str = Field(default="active", index=True)

    # ======================================================
    # META
    # ======================================================
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # ======================================================
    # AUTO ESTIMATED CHECKOUT CALCULATION
    # ======================================================
    def estimated_checkout(self) -> Optional[date]:
        """
        For monthly/yearly tenants:
        Calculate estimated checkout using planned months.

        For daily guests:
        Return actual checkout date.
        """
        if self.stay_type in ["monthly", "yearly"] and self.planned_months:
            return self.check_in_date + timedelta(days=30 * self.planned_months)

        return self.check_out_date
