from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import date

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.permissions import require_roles

from app.models.stay import Stay
from app.models.unit import Unit
from app.models.user import User


router = APIRouter(prefix="/stays", tags=["Stays"])


# ======================================================
# CHECK IF UNIT ALREADY OCCUPIED
# ======================================================
def check_active_stay(session: Session, unit_id: int):
    statement = (
        select(Stay)
        .where(Stay.unit_id == unit_id)
        .where(Stay.status == "active")
    )
    return session.exec(statement).first()


# ======================================================
# POST /stays  → CHECK-IN API
# ======================================================
@router.post("/")
def create_stay(
    stay: Stay,
    session: Session = Depends(get_session),
    user: User = Depends(
        require_roles(
            [
                "admin",
                "hotel_owner",
                "apartment_owner",
                "reception",
                "supervisor",
            ]
        )
    ),
):

    # Check unit exists
    unit = session.get(Unit, stay.unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    # Prevent double occupancy
    existing = check_active_stay(session, stay.unit_id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="This unit already has an active stay",
        )

    # Auto logic for yearly tenant
    if stay.stay_type == "yearly" and not stay.planned_months:
        stay.planned_months = 12

    # Daily stay must have checkout date
    if stay.stay_type == "daily" and not stay.check_out_date:
        raise HTTPException(
            status_code=400,
            detail="Daily stay requires check_out_date",
        )

    # Monthly/yearly require planned months
    if stay.stay_type in ["monthly", "yearly"] and not stay.planned_months:
        raise HTTPException(
            status_code=400,
            detail="Monthly/Yearly stay requires planned_months",
        )

    session.add(stay)
    session.commit()
    session.refresh(stay)

    return {
        "message": "Stay created successfully",
        "stay_id": stay.id,
        "estimated_checkout": stay.estimated_checkout(),
    }


# ======================================================
# GET ALL ACTIVE STAYS
# ======================================================
@router.get("/")
def get_all_stays(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    statement = select(Stay).where(Stay.status == "active")
    stays = session.exec(statement).all()

    return stays


# ======================================================
# CHECKOUT (COMPLETE STAY)
# ======================================================
@router.patch("/{stay_id}/checkout")
def checkout_stay(
    stay_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(require_roles(["admin", "reception"])),
):

    stay = session.get(Stay, stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail="Stay not found")

    stay.status = "completed"

    # Auto set checkout date if tenant
    if not stay.check_out_date:
        stay.check_out_date = date.today()

    session.add(stay)
    session.commit()

    return {"message": "Checkout completed"}
