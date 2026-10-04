import csv
import statistics
from collections import defaultdict
from pathlib import Path

INPUT_FILE = "data/invoice_50k.csv"
OUTPUT_DIR = Path("data/metrics")
COLUMNS = ["invoice_id", "vendor", "amount", "status"]
BANDS = [
    ("<= 10,000", 0, 10000),
    ("10,001 - 100,000", 10000, 100000),
    ("100,001 - 500,000", 100000, 500000),
    ("> 500,000", 500000, float("inf")),
]


def read_invoices(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def parse_amount(raw):
    """Return the amount as a float, or None if blank/invalid."""
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def get_approver(amount):
    if amount > 500000:
        return "Finance Controller"
    elif amount > 100000:
        return "Manager"
    return "Standard"


def write_csv(filename, rows, fieldnames):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  written: {path}")


def summary_kpis(rows, valid):
    vendors = {r["vendor"] for r in rows if r["vendor"].strip()}
    return [
        {"metric": "rows", "value": len(rows)},
        {"metric": "vendors", "value": len(vendors)},
        {"metric": "valid_invoices", "value": len(valid)},
        {"metric": "skipped_invoices", "value": len(rows) - len(valid)},
        {"metric": "total_amount_excl_skipped", "value": round(sum(a for _, a in valid), 2)},
    ]


def data_quality_metrics(rows):
    total = len(rows)
    result = []
    for col in COLUMNS:
        missing = sum(1 for r in rows if not r[col].strip())
        result.append({"metric": f"missing_{col}", "value": missing, "pct": round(missing / total * 100, 2)})

    invalid = sum(
        1 for r in rows if r["amount"].strip() and parse_amount(r["amount"]) is None
    )
    skipped = sum(1 for r in rows if parse_amount(r["amount"]) is None)
    ids = [r["invoice_id"] for r in rows]
    result.append({"metric": "invalid_amount", "value": invalid, "pct": round(invalid / total * 100, 2)})
    result.append({"metric": "skip_rate", "value": skipped, "pct": round(skipped / total * 100, 2)})
    result.append({"metric": "duplicate_invoice_ids", "value": len(ids) - len(set(ids)), "pct": ""})
    return result


def amount_distribution(valid):
    amounts = sorted(a for _, a in valid)
    cuts = statistics.quantiles(amounts, n=100)
    q1, q3 = cuts[24], cuts[74]
    iqr = q3 - q1
    outliers = sum(1 for a in amounts if a < q1 - 1.5 * iqr or a > q3 + 1.5 * iqr)
    stats = {
        "mean": statistics.mean(amounts),
        "median": statistics.median(amounts),
        "min": amounts[0],
        "max": amounts[-1],
        "p25": q1,
        "p75": q3,
        "p90": cuts[89],
        "p99": cuts[98],
        "std_dev": statistics.stdev(amounts),
        "outliers_iqr": outliers,
    }
    return [{"metric": k, "value": round(v, 2)} for k, v in stats.items()]


def amount_bands(valid):
    rows = []
    for label, low, high in BANDS:
        in_band = [a for _, a in valid if low < a <= high or (low == 0 and a == 0)]
        rows.append({"band": label, "count": len(in_band), "total": round(sum(in_band), 2)})
    return rows


def approver_workload(valid):
    groups = defaultdict(list)
    for _, amount in valid:
        groups[get_approver(amount)].append(amount)
    return [
        {"approver": k, "count": len(v), "total": round(sum(v), 2)}
        for k, v in sorted(groups.items())
    ]


def status_breakdown(valid):
    groups = defaultdict(list)
    for row, amount in valid:
        groups[row["status"].strip() or "MISSING"].append(amount)
    rows = [
        {"status": k, "count": len(v), "total": round(sum(v), 2)}
        for k, v in sorted(groups.items())
    ]
    exposure = [a for s in ("PENDING", "REVIEW") for a in groups.get(s, [])]
    rows.append({"status": "PENDING+REVIEW (exposure)", "count": len(exposure), "total": round(sum(exposure), 2)})
    return rows


def vendor_summary(valid):
    groups = defaultdict(list)
    for row, amount in valid:
        groups[row["vendor"].strip() or "UNKNOWN"].append(amount)
    grand_total = sum(sum(v) for v in groups.values())
    rows = [
        {
            "vendor": k,
            "count": len(v),
            "total": round(sum(v), 2),
            "average": round(sum(v) / len(v), 2),
            "share_pct": round(sum(v) / grand_total * 100, 2),
        }
        for k, v in groups.items()
    ]
    return sorted(rows, key=lambda r: r["total"], reverse=True)


def main():
    try:
        rows = read_invoices(INPUT_FILE)
    except FileNotFoundError:
        print(f"File not found: {INPUT_FILE}")
        return

    valid = [(r, a) for r in rows if (a := parse_amount(r["amount"])) is not None]

    kpis = summary_kpis(rows, valid)
    print("Summary")
    for k in kpis:
        print(f"  {k['metric']}: {k['value']:,}" if isinstance(k["value"], (int, float)) else f"  {k['metric']}: {k['value']}")

    print("\nWriting metric files")
    write_csv("metrics_summary.csv", kpis, ["metric", "value"])
    write_csv("metrics_data_quality.csv", data_quality_metrics(rows), ["metric", "value", "pct"])
    write_csv("metrics_amount_distribution.csv", amount_distribution(valid), ["metric", "value"])
    write_csv("metrics_amount_bands.csv", amount_bands(valid), ["band", "count", "total"])
    write_csv("metrics_approver_workload.csv", approver_workload(valid), ["approver", "count", "total"])
    write_csv("metrics_status.csv", status_breakdown(valid), ["status", "count", "total"])
    write_csv(
        "metrics_vendor_summary.csv",
        vendor_summary(valid),
        ["vendor", "count", "total", "average", "share_pct"],
    )


main()
