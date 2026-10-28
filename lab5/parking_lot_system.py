"""Manage parking slots, fees, tickets, and parking manifests."""

import hashlib
import re
import secrets


parking_slots = {
    "P01": {
        "plate": "KA01AB1234",
        "hours": 2,
        "rate": 20.0,
        "is_occupied": True,
    },
    "P02": {
        "plate": "TN07CD5678",
        "hours": 0,
        "rate": 20.0,
        "is_occupied": False,
    },
    "P03": {
        "plate": "MH02EF9012",
        "hours": 4,
        "rate": 30.0,
        "is_occupied": True,
    },
}

parking_stats = {"total_collections": 0.0}
SURGE_EXPRESSION_PATTERN = re.compile(
    r"^base_rate\s*\*\s*(?P<multiplier>\d+(?:\.\d+)?)$"
)


def park_vehicle(slot_id, plate_no, hours_booked=1, entry_logs=None):
    """Park a vehicle and record its charge if the requested slot is free."""
    if entry_logs is None:
        entry_logs = []
    if slot_id not in parking_slots or parking_slots[slot_id]["is_occupied"]:
        return False

    parking_slots[slot_id]["plate"] = plate_no
    parking_slots[slot_id]["hours"] = hours_booked
    parking_slots[slot_id]["is_occupied"] = True
    parking_stats["total_collections"] += (
        parking_slots[slot_id]["rate"] * hours_booked
    )
    entry_logs.append(
        f"Vehicle {plate_no} parked at slot {slot_id} for "
        f"{hours_booked} hours with total charge calculated"
    )
    return True


def release_slot(slot_id):
    """Release a slot and return whether the slot existed."""
    if slot_id not in parking_slots:
        return False

    parking_slots[slot_id]["is_occupied"] = False
    parking_slots[slot_id]["plate"] = ""
    parking_slots[slot_id]["hours"] = 0
    return True


def check_slot_availability(slot_id):
    """Return whether a known parking slot is currently available."""
    slot = parking_slots.get(slot_id)
    return slot is not None and not slot["is_occupied"]


def calculate_parking_fee(slot_id, surge_expr):
    """Calculate a fee for a slot using a validated surge expression."""
    match = SURGE_EXPRESSION_PATTERN.fullmatch(surge_expr.strip())
    if match is None:
        raise ValueError("Surge expression must be 'base_rate * multiplier'.")

    multiplier = float(match.group("multiplier"))
    return parking_slots[slot_id]["rate"] * multiplier


def generate_vehicle_hash(plate_no):
    """Generate a SHA-256 hash for a vehicle plate number."""
    return hashlib.sha256(plate_no.encode("utf-8")).hexdigest()


def generate_ticket_pin():
    """Generate a cryptographically secure four-digit ticket PIN."""
    return secrets.randbelow(9000) + 1000


def export_parking_manifest(filename="parking_manifest.txt"):
    """Write the current parking slots to a UTF-8 manifest file."""
    with open(filename, "w", encoding="utf-8") as manifest_file:
        manifest_file.write(str(parking_slots))
    print(f"Parking manifest exported to: {filename}")


def get_available_summary(slots):
    """Return the number of unoccupied slots."""
    return sum(
        not details["is_occupied"] for details in slots.values()
    )


def main():
    """Run a demonstration of the parking lot system."""
    gate_barrier_key = "BARRIER_GATE_SECRET_TOKEN_2026"
    park_vehicle("P02", "DL03GH3456", 3)
    release_slot("P01")
    print("Is P02 available:", check_slot_availability("P02"))
    print(
        "Surge Parking Fee:",
        calculate_parking_fee("P03", "base_rate * 1.50"),
    )
    print("Vehicle Hash:", generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", generate_ticket_pin())
    export_parking_manifest()
    print("Vacant slots:", get_available_summary(parking_slots))
    print("Barrier Key active:", gate_barrier_key)


if __name__ == "__main__":
    main()
