import tkinter as tk
from tkinter import ttk
import arrow
import csv
import calendar
import math

win = tk.Tk()
win.title("Budgeting App")

TAX_PERSONAL_ALLOWANCE = 456
TAX_BASE_LIMIT = 1327
TAX_HIGHER_LIMIT = 5770
NATIONAL_INSURANCE_ALLOWANCE = 324
TAX_BASE_RATE = 0.2
TAX_HIGHER_RATE = 0.4
TAX_ADDITIONAL_RATE = 0.45
NATIONAL_INSURANCE_RATE = 0.12
DAYS_BETWEEN_PAY = 14
SAVINGS = 200

exp = []
names = []
costs = []
dates = []


def radCall():
    pass


def taxCalc():

    money = int(pay.get())

    if money >= TAX_HIGHER_LIMIT:
        addTaxAmt = money - TAX_HIGHER_LIMIT
        higTaxAmt = TAX_HIGHER_LIMIT - TAX_BASE_LIMIT
        basTaxAmt = TAX_BASE_LIMIT - TAX_PERSONAL_ALLOWANCE
        tax = math.floor((addTaxAmt * TAX_ADDITIONAL_RATE) + (higTaxAmt * TAX_HIGHER_RATE) + (basTaxAmt * TAX_BASE_RATE))
    elif money >= TAX_BASE_LIMIT:
        higTaxAmt = money - TAX_BASE_LIMIT
        basTaxAmt = TAX_BASE_LIMIT - TAX_PERSONAL_ALLOWANCE
        tax = math.floor((higTaxAmt * TAX_HIGHER_RATE) + (basTaxAmt * TAX_BASE_RATE))
    elif money >= TAX_PERSONAL_ALLOWANCE:
        tax = math.floor(((money - TAX_PERSONAL_ALLOWANCE) * TAX_BASE_RATE))
    else:
        pass

    if money >= NATIONAL_INSURANCE_ALLOWANCE:
        NI = math.floor((money - NATIONAL_INSURANCE_ALLOWANCE) * NATIONAL_INSURANCE_RATE)
    else:
        pass

    money -= tax
    exp.append(['Tax', str(tax), str(money)])
    ttk.Label(win, text="Tax: £" + str(tax) + ", £" + str(money)).grid(column=0, row=8, columnspan=3)
    money -= NI
    exp.append(['National Insurance', str(NI), str(money)])
    ttk.Label(win, text='National Insurance: £' + str(NI) + ", £" + str(money)).grid(column=0, row=9, columnspan=3)

    save(money)


def restBudget(m):

    a = arrow.utcnow()
    month = a.month
    days = 0
    rent = 60

    with open('expenses.txt', 'r') as csvfile:
        readers = csv.reader(csvfile, delimiter=",")
        for row1 in readers:
            names.append(row1[0])
            costs.append(row1[1])
            dates.append(row1[2])

    rows = 10

    if (month == '2') and (a.year // 4) == 0:
        month = 'February2'
    elif month == '2':
        month = 'February1'
    else:
        month = calendar.month_name[month]
    print(month)

    with open('months.txt', 'r') as csvfile:
        readers = csv.reader(csvfile, delimiter=",")
        for row in readers:
            if row[0] == month:
                days = row[1]
            else:
                pass

    if int(date.get())+14 > int(days):
        daysend = int(days) - int(date.get())
        payday = DAYS_BETWEEN_PAY - daysend
        print(payday)

    x = 0
    days = int(days)
    while x != len(names):
        if int(date.get()) <= days:
            if int(dates[x]) - int(date.get()) >= 0:
                rows += 1
                m -= int(costs[x])
                ttk.Label(win, text=names[x] + ": £" + costs[x] + ", £" + str(m)).grid(column=0, row=rows, columnspan=3)
            else:
                pass
        else:
            daysend = days - int(date.get())
            payday = DAYS_BETWEEN_PAY - daysend
            print(payday)
            if dates[x] < 10:
                rows += 1
                m -= int(costs[x])
                ttk.Label(win, text=names[x] + ": £" + costs[x] + ", £" + str(m)).grid(column=0, row=rows, columnspan=3)
            else:
                pass
        x += 1

    m -= rent
    ttk.Label(win, text="Rent: £" + str(rent) + ", £" + str(m)).grid(column=0, row=rows + 1, columnspan=3)
    ttk.Label(win, text="Remaining Money: £" + str(m)).grid(column=0, row=7, columnspan=3)


def save(money):

    if savings.get() == 1:
        money -= SAVINGS
        exp.append(["Savings", str(SAVINGS), str(money)])
        print(exp)
        restBudget(money)
        ttk.Label(win, text="Savings: £" + str(SAVINGS) + ", £" + str(money)).grid(column=0, row=10, columnspan=3)
    else:
        restBudget(money)


# adding a label for instructions
ttk.Label(win, text="Enter Date number of the Pay Day").grid(column=0, row=0, columnspan=3)

# adding another entry for the date
date = tk.StringVar()
dateEntered = ttk.Entry(win, width=12, textvariable=date)
dateEntered.grid(column=0, row=1, columnspan=3)

radVar = tk.IntVar()
# Adding a radio button for a repeating paycheck
rad1 = tk.Radiobutton(win, text="Repeat Paycheck", variable=radVar, value=1, command=radCall)
rad1.grid(column=0, row=2, columnspan=3)

# Adding a Textbox Entry Widget to enter the amount
pay = tk.StringVar()
nameEntered = ttk.Entry(win, width=12, textvariable=pay)
nameEntered.grid(column=0, row=3, columnspan=3)

# Adding a check button for saving
savings = tk.IntVar()
check1 = tk.Checkbutton(win, text='Saving', variable=savings).grid(column=0, row=4, columnspan=3)

# Adding a button to workout the budget
working = ttk.Button(win, text="Workout the Budget", command=taxCalc).grid(column=0, row=6, columnspan=3)

win.mainloop()
