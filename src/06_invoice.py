invoice_amount = 50000

# if / elif version
if invoice_amount > 50000:
    approver = "Manager and Director"
elif invoice_amount > 25000:
    approver = "Manager"
else:
    approver = "Supervisor"  # includes amount < 1000; 1000-25000 assumed Supervisor
print("if:", approver)

# match / case version (guards handle the ranges)
match invoice_amount:
    case amount if amount > 50000:
        approver = "Manager and Director"
    case amount if amount > 25000:
        approver = "Manager"
    case _:
        approver = "Supervisor"
print("match:", approver)
