employees = [
    (101, "Alexander", 200000),
    (102, "Ravi", 150000),
    (103, "Priyanka", 300000),
    (104, "Christopher", 240000),
    (105, "Meera", 90000),
]

for emp_id, name, salary in employees:
    if len(name) > 6 and salary < 250000:
        print(name)
