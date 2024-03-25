# This application is only intended for use on Microsoft Windows(tm)
#
# Paper day use ticket logger for California State Parks
# that do not use R2S2.
#
# Created with Python 3.12.2
#
# Version a1.0.0.0
# 
# Created by Ryan Porter (github.com/PorterRyan). 
# Copyright 2024 Ryan Porter. This software is licensed under the GNU 
# General Public License version 3.0. Please see the COPYING file and copy
# of the GNU GPL v3.0 included with this software.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details. 
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see https://www.gnu.org/license/.

# Imports
from time import sleep
from datetime import datetime
import os, subprocess

# Park name. Edit for use in different state parks.
park_name = "Portola Redwoods State Park"

# Folder to save xreports in. Default is the Desktop.
xreport_folder = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + '\Desktop'

#Payment Function
def payment(method,ticket_price,qty):
    """ Payment calculator function.
    method: Payment method. 1 = Cash, 2 = Card, 3 = Check
    ticket_price: Ticket price for selected sale type.
    qty: Number of tickets being sold.
    """
    print("Running payment() now.")
    subtotal = int(ticket_price) * int(qty)
    if method == 1:
        try:
            print(f'Amount due: ${subtotal}.00')
            amt_received = float(input("Enter amount of cash received: "))
        except ValueError:
            amt_received = float(ticket_price)
        if amt_received == 0:
            amt_received = float(ticket_price)
        change = amt_received - subtotal
        if change != 0:
            print("Changed owed: $" + str(change))
            input("Press Enter when change given")
        return subtotal
    elif method == 2:
        return subtotal
    elif method == 3:
        check_num = input("Enter check number: ")
        return subtotal, check_num

def save_transaction(car_qty,payment_method,subtotal,check_num,vsa_name,ticket_type,ticket_num):
    """ Generate a transaction report.
    car_qty: Number of tickets being sold
    payment_method: Payment method (string). Use "Cash", "Card", or "Check"
    subtotal: Transaction total
    check_num: If paying by check, include the check number
    vsa_name: Name of service aide conducting the transaction
    ticket_type: Type of ticket (Day use, Senior, Disabled Discount)
    ticket_num: Current ticket number at start of transaction.
    """
    timestamp = str(datetime.now())
    car_qty = int(car_qty)
    ticket_list = []
    ticket_list.append(ticket_num)
    transaction_string = "===\n"
    transaction_string += f'{timestamp}\n'
    transaction_string += f'Ticket Type: {ticket_type}\n'
    if car_qty > 1: # Handle sales of more than one ticket at once.
        ticket_iter = 1
        while ticket_iter <= car_qty - 1:
            ticket_list.append(ticket_num + ticket_iter)
            ticket_iter += 1
        ticket_list_string = ""
        for ticket in ticket_list:
            ticket_list_string += str(ticket) + ', '
        ticket_list_string = ticket_list_string[:-2]
        transaction_string += f'Ticket numbers: {ticket_list_string}\n'
    else:
        transaction_string += f'Ticket number: {ticket_num}\n'
    print(ticket_list)
    transaction_string += f'Number of cars: {car_qty}\n'
    transaction_string += f'Payment method: {payment_method}\n'
    transaction_string += f'Subtotal: {subtotal}\n'
    if payment_method == "Check":
        transaction_string += f'Check Number: {check_num}\n'
    transaction_string += f'Service Aide: {vsa_name}\n'  
    transaction_string += "===\n\n"  
    return transaction_string

def ticket_validation(input_string):
    """Validate starting ticket number input.
    input_string: User input prompt
    """
    ticket_number = int()
    while True:
        try:
            ticket_number = int(input(input_string))
            return ticket_number
        except ValueError:
            print("Error: Invalid ticket number")
            print("Please enter a valid ticket number with no leading letters")
            continue

# Main function
def main():
    print(park_name)
    print("Day Use Recorder\n")
    print("""\nCopyright (c) 2021, 2023 Ryan Porter""")
    print("""
        This program is free software: You can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful, but
        WITHOUT ANY WARRANTY; without even the implied warranty of 
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
        General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program. If not, see https://www.gnu.org/licenses.

        Please note that this program uses Python modules that are covered
        under their own licenses. The license for Python itself, as well as
        its module time, os, subprocess, and datetime, can be found at https://docs.python.org/3/license.html.
        This software may have been compiled for use on
        Microsoft Windows systems using Nuitka, which is licensed under the
        Apache-2.0 license.

        You can contact the author of this program at github.com/PorterRyan.
        """)
    print("")
    sleep(3)
    os.system('cls')

    today = "{:%m-%d-%Y}".format(datetime.now())

    # Create XREPORT file
    xfilename = f"{xreport_folder}\\xreport_{today}.txt"
    vsa_name = input("Enter your name: ")
    starting_dayuse_ticket = ticket_validation("Enter starting day use ticket number without any leading letters: ")
    starting_senior_ticket = ticket_validation("Enter starting senior ticket number without any leading letters: ")
    starting_disabled_ticket = ticket_validation("Enter starting disabled ticket number without any leading letters: ")
    current_dayuse_ticket = int(starting_dayuse_ticket)
    current_senior_ticket = int(starting_senior_ticket)
    current_disabled_ticket = int(starting_disabled_ticket)
    total_cash = 0
    total_check = 0

    xfile_header = "Day Use Ticket Log\n"
    xfile_header += f'{today}\n'
    xfile_header += f'Employee: {vsa_name}\n\n'

    try:
        f = open(xfilename, 'x')
        f.close()
    # Make a new xreport file if one for today already exists
    except FileExistsError:
        print("File exists, starting new file...")
        count = 0
        for filename in os.listdir(xreport_folder):
            if filename.startswith(f"xreport_{today}"):
                count += 1
        xfilename = f"{xreport_folder}\\xreport_{today}-{str(count)}.txt"


    with open(xfilename, 'w') as xfile:
        xfile.write(xfile_header)
        xfile.close()

    os.system('cls')

    # Main Menu Loop
    menu = ""

    while menu != "q":
        print("Sale Mode")
        print(f"Current User: {vsa_name}")
        print("=========")
        menu = input("""
        Select a Menu Number:
        1: Day Use Sale
        2: Senior Day Use Sale
        3: Disabled Discount Day Use Sale
        4: Change current user
        5: Quit and Print XREPORT
        > """)

        match menu:
            case "1":
                os.system('cls')
                ticket_type = "Day Use"
                print("Day Use Ticket Sale")
                car_amt = int(input("Number of cars: "))
                ticket_price = 10
                payment_method = input("[1] Cash | [2] Card | [3] Check: ")
                match payment_method:
                    case "1":
                        print("Payment method: Cash")
                        payVars = payment(1, 10, car_amt)
                        print("payVars = " + str(payVars))
                        ticket_number = current_dayuse_ticket

                        # Save Report
                        transaction_report = save_transaction(car_amt,"Cash",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_dayuse_ticket += (1 * car_amt) 
                        total_cash += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

                    case "2":
                        print("Payment method: Card")
                        payVars = payment(2,10,car_amt)
                        ticket_number = current_dayuse_ticket
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Card",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_dayuse_ticket += (1 * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
                    case "3":
                        print("Payment method: Check")
                        payVars = payment(3,10,car_amt)
                        print("payVars = " + str(payVars))
                        ticket_number = current_dayuse_ticket
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Check",payVars[0],payVars[1],vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_dayuse_ticket += (1 * car_amt)
                        total_check += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
                        
            case "2":
                os.system('cls')
                ticket_price = 9
                ticket_type = "Senior Day Use"
                print("Senior Day Use Ticket Sale")
                car_amt = int(input("Number of cars: "))
                payment_method = input("[1] Cash | [2] Card | [3] Check: ")
                match payment_method:
                    case "1":
                        print("Payment method: Cash")
                        payVars = payment(1, ticket_price, car_amt)
                        print("payVars = " + str(payVars))
                        ticket_number = current_senior_ticket

                        # Save Report
                        transaction_report = save_transaction(car_amt,"Cash",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_senior_ticket += (1 * car_amt)
                        total_cash += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

                    case "2":
                        print("Payment method: Card")
                        payVars = payment(2,ticket_price,car_amt)
                        ticket_number = current_senior_ticket
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Card",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_senior_ticket += (1 * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
                    case "3":
                        print("Payment method: Check")
                        payVars = payment(3,ticket_price,car_amt)
                        print("payVars = " + str(payVars))
                        ticket_number = current_senior_ticket
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Check",payVars[0],payVars[1],vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_senior_ticket += (1 * car_amt)
                        total_check += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

            case "3":
                os.system('cls')
                ticket_price = 5
                ticket_type = "Disabled Day Use"
                print("Disabled Day Use Ticket Sale")
                car_amt = int(input("Number of cars: "))
                payment_method = input("[1] Cash | [2] Card | [3] Check: ")
                match payment_method:
                    case "1":
                        print("Payment method: Cash")
                        payVars = payment(1, ticket_price, car_amt)
                        print("payVars = " + str(payVars))
                        ticket_number = current_disabled_ticket

                        # Save Report
                        transaction_report = save_transaction(car_amt,"Cash",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_disabled_ticket += (1 * car_amt)
                        total_cash += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

                    case "2":
                        print("Payment method: Card")
                        payVars = payment(2,ticket_price,car_amt)
                        ticket_number = current_disabled_ticket
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Card",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_disabled_ticket += (1 * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
                    case "3":
                        print("Payment method: Check")
                        payVars = payment(3,ticket_price,car_amt)
                        print("payVars = " + str(payVars))
                        ticket_number = current_disabled_ticket
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Check",payVars[0],payVars[1],vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_disabled_ticket += (1 * car_amt)
                        total_check += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

            case "4":
                os.system('cls')
                print("Change Current Service Aide")
                vsa_name = input("Enter your name: ")

            case "5":
                final_dayuse_ticket = current_dayuse_ticket
                final_senior_ticket = current_senior_ticket
                final_disabled_ticket = current_disabled_ticket
                total_dayuse_sales = int(final_dayuse_ticket) - int(starting_dayuse_ticket)
                total_senior_sales = int(final_senior_ticket) - int(starting_senior_ticket)
                total_disabled_sales = int(final_disabled_ticket) - int(starting_disabled_ticket)

                xreport = "XREPORT\n"
                xreport += "=======\n"
                xreport += today + '\n'
                xreport += f'Starting Day Use Ticket: H{starting_dayuse_ticket}\n'
                xreport += f'Starting Senior Ticket: B{starting_senior_ticket}\n'
                xreport += f'Starting Disabled Ticket: A{starting_disabled_ticket}\n\n'
                xreport += f'Unsold Day Use Ticket: H{final_dayuse_ticket}\n'
                xreport += f'Unsold Senior Day Use Ticket: B{final_senior_ticket}\n'
                xreport += f'Unsold Disabled Day Use Ticket: A{final_disabled_ticket}\n\n'
                xreport += "DAILY TOTALS\n"
                xreport += "============\n"
                xreport += ""
                xreport += f'Total Day Use Sales: {total_dayuse_sales}\n'
                xreport += f'Total Senior Day Use Sales: {total_senior_sales}\n'
                xreport += f'Total Disabled Day Use Sales: {total_disabled_sales}\n'
                xreport += ""
                xreport += f'Total Cash: ${total_cash}.00'
                with open(xfilename, 'a') as xfile:
                    xfile.write(xreport)
                    xfile.close()
                os.system('cls')
                print(f'XReport saved in {xfilename}.')
                print('\n'.join(xreport.splitlines()[-19:]))
                print("")
                subprocess.run(["notepad",xfilename])
                input("Press 'Enter' when finished.")
                return

if __name__ == "__main__":
    main()