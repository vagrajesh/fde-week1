import csv
from collections import defaultdict

INPUT_FILE = "data/invoice_50k.csv"
OUTPUT_FILE = "data/high_value_invoices.csv"
VENDOR_TOTALS_FILE = "data/vendor_totals.csv"
HIGH_VALUE_THRESHOLD = 900000


def read_invoice(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        # blank cells become None so float() raises TypeError for them
        row["amount"] = row["amount"].strip() or None
    return rows


def validate_invoice(invoice):
    """Return (amount, reason); amount is None when missing/invalid."""
    try:
        return float(invoice["amount"]), None
    except TypeError:
        return None, "amount is missing"
    except ValueError:
        return None, f"invalid amount '{invoice['amount']}'"


def get_approver(amount):
    if amount > 500000:
        return "Finance Controller"
    elif amount > 100000:
        return "Manager"
    else:
        return "Standard"


def calculate_total(invoices):
    totals = defaultdict(float)
    for invoice in invoices:
        vendor = invoice["vendor"] or "UNKNOWN"
        totals[vendor] += invoice["amount"]
    return totals


def write_output(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    try:
        invoices = read_invoice(INPUT_FILE)
    except FileNotFoundError:
        print(f"File not found: {INPUT_FILE}")
        return

    high_value = []
    skipped = []
    for invoice in invoices:
        amount, reason = validate_invoice(invoice)
        if amount is None:
            skipped.append((invoice["invoice_id"], reason))
            continue
        if amount > HIGH_VALUE_THRESHOLD:
            invoice["amount"] = amount
            invoice["approver"] = get_approver(amount)
            high_value.append(invoice)
            print(invoice["invoice_id"], invoice["vendor"], amount, invoice["approver"])

    write_output(OUTPUT_FILE, high_value, ["invoice_id", "vendor", "amount", "status", "approver"])

    totals = calculate_total(high_value)
    write_output(
        VENDOR_TOTALS_FILE,
        [{"vendor": v, "total": round(t, 2)} for v, t in sorted(totals.items())],
        ["vendor", "total"],
    )
    print(f"\n{len(high_value)} high-value invoices written to {OUTPUT_FILE}")

    print("\nGroup totals by vendor")
    for vendor, total in sorted(totals.items()):
        print(f"{vendor}: {total:,.2f}")

    print(f"\nSkipped invoices ({len(skipped)})")
    for invoice_id, reason in skipped:
        print(f"{invoice_id}: {reason}")


main()
