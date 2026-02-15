from sqlmodel import Session, select

from app.core.database import engine
from app.models.unit import Unit


# ======================================================
# HELPER: Avoid duplicate inserts
# ======================================================

def unit_exists(session: Session, unit_number: str) -> bool:
    statement = select(Unit).where(Unit.unit_number == unit_number)
    return session.exec(statement).first() is not None


# ======================================================
# SEEDER FUNCTION
# ======================================================

def seed_units():
    with Session(engine) as session:

        units_to_add = []

        # ======================================================
        # 🏨 Sukha Retreats Hotel Rooms
        # Floors:
        # 102–107
        # 202–207
        # 302–307
        # ======================================================

        for floor in [1, 2, 3]:
            for room in range(2, 8):  # 02 to 07
                unit_number = f"{floor}0{room}"

                if not unit_exists(session, unit_number):
                    units_to_add.append(
                        Unit(
                            property_name="Sukha Retreats",
                            unit_number=unit_number,
                            unit_type="room",
                            floor_number=floor,
                            building_block=None,
                            building_name=None,
                            billing_mode="daily",
                            status="active",
                        )
                    )

        # ======================================================
        # 🏢 Sukha Paradise — New Building Apartments
        # B101–B103 (Floor 1)
        # C101–C103 (Floor 2)
        # ======================================================

        new_apartments = [
            ("B101", 1),
            ("B102", 1),
            ("B103", 1),
            ("C101", 2),
            ("C102", 2),
            ("C103", 2),
        ]

        for unit_number, floor in new_apartments:
            if not unit_exists(session, unit_number):
                units_to_add.append(
                    Unit(
                        property_name="Sukha Paradise",
                        unit_number=unit_number,
                        unit_type="apartment",
                        floor_number=floor,
                        building_block=unit_number[0],
                        building_name="New Building",
                        billing_mode="daily",
                        status="active",
                    )
                )

        # ======================================================
        # 🏚 Sukha Paradise — Old Building Apartments
        # A103, B104, C104
        # Mostly monthly tenants
        # ======================================================

        old_apartments = [
            ("A103", 1),
            ("B104", 2),
            ("C104", 3),
        ]

        for unit_number, floor in old_apartments:
            if not unit_exists(session, unit_number):
                units_to_add.append(
                    Unit(
                        property_name="Sukha Paradise",
                        unit_number=unit_number,
                        unit_type="apartment",
                        floor_number=floor,
                        building_block=unit_number[0],
                        building_name="Old Building",
                        billing_mode="monthly",
                        status="active",
                    )
                )

        # ======================================================
        # SAVE ALL
        # ======================================================

        session.add_all(units_to_add)
        session.commit()

        print(f"✅ Seeded {len(units_to_add)} units successfully!")
if __name__ == "__main__":
    seed_units()

