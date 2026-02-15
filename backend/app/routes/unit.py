from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.permissions import require_roles

from app.models.unit import Unit
from app.models.stay import Stay
from app.models.user import User


router = APIRouter(prefix="/units", tags=["Units"])


# ======================================================
# FORMAT DISPLAY NAME
# ======================================================
def format_unit_display(unit: Unit) -> str:
    if unit.unit_type == "apartment" and unit.building_name:
        return f"{unit.unit_number} ({unit.building_name})"
    return unit.unit_number


# ======================================================
# BUILD LIVE STATUS USING STAY MODEL
# ======================================================
def build_unit_status(unit: Unit, stay: Stay | None):

    if not stay:
        return {
            "status": "vacant",
            "label": "Vacant",
            "guest_source": None,
            "estimated_checkout": None,
        }

    if stay.stay_type == "daily":
        return {
            "status": "occupied",
            "label": f"Occupied ({stay.guest_source.capitalize()})",
            "guest_source": stay.guest_source,
            "estimated_checkout": stay.check_out_date,
        }

    if stay.stay_type == "monthly":
        return {
            "status": "monthly",
            "label": f"Monthly Tenant ({stay.planned_months} Months)"
            if stay.planned_months
            else "Monthly Tenant",
            "guest_source": stay.guest_source,
            "estimated_checkout": stay.estimated_checkout(),
        }

    if stay.stay_type == "yearly":
        return {
            "status": "yearly",
            "label": "Yearly Tenant",
            "guest_source": stay.guest_source,
            "estimated_checkout": stay.estimated_checkout(),
        }

    return {
        "status": "unknown",
        "label": "Unknown",
        "guest_source": None,
        "estimated_checkout": None,
    }


# ======================================================
# GET ALL UNITS WITH LIVE STAY STATUS
# ======================================================
@router.get("/")
def get_all_units(
    session: Session = Depends(get_session),
    user: User = Depends(
        require_roles(
            [
                "admin",
                "hotel_owner",
                "apartment_owner",
                "supervisor",
                "reception",
            ]
        )
    ),
):

    statement = select(Unit).order_by(Unit.unit_number)
    units = session.exec(statement).all()

    response = []

    for unit in units:
        stay_statement = (
            select(Stay)
            .where(Stay.unit_id == unit.id)
            .where(Stay.status == "active")
        )
        stay = session.exec(stay_statement).first()

        status_info = build_unit_status(unit, stay)

        response.append(
            {
                "id": unit.id,
                "display_name": format_unit_display(unit),
                "property_name": unit.property_name,
                "unit_type": unit.unit_type,
                "floor_number": unit.floor_number,
                "building_name": unit.building_name,
                "billing_mode": unit.billing_mode,
                "status": status_info["status"],
                "status_label": status_info["label"],
                "guest_source": status_info["guest_source"],
                "estimated_checkout": status_info["estimated_checkout"],
            }
        )

    return response


# ======================================================
# GET AVAILABLE (VACANT) UNITS
# MUST COME BEFORE /{unit_id}
# ======================================================
@router.get("/available")
def get_available_units(
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

    active_stays_statement = select(Stay).where(Stay.status == "active")
    active_stays = session.exec(active_stays_statement).all()

    occupied_unit_ids = {stay.unit_id for stay in active_stays}

    units_statement = select(Unit).order_by(Unit.unit_number)
    units = session.exec(units_statement).all()

    available_units = []

    for unit in units:
        if unit.id not in occupied_unit_ids:
            available_units.append(
                {
                    "id": unit.id,
                    "display_name": format_unit_display(unit),
                    "property_name": unit.property_name,
                    "unit_type": unit.unit_type,
                    "floor_number": unit.floor_number,
                    "building_name": unit.building_name,
                }
            )

    return available_units


# ======================================================
# GET SINGLE UNIT WITH LIVE STATUS
# MUST ALWAYS BE LAST
# ======================================================
@router.get("/{unit_id}")
def get_unit(
    unit_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    unit = session.get(Unit, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    stay_statement = (
        select(Stay)
        .where(Stay.unit_id == unit.id)
        .where(Stay.status == "active")
    )
    stay = session.exec(stay_statement).first()

    status_info = build_unit_status(unit, stay)

    return {
        "id": unit.id,
        "display_name": format_unit_display(unit),
        "status": status_info["status"],
        "status_label": status_info["label"],
        "guest_source": status_info["guest_source"],
        "estimated_checkout": status_info["estimated_checkout"],
    }
