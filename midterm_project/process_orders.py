# process_orders.py
import json
import sys
from collections import defaultdict

def normalize_phone(phone: str) -> str:
    """Convert phone to xxx-xxx-xxxx format, keeping only digits."""
    digits = ''.join(c for c in phone if c.isdigit())
    #Siggy dont forget the length is != because you want something less then a certain digit
    if len(digits) != 10:
        raise ValueError(f"Phone needs 10 digits: {phone}")
    return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
def main():
    if len(sys.argv) != 2:
        print("Usage: python process_orders.py <orders_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            orders = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    customers = {}
    items = defaultdict(lambda: {"price": 0.0, "orders": 0})

    for order in orders:
        name = order.get("customer_name")
        phone_raw = order.get("phone_number")
        if not name or not phone_raw:
            continue

        try:
            phone = normalize_phone(phone_raw)
        except ValueError as e:
            print(f"Skipping bad phone: {e}")
            continue

        # First name for this phone wins
        if phone not in customers:
            customers[phone] = name

        # Process items
        for item in order.get("items", []):
            item_name = item.get("name", "").strip()
            price = item.get("price")
            if not item_name or not isinstance(price, (int, float)):
                continue

            if item_name not in items:
                items[item_name]["price"] = float(price)

            items[item_name]["orders"] += 1
    # Write customers.json
    with open("customers.json", "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=2, sort_keys=True)
    # Write items.json (sorted by name)
    with open("items.json", "w", encoding="utf-8") as f:
        json.dump(dict(sorted(items.items())), f, indent=2)
    print(f"Processed {len(orders)} orders.")
    print(f"{len(customers)} customers, {len(items)} items saved.")
if __name__ == "__main__":
    main()