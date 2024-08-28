# This application is only intended for use on Microsoft Windows(tm)
#
# Paper day use ticket logger for California State Parks
# that do not use R2S2.
#
# Created with Python 3.12.2
#
# Version 1.7.0
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

# TODO Reduce the number of lines in sale logs
# TODO Add accounting for Iron Ranger
# TODO Second roll variables need to be cast as int for counting

# Imports
from time import sleep
import datetime
import os, subprocess

# GLOBAL VARIABLES

# Park name. Edit for use in different state parks.
park_name = "Portola Redwoods State Park"

# Folder to save xreports in. Default is the Desktop.
xreport_folder = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + '\\Desktop'

def clear():
    _ = subprocess.call('cls', shell=True)

def adjust_ticket_numbers():
    """Adjust current ticket numbers
    """
    clear()
    print("Ticket Number Adjustment")
    print("========================")
    print("What type of ticket would you like to adjust?")
    ticket_type = input("[1] Day Use  [2] Senior  [3] Disabled [C]ancel: ")
    match ticket_type.upper():
        case "1":
            new_ticket = ticket_validation("Enter new current ticket number: ")
            current_dayuse_ticket = new_ticket[1]
            return "dayuse",current_dayuse_ticket
        case "2":
            new_ticket = ticket_validation("Enter new current senior ticket number: ")
            current_senior_ticket = new_ticket[1]
            return "senior",current_senior_ticket
        case "3":
            new_ticket = ticket_validation("Enter new current disabled ticket number: ")
            current_disabled_ticket = new_ticket[1]
            return "disabled",current_disabled_ticket
        case "C":
            print("Canceling...")
            return "canceled"

#Payment Function
def payment(method,ticket_price,qty):
    """ Payment calculator function.

    method: Payment method. 1 = Cash, 2 = Card, 3 = Check
    ticket_price: Ticket price for selected sale type.
    qty: Number of tickets being sold.
    """
    print("Running payment() now.")
    subtotal = float(ticket_price) * int(qty)
        
    if method == 1:
        try:
            print(f'Amount due: ${subtotal}0')
            amt_received = 0
            amt_received = float(input("Enter amount of cash received: "))
        except ValueError:
            amt_received = float(subtotal)
        if amt_received == 0:
            amt_received = float(subtotal)
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

def void_ticket():
    """ Void a day use ticket.
    """

    clear()
    ticket_type = input("Ticket Type: [1] Regular Day Use  [2] Senior Day Use  [3] Disabled Day Use:")
    ticket = ticket_validation("Ticket Number (no leading letters): ")
    ticket_number = ticket[1]
    ticket_letter = ticket[0]
    payment_method = input("Payment method used: [1] Cash  [2] Card  [3] Check")
    void_string = """====
    VOID
    ====

    """
    match ticket_type:
        
        case "1":
            print(f"Voiding ticket # {ticket_letter}{ticket_number}.")
            void_string += f"Ticket {ticket_letter}{ticket_number}\n"
            if payment_method == "1":
                total_cash -= 10
                void_string += f"Total Cash -$10.00\n"
            elif payment_method == "3":
                total_check -= 10
                void_string += f"Total Check -$10.00\n"
            else:
                print("Void credit transaction using credit card reader.")
            
        case "2":
            print(f"Voiding ticket # {ticket_letter}{ticket_number}.")
            void_string += f"Ticket {ticket_letter}{ticket_number}\n"
            if payment_method == "1":
                total_cash -= 9
                void_string += f"Total Cash -$9.00\n"
            elif payment_method == "3":
                total_check -= 9
                void_string += f"Total Check -$9.00\n"
            else:
                print("Void credit transaction using credit card reader.")

        case "3":
            print(f"Voiding ticket # {ticket_letter}{ticket_number}.")
            void_string += f"Ticket {ticket_letter}{ticket_number}\n"
            if payment_method == "1":
                total_cash -= 5
                void_string += f"Total Cash -$5.00\n"
            elif payment_method == "3":
                total_check -= 5
                void_string += f"Total Check -$5.00\n"
            else:
                print("Void credit transaction using credit card reader.")

    void_string += """========
    END VOID
    ========\n
    """

    return void_string

def sell_campsite(vsa_name,site_type,site_list):
    """Sell a walk-up campsite.
    vsa_name: Name of current VSA user.
    site_type: sr, reg, or dis for Senior, Regular, or Disabled campsites.
    """
    timestamp = str(datetime.datetime.now())
    reg_price = 35
    sr_price = 33
    dis_price = 17.5
    site_number = ""

    due_out = datetime.datetime.now() + datetime.timedelta(days=1)
    due_out = due_out.date()

    match site_type:
        case "reg": # Sell a regular campsite
            site_type = "Regular Campsite"
            site_price = reg_price
            print(f"Selling {site_type}")
            site_number_loop = True # Loop for simple input validation
            while site_number_loop:
                site_number = input("Enter site number: ")
                if site_number in site_list:
                    site_number_loop = False
                else:
                    print("Invalid site number!")
                    continue

            payment_type = input("[1] Cash  [2] Card  [3] Check: ")

            match payment_type:
                case "1":
                    payment_type = "Cash"
                    print("Payment method: Cash")
                    subtotal = payment(1,site_price,1)
                
                case "2":
                    payment_type = "Card"
                    print("Payment method: Card")
                    subtotal = payment(2,site_price,1)

                case "3":
                    payment_type = "Check"
                    print("Payment method: Check")
                    payVars = payment(3,site_price,1)
                    subtotal = payVars[0]
                    check_num = payVars[1]

        case "sr": # Sell a senior campsite
            site_type = "Senior Campsite"
            site_price = sr_price
            print(f"Selling {site_type}")
            site_number_loop = True # Loop for simple input validation
            while site_number_loop:
                site_number = input("Enter site number: ")
                if site_number in site_list:
                    site_number_loop = False
                else:
                    print("Invalid site number!")
                    continue

            payment_type = input("[1] Cash  [2] Card  [3] Check: ")

            match payment_type:
                case "1":
                    payment_type = "Cash"
                    print("Payment method: Cash")
                    subtotal = payment(1,site_price,1)
                
                case "2":
                    payment_type = "Card"
                    print("Payment method: Card")
                    subtotal = payment(2,site_price,1)

                case "3":
                    payment_type = "Check"
                    print("Payment method: Check")
                    payVars = payment(3,site_price,1)
                    subtotal = payVars[0]
                    check_num = payVars[1]
                    return 

        case "dis": # Sell a disabled campsite
            site_type = "Disabled Discount Campsite"
            site_price = dis_price
            print(f"Selling {site_type}")
            site_number_loop = True # Loop for simple input validation
            while site_number_loop:
                site_number = input("Enter site number: ")
                if site_number in site_list:
                    site_number_loop = False
                else:
                    print("Invalid site number!")
                    continue

            payment_type = input("[1] Cash  [2] Card  [3] Check: ")

            match payment_type:
                case "1":
                    payment_type = "Cash"
                    print("Payment method: Cash")
                    subtotal = payment(1,site_price,1)
                
                case "2":
                    payment_type = "Card"
                    print("Payment method: Card")
                    subtotal = payment(2,site_price,1)

                case "3":
                    payment_type = "Check"
                    print("Payment method: Check")
                    payVars = payment(3,site_price,1)
                    subtotal = payVars[0]
                    check_num = payVars[1]
    
    transaction_string = '''\
===
{timestamp}
Ticket type: {site_type}
Site number: {site_number}
Due out: {due_out}
Payment method: {payment_type}
\
'''.format(
    timestamp=timestamp,
    site_type=site_type,
    site_number=site_number,
    due_out=due_out,
    payment_type=payment_type)
    if payment_type == "Check":
        transaction_string += f"Check number: {check_num}\n"
    transaction_string += '''\
Subtotal: {0:.2f}
Service Aide: {vsa_name}
===\n
\
'''.format(subtotal,vsa_name=vsa_name)
    return transaction_string,site_type,payment_type,subtotal


def sell_annual_pass(vsa_name):
    """Sell Golden Poppy or California Explorer annual passes.
    vsa_name: Name of current VSA user.
    """
    poppy_price = 125
    explorer_price = 195
    month_abbr = ['Jan',
                  'Feb',
                  'Mar',
                  'Apr',
                  'May',
                  'Jun',
                  'Jul',
                  'Aug',
                  'Sep,'
                  'Oct',
                  'Nov',
                  'Dec']
    
    timestamp = datetime.datetime.now()
    pass_number = ""
    expiration_month = str(month_abbr[timestamp.month - 1])
    expiration_year = str(timestamp.year + 1)
    subtotal = int()
    check_num = False
    payment_type = ""

    clear()
    pass_loop = True
    while pass_loop: # Loop for simple input validation
        pass_type = input(
            """Select annual pass type:
            [1] Golden Poppy Pass  [2] California Explorer Pass
            > """)
        if pass_type == "1" or pass_type == "2":
            pass_loop = False
        else:
            continue
    
    match pass_type:
        case "1":
            pass_type = "Golden Poppy"
            print(f"Selling {pass_type} Pass")
            cancel_sale = input('If you wish to cancel, enter "Q", otherwise, just press "Enter": ')
            if cancel_sale.upper() == "Q":
                return
            
            pass_number_loop = True # Loop for simple input validation
            while pass_number_loop:
                pass_number = input("Enter the last six digits of the pass number: ")
                if len(pass_number) == 6:
                    pass_number_loop = False
                else:
                    print("Invalid pass number!")
                    continue
            payment_type = input("[1] Cash  [2] Card  [3] Check: ")

            match payment_type:
                case "1":
                    payment_type = "Cash"
                    print("Payment method: Cash")
                    subtotal = payment(1,poppy_price,1)
                
                case "2":
                    payment_type = "Card"
                    print("Payment method: Card")
                    subtotal = payment(2,poppy_price,1)

                case "3":
                    payment_type = "Check"
                    print("Payment method: Check")
                    payVars = payment(3,poppy_price,1)
                    subtotal = payVars[0]
                    check_num = payVars[1]
        
        case "2":
            pass_type = "California Explorer"
            print(f"Selling {pass_type} Pass")
            cancel_sale = input('If you wish to cancel, enter "Q", otherwise, just press "Enter": ')
            if cancel_sale.upper() == "Q":
                return
            
            pass_number_loop = True # Loop for simple input validation
            while pass_number_loop:
                pass_number = input("Enter the last six digits of the pass number: ")
                if len(pass_number) == 6:
                    pass_number_loop = False
                else:
                    print("Invalid pass number!")
                    continue

            payment_type = input("[1] Cash  [2] Card  [3] Check: ")

            match payment_type:
                case "1":
                    payment_type = "Cash"
                    print("Payment method: Cash")
                    subtotal = payment(1,explorer_price,1)
                
                case "2":
                    payment_type = "Card"
                    print("Payment method: Card")
                    subtotal = payment(2,explorer_price,1)

                case "3":
                    payment_type = "Check"
                    print("Payment method: Check")
                    payVars = payment(3,explorer_price,1)
                    subtotal = payVars[0]
                    check_num = payVars[1]
    
    transaction_string = '''\
===
{timestamp}
Ticket type: {pass_type}
Pass number: {pass_number}
Expiration month: {month}
Expiration year: {year}
Quantity: 1
Payment method: {payment_type}
\
'''.format(
    timestamp=timestamp,
    pass_type=pass_type,
    pass_number=pass_number,
    payment_type=payment_type,
    month=expiration_month,
    year=expiration_year)
    if payment_type == "Check":
        transaction_string += f"Check number: {check_num}\n"
    transaction_string += '''\
Subtotal: {0:.2f}
Service Aide: {vsa_name}
===\n
\
'''.format(subtotal,vsa_name=vsa_name)
    return transaction_string,pass_type,payment_type,subtotal

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
    timestamp = str(datetime.datetime.now())
    car_qty = int(car_qty)
    ticket_list = []
    ticket_list.append(ticket_num)
    transaction_string = "===\n"
    transaction_string += f'{timestamp}\n'
    transaction_string += f'Ticket type: {ticket_type}\n'
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
    transaction_string += f'Subtotal: {subtotal:.2f}\n'
    if payment_method == "Check":
        transaction_string += f'Check Number: {check_num}\n'
    transaction_string += f'Service Aide: {vsa_name}\n'  
    transaction_string += "===\n\n"  
    return transaction_string

def ticket_validation(input_string):
    """Validate starting ticket number input.

    input_string: User input prompt
    """

    while True:
        ticket = input(input_string)
        if len(ticket) > 6:
            if not ticket[0].isdigit():
                letter = ticket[0]
                ticket_number = ticket[1:len(ticket)]
                return letter, ticket_number
            else:
                print(ticket)
                print("Error: Invalid ticket number.")
                print("Please enter a valid ticket number. Valid numbers appear like the following:")
                print("C2083816")
                print("Use the starting letter on your ticket.")
                continue
        print("Error: Invalid ticket number.")
        print("Please enter a valid ticket number. Valid numbers appear like the following:")
        print("C2083816")
        print("Use the starting letter on your ticket.")
        continue

    #ticket_number = int()
    #while True:
    #    try:
    #        ticket_number = int(input(input_string))
    #        return ticket_number
    #    except ValueError:
    #        print("Error: Invalid ticket number")
    #        print("Please enter a valid ticket number with no leading letters.")
    #        continue

# Main function
def main():
    print(park_name)
    print("Day Use Recorder\n")
    print("""\nCopyright (c) 2024 Ryan Porter""")
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
        its module time, os, subprocess, and datetime, can be found at 
        https://docs.python.org/3/license.html. This software may have been 
        compiled for use on Microsoft Windows systems using Nuitka, which is 
        licensed under the Apache-2.0 license.

        You can contact the author of this program at github.com/PorterRyan.
        """)
    print("")
    sleep(3)
    clear()

    today = "{:%m-%d-%Y}".format(datetime.datetime.now())

    site_list = ("2",
                 "3",
                 "4",
                 "5",
                 "6",
                 "7",
                 "8",
                 "9",
                 "10",
                 "11",
                 "12",
                 "13",
                 "14",
                 "15",
                 "16",
                 "17",
                 "18",
                 "19",
                 "20",
                 "21",
                 "22",
                 "23",
                 "24",
                 "25",
                 "26",
                 "27",
                 "28",
                 "29",
                 "30",
                 "31",
                 "32",
                 "33",
                 "34",
                 "35",
                 "36",
                 "37",
                 "38",
                 "39",
                 "40",
                 "41",
                 "42",
                 "43",
                 "44",
                 "45",
                 "46",
                 "47",
                 "48",
                 "49",
                 "50",
                 "51",
                 "52",
                 "53",
                 "61",
                 "62",
                 "63",
                 "64",
                 "C",
                 "H",
                 "R",
                 "P",
                 "TC")

    # Create XREPORT file
    xfilename = f"{xreport_folder}\\xreport_{today}.txt"
    vsa_name = input("Enter your name: ")
    dayuse_tickets = ticket_validation("Enter starting day use ticket number: ")
    senior_tickets = ticket_validation("Enter starting senior ticket number: ")
    disabled_tickets = ticket_validation("Enter starting disabled ticket number: ")

    starting_dayuse_ticket = dayuse_tickets[1]
    starting_senior_ticket = senior_tickets[1]
    starting_disabled_ticket = disabled_tickets[1]

    current_dayuse_ticket = int(starting_dayuse_ticket)
    current_senior_ticket = int(starting_senior_ticket)
    current_disabled_ticket = int(starting_disabled_ticket)

    dayuse_letter = dayuse_tickets[0]
    senior_letter = senior_tickets[0]
    disabled_letter = disabled_tickets[0]

    dayuse_roll_2_letter = ""
    dayuse_roll_2_starting_number = 0
    current_dayuse_ticket_2 = 0

    senior_roll_2_letter = ""
    senior_roll_2_starting_number = 0
    current_senior_ticket_2 = 0

    disabled_roll_2_letter = ""
    disabled_roll_2_starting_number = 0
    current_disabled_ticket_2 = 0

    # Amount Totals
    total_cash = 0
    total_card = 0
    total_check = 0

    # Annual Pass Counters
    total_golden_poppy = 0
    total_california_explorer = 0

    # Camping Counters
    total_regular_campsite = 0
    total_senior_campsite = 0
    total_disabled_campsite = 0
    total_xv = 0
    total_hb = 0
    total_tc = 0

    # Other Counters
    total_small_buses = 0
    total_large_buses = 0

    # X-Report Header
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

    clear()

    # Main Menu Loop
    menu = ""

    while menu != "q":
        clear()
        print("Sale Mode")
        print(f"Current User: {vsa_name}")
        print("=========")
        menu = input("""
        Select a Menu Number:
        1: Day Use Sale
        2: Senior Day Use Sale
        3: Disabled Discount Day Use Sale
        4: Annual Pass Sale
        5: Small/Large Bus Pass Sale
        6: Regular Campsite
        7: Senior Campsite
        8: Disabled Discount Campsite
        9: Extra Vehicle
        10: Trail Camp
        11: Hike/Bike
        12: Change current user
        13: Change current ticket numbers
        14: Switch to a new ticket roll
        15: Display Current Ticket Numbers
        16: Void a Ticket Sale (experimental)
        X: Quit and Print XREPORT
        > """)

        match menu.upper():
            case "1": # Sell day use passes
                clear()
                ticket_type = "Day Use"
                print("Day Use Ticket Sale")
                #Confirm or cancel sale
                cancel = input("Continue with sale? Y/N: ")
                if cancel.upper() == "N":
                    continue
                car_amt = int(input("Number of cars: "))
                ticket_price = float(10.00)
                payment_method = input("[1] Cash | [2] Card | [3] Check | [Q] Cancel: ")
                match payment_method.upper():
                    case "1":
                        print("Payment method: Cash")
                        payVars = payment(1, 10, car_amt)
                        #print("payVars = " + str(payVars))

                        if int(current_dayuse_ticket_2) == 0: # check if we are on a second roll
                            ticket_number = current_dayuse_ticket
                        elif int(current_dayuse_ticket_2) > 0:
                            ticket_number = int(current_dayuse_ticket_2)

                        # Save Report
                        transaction_report = save_transaction(car_amt,"Cash",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if int(current_dayuse_ticket_2) == 0: # Check if we are on a second roll
                            current_dayuse_ticket += (1 * car_amt)
                        elif int(current_dayuse_ticket_2) > 0:
                            current_dayuse_ticket_2 += (1 * car_amt)
                        total_cash += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

                    case "2":
                        print("Payment method: Card")
                        payVars = payment(2,10,car_amt)
                        if current_dayuse_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_dayuse_ticket
                        elif current_dayuse_ticket_2 > 0:
                            ticket_number = current_dayuse_ticket_2
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Card",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_dayuse_ticket_2 == 0:
                            current_dayuse_ticket += (1 * car_amt)
                        elif current_dayuse_ticket_2 > 0:
                            current_dayuse_ticket_2 += (1 * car_amt)
                        total_card += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
                    case "3":
                        print("Payment method: Check")
                        payVars = payment(3,10,car_amt)
                        if current_dayuse_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_dayuse_ticket
                        elif current_dayuse_ticket_2 > 0:
                            ticket_number = current_dayuse_ticket_2
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Check",payVars[0],payVars[1],vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_dayuse_ticket_2 == 0:
                            current_dayuse_ticket += (1 * car_amt)
                        elif current_dayuse_ticket_2 > 0:
                            current_dayuse_ticket_2 += (1 * car_amt)
                        total_check += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
                    
                    case "Q":
                        continue
                    
                    case _:
                        print("Payment method: Cash")
                        payVars = payment(1, 10, car_amt)
                        if current_dayuse_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_dayuse_ticket
                        elif current_dayuse_ticket_2 > 0:
                            ticket_number = current_dayuse_ticket_2

                        # Save Report
                        transaction_report = save_transaction(car_amt,"Cash",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_dayuse_ticket_2 == 0:
                            current_dayuse_ticket += (1 * car_amt)
                        elif current_dayuse_ticket_2 > 0:
                            current_dayuse_ticket_2 += (1 * car_amt)
                        total_cash += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
                        
            case "2":
                clear()
                ticket_price = float(9.00)
                ticket_type = "Senior Day Use"
                print("Senior Day Use Ticket Sale")
                #Confirm or cancel sale
                cancel = input("Continue with sale? Y/N: ")
                if cancel.upper() == "N":
                    continue
                car_amt = int(input("Number of cars: "))
                payment_method = input("[1] Cash | [2] Card | [3] Check | [Q] Cancel: ")
                match payment_method:
                    case "1":
                        print("Payment method: Cash")
                        payVars = payment(1, ticket_price, car_amt)
                        #print("payVars = " + str(payVars))
                        if current_senior_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_senior_ticket
                        elif current_senior_ticket_2 > 0:
                            ticket_number = current_senior_ticket_2

                        # Save Report
                        transaction_report = save_transaction(car_amt,"Cash",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_senior_ticket_2 == 0: # Check if we are on a second roll
                            current_senior_ticket += (1 * car_amt)
                        elif current_senior_ticket_2 > 0:
                            current_senior_ticket_2 += (1 * car_amt)
                        total_cash += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

                    case "2":
                        print("Payment method: Card")
                        payVars = payment(2,ticket_price,car_amt)
                        if current_senior_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_senior_ticket
                        elif current_senior_ticket_2 > 0:
                            ticket_number = current_senior_ticket_2
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Card",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_senior_ticket_2 == 0: # Check if we are on a second roll
                            current_senior_ticket += (1 * car_amt)
                        elif current_senior_ticket_2 > 0:
                            current_senior_ticket_2 += (1 * car_amt)
                        total_card += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
                    case "3":
                        print("Payment method: Check")
                        payVars = payment(3,ticket_price,car_amt)
                        #print("payVars = " + str(payVars))
                        if current_senior_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_senior_ticket
                        elif current_senior_ticket_2 > 0:
                            ticket_number = current_senior_ticket_2
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Check",payVars[0],payVars[1],vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_senior_ticket_2 == 0: # Check if we are on a second roll
                            current_senior_ticket += (1 * car_amt)
                        elif current_senior_ticket_2 > 0:
                            current_senior_ticket_2 += (1 * car_amt)
                        total_check += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

                    case "Q":
                        continue
                    
                    case _:
                        print("Payment method: Cash")
                        payVars = payment(1, ticket_price, car_amt)
                        #print("payVars = " + str(payVars))
                        if current_senior_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_senior_ticket
                        elif current_senior_ticket_2 > 0:
                            ticket_number = current_senior_ticket_2

                        # Save Report
                        transaction_report = save_transaction(car_amt,"Cash",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_senior_ticket_2 == 0: # Check if we are on a second roll
                            current_senior_ticket += (1 * car_amt)
                        elif current_senior_ticket_2 > 0:
                            current_senior_ticket_2 += (1 * car_amt)
                        total_cash += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

            case "3": # Sell Disabled Day Use Passes
                clear()
                ticket_price = float(5.00)
                ticket_type = "Disabled Day Use"
                print("Disabled Day Use Ticket Sale")
                #Confirm or cancel sale
                cancel = input("Continue with sale? Y/N: ")
                if cancel.upper() == "N":
                    continue
                car_amt = int(input("Number of cars: "))
                payment_method = input("[1] Cash | [2] Card | [3] Check | [Q] Cancel: ")
                match payment_method:
                    case "1":
                        print("Payment method: Cash")
                        payVars = payment(1, ticket_price, car_amt)
                        #print("payVars = " + str(payVars))
                        if current_disabled_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_disabled_ticket
                        elif current_disabled_ticket_2 > 0:
                            ticket_number = current_disabled_ticket_2

                        # Save Report
                        transaction_report = save_transaction(car_amt,"Cash",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_disabled_ticket_2 == 0: # Check if we are on a second roll
                            current_disabled_ticket += (1 * car_amt)
                        elif current_disabled_ticket_2 > 0:
                            current_disabled_ticket_2 += (1 * car_amt)
                        total_cash += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

                    case "2":
                        print("Payment method: Card")
                        payVars = payment(2,ticket_price,car_amt)
                        if current_disabled_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_disabled_ticket
                        elif current_disabled_ticket_2 > 0:
                            ticket_number = current_disabled_ticket_2
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Card",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_disabled_ticket_2 == 0: # Check if we are on a second roll
                            current_disabled_ticket += (1 * car_amt)
                        elif current_disabled_ticket_2 > 0:
                            current_disabled_ticket_2 += (1 * car_amt)
                        total_card += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
                    case "3":
                        print("Payment method: Check")
                        payVars = payment(3,ticket_price,car_amt)
                        #print("payVars = " + str(payVars))
                        if current_disabled_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_disabled_ticket
                        elif current_disabled_ticket_2 > 0:
                            ticket_number = current_disabled_ticket_2
                        # SAVE TRANSACTION
                        transaction_report = save_transaction(car_amt,"Check",payVars[0],payVars[1],vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        current_disabled_ticket += (1 * car_amt)
                        total_check += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()

                    case "Q":
                        continue

                    case _:
                        print("Payment method: Cash")
                        payVars = payment(1, ticket_price, car_amt)
                        #print("payVars = " + str(payVars))
                        if current_disabled_ticket_2 == 0: # check if we are on a second roll
                            ticket_number = current_disabled_ticket
                        elif current_disabled_ticket_2 > 0:
                            ticket_number = current_disabled_ticket_2

                        # Save Report
                        transaction_report = save_transaction(car_amt,"Cash",payVars,0,vsa_name,ticket_type,ticket_number)
                        print(transaction_report)
                        if current_disabled_ticket_2 == 0: # Check if we are on a second roll
                            current_disabled_ticket += (1 * car_amt)
                        elif current_disabled_ticket_2 > 0:
                            current_disabled_ticket_2 += (1 * car_amt)
                        total_cash += (ticket_price * car_amt)
                        with open(xfilename, 'a') as xfile:
                            xfile.write(transaction_report)
                            xfile.close()
            
            case "4": # Sell annual pass
                saleVars = sell_annual_pass(vsa_name)
                transaction_report = saleVars[0]
                pass_type = saleVars[1]
                payment_method = saleVars[2]
                subtotal = saleVars[3]
                if payment_method == "Cash":
                    total_cash += subtotal
                elif payment_method == "Card":
                    total_card += subtotal
                elif payment_method == "Check":
                    total_check += subtotal
                
                if pass_type == "Golden Poppy":
                    total_golden_poppy += 1
                elif pass_type == "California Explorer":
                    total_california_explorer += 1

                with open(xfilename,'a') as xfile:
                    xfile.write(transaction_report)
                    xfile.close()
                    
            case "5": # Small/Large Bus Passes
                clear()
                print("Bus Day Use Ticket Sale")
                #Confirm or cancel sale
                cancel = input("Continue with sale? Y/N: ")
                if cancel.upper() == "N":
                    continue
                ticket_type = ""

                bus_size = input("[S]mall or [L]arge bus: ")
                match bus_size.upper():
                    case "S":
                        ticket_type = "Small Bus"
                        ticket_price = float(50.00)
                        payment_method = input("[1] Cash | [2] Card | [3] check | [Q] Cancel: ")
                        match payment_method.upper():
                            case "1":
                                print("Payment method: Cash")
                                payVars = payment(1,ticket_price,1)
                                # No ticket numbers for buses

                                # Save Report
                                transaction_report = save_transaction(1,"Cash",payVars,0,vsa_name,ticket_type,"N/A")
                                print(transaction_report)
                                total_cash += ticket_price
                                total_small_buses += 1
                                with open(xfilename, 'a') as xfile:
                                    xfile.write(transaction_report)
                                    xfile.close()
                            case "2":
                                print("Payment Method: Card")
                                payVars = payment(2,ticket_price,1)
                                # No ticket numbers for buses
                                # Save Report
                                transaction_report = save_transaction(1,"Card",payVars,0,vsa_name,ticket_type,"N/A")
                                print(transaction_report)
                                total_small_buses += 1
                                total_card += ticket_price
                                with open(xfilename, 'a') as xfile:
                                    xfile.write(transaction_report)
                                    xfile.close()
                            case "3":
                                print("Payment Method: Check")
                                payVars = payment(3,ticket_price,1)
                                # No ticket numbers for buses
                                # Save Report
                                transaction_report = save_transaction(1,3,payVars[0],payVars[1],vsa_name,ticket_type,"N/A")
                                print(transaction_report)
                                total_check += ticket_price
                                with open(xfilename, 'a') as xfile:
                                    xfile.write(transaction_report)
                                    xfile.close()
                            case "Q":
                                continue
                    case "L":
                        ticket_type = "Large Bus"
                        ticket_price = float(100.00)
                        payment_method = input("[1] Cash | [2] Card | [3] check | [Q] Cancel: ")
                        match payment_method.upper():
                            case "1":
                                print("Payment method: Cash")
                                payVars = payment(1,ticket_price,1)
                                # No ticket numbers for buses

                                # Save Report
                                transaction_report = save_transaction(1,"Cash",payVars,0,vsa_name,ticket_type,"N/A")
                                print(transaction_report)
                                total_cash += ticket_price
                                total_small_buses += 1
                                with open(xfilename, 'a') as xfile:
                                    xfile.write(transaction_report)
                                    xfile.close()
                            case "2":
                                print("Payment Method: Card")
                                payVars = payment(2,ticket_price,1)
                                # No ticket numbers for buses
                                # Save Report
                                transaction_report = save_transaction(1,"Card",payVars,0,vsa_name,ticket_type,"N/A")
                                print(transaction_report)
                                total_small_buses += 1
                                total_card += ticket_price
                                with open(xfilename, 'a') as xfile:
                                    xfile.write(transaction_report)
                                    xfile.close()
                            case "3":
                                print("Payment Method: Check")
                                payVars = payment(3,ticket_price,1)
                                # No ticket numbers for buses
                                # Save Report
                                transaction_report = save_transaction(1,3,payVars[0],payVars[1],vsa_name,ticket_type,"N/A")
                                print(transaction_report)
                                total_check += ticket_price
                                with open(xfilename, 'a') as xfile:
                                    xfile.write(transaction_report)
                                    xfile.close()
                            case "Q":
                                continue
                    case _:
                        print('Please enter "S" for a small bus or "L" for a large bus.')

            case "6": # Regular Campsite
                clear()
                print("Regular Walk-up Campsite Sale")
                confirm = input("Confirm sale of regular campsite? Y/N: ")
                if confirm.upper() == "N":
                    continue
                saleVars = sell_campsite(vsa_name,"reg",site_list)
                transaction_report = saleVars[0]
                site_type = saleVars[1]
                payment_method = saleVars[2]
                subtotal = saleVars[3]
                if payment_method == "Cash":
                    total_cash += subtotal
                elif payment_method == "Card":
                    total_card += subtotal
                elif payment_method == "Check":
                    total_check += subtotal
                total_regular_campsite += 1

                with open(xfilename, 'a') as xfile:
                    xfile.write(transaction_report)
                    xfile.close()

            case "7": # Senior Campsite
                clear()
                print("Senior Walk-up Campsite Sale")
                confirm = input("Confirm sale of senior campsite? Y/N: ")
                if confirm.upper() == "N":
                    continue
                saleVars = sell_campsite(vsa_name,"sr",site_list)
                transaction_report = saleVars[0]
                site_type = saleVars[1]
                payment_method = saleVars[2]
                subtotal = saleVars[3]
                if payment_method == "Cash":
                    total_cash += subtotal
                elif payment_method == "Check":
                    total_check += subtotal
                total_senior_campsite += 1

                with open(xfilename, 'a') as xfile:
                    xfile.write(transaction_report)
                    xfile.close()

            case "8": # Disabled Discount Campsite
                clear()
                print("Disabled Discount Walk-up Campsite Sale")
                confirm = input("Confirm sale of disabled discount campsite? Y/N: ")
                if confirm.upper() == "N":
                    continue
                saleVars = sell_campsite(vsa_name,"dis")
                transaction_report = saleVars[0]
                site_type = saleVars[1]
                payment_method = saleVars[2]
                subtotal = saleVars[3]
                if payment_method == "Cash":
                    total_cash += subtotal
                elif payment_method == "Card":
                    total_card += subtotal
                elif payment_method == "Check":
                    total_check += subtotal
                total_disabled_campsite += 1

                with open(xfilename, 'a') as xfile:
                    xfile.write(transaction_report)
                    xfile.close()

            case "9": # Extra Vehicle Sales
                timestamp = str(datetime.datetime.now())
                xv_price = 10
                print("Selling Extra Vehicle")
                #Confirm or cancel sale
                cancel = input("Continue with sale? Y/N: ")
                if cancel.upper() == "N":
                    continue
                site_number_loop = True # Loop for simple input validation
                while site_number_loop:
                    site_number = input("""
Enter site number or first letter of group site name (C, H, R, P) below.
Enter "TC" for Trail Camp extra vehicles. 
> """)
                    if site_number.upper() in site_list:
                        site_number_loop = False
                    else:
                        print("Invalid site number!")
                        continue
                nights = input("Number of nights: ")
                due_out = datetime.datetime.now() + datetime.timedelta(days=int(nights))
                due_out = due_out.date()
                payment_type = input("[1] Cash  [2] Card  [3] Check: ")

                match payment_type:
                    case "1":
                        payment_type = "Cash"
                        print("Payment method: Cash")
                        subtotal = payment(1,xv_price,nights)
                
                    case "2":
                        payment_type = "Card"
                        print("Payment method: Card")
                        subtotal = payment(2,xv_price,nights)

                    case "3":
                        payment_type = "Check"
                        print("Payment method: Check")
                        payVars = payment(3,xv_price,nights)
                        subtotal = payVars[0]
                        check_num = payVars[1]
                site_number = site_number.upper()
                transaction_string = '''\
===
{timestamp}
Ticket type: Extra Vehicle
Site number: {site_number}
Due Out: {due_out}
Number of nights: {nights}
Payment method: {payment_type}
\
'''.format(timestamp=timestamp,site_number=site_number,due_out=due_out,nights=nights,payment_type=payment_type)
                if payment_type == "Check":
                    transaction_string += f"Check number: {check_num}\n"
                    total_check += subtotal
                elif payment_type == "Cash":
                    total_cash += subtotal
                elif payment_type == "Card":
                    total_card += subtotal
                transaction_string += '''\
Subtotal: {0:.2f}
Service Aide: {vsa_name}
===\n
\
'''.format(subtotal,vsa_name=vsa_name)
                total_xv += 1
                with open(xfilename, 'a') as xfile:
                    xfile.write(transaction_string)
                    xfile.close()

            case "10": # Trail Camp Sales
                timestamp = str(datetime.datetime.now())
                tr_price = 15
                res_fee = 8
                total_price = tr_price + res_fee
                print("Selling Trail Camp")
                print("ONE NIGHT ONLY!")
                print("Additional nights require a reservation from")
                print("parks.ca.gov/scmtrailcamps")
                trail_camp = "Slate Creek"

                payment_type = input("[1] Cash  [2] Card  [3] Check: ")

                match payment_type:
                    case "1":
                        payment_type = "Cash"
                        print("Payment method: Cash")
                        subtotal = payment(1,total_price,1)
                
                    case "2":
                        payment_type = "Card"
                        print("Payment method: Card")
                        subtotal = payment(2,total_price,1)

                    case "3":
                        payment_type = "Check"
                        print("Payment method: Check")
                        payVars = payment(3,total_price,1)
                        subtotal = payVars[0]
                        check_num = payVars[1]
                        transaction_string = '''\
===
{timestamp}
Ticket type: Trail Camp
Trail Camp: {trail_camp}
Payment method: {payment_type}
\
'''.format(timestamp=timestamp,payment_type=payment_type,trail_camp=trail_camp)
                if payment_type == "Check":
                    transaction_string += f"Check number: {check_num}\n"
                    total_check += subtotal
                elif payment_type == "Cash":
                    total_cash += subtotal
                elif payment_type == "Card":
                    total_card += subtotal
                transaction_string += '''\
Camping Fee: {tr_price}
Reservation Fee: {res_fee}
Subtotal: {0:.2f}
Service Aide: {vsa_name}
===\n
\
'''.format(tr_price,res_fee,subtotal,vsa_name=vsa_name)
                total_tc += 1
                with open(xfilename, 'a') as xfile:
                    xfile.write(transaction_string)
                    xfile.close()
                
            case "11": # Hike/Bike
                timestamp = str(datetime.datetime.now())
                hb_price = 5
                qty = int(0)
                print("Selling Hike/Bike Camping")
                print("$5 per person per night")
                campers = input("How many campers? ")
                nights = input("How many nights? ")
                qty = int(campers) + int(nights)

                payment_type = input("[1] Cash  [2] Card  [3] Check: ")

                match payment_type:
                    case "1":
                        payment_type = "Cash"
                        print("Payment method: Cash")
                        subtotal = payment(1,hb_price,qty)
                
                    case "2":
                        payment_type = "Card"
                        print("Payment method: Card")
                        subtotal = payment(2,hb_price,qty)

                    case "3":
                        payment_type = "Check"
                        print("Payment method: Check")
                        payVars = payment(3,hb_price,qty)
                        subtotal = payVars[0]
                        check_num = payVars[1]
                        transaction_string = '''\
===
{timestamp}
Ticket type: Hike/Bike
Payment method: {payment_type}
\
'''.format(timestamp=timestamp,payment_type=payment_type)
                if payment_type == "Check":
                    transaction_string += f"Check number: {check_num}\n"
                    total_check += subtotal
                elif payment_type == "Cash":
                    total_cash += subtotal
                elif payment_type == "Card":
                    total_card += subtotal
                transaction_string += '''\
Camping Fee: {hb_price}
Subtotal: {0:.2f}
Service Aide: {vsa_name}
===\n
\
'''.format(hb_price,subtotal,vsa_name=vsa_name)
                total_hb += qty
                with open(xfilename, 'a') as xfile:
                    xfile.write(transaction_string)
                    xfile.close()


            case "12": # Change the Service Aide Name
                clear()
                print("Change Current Service Aide")
                vsa_name = input("Enter your name: ")

            case "13": # Change the current ticket number
                change_results = adjust_ticket_numbers()
                ticket_type = change_results[0]
                new_number = change_results[1]
                if ticket_type == "canceled":
                    continue
                elif ticket_type == "dayuse":
                    current_dayuse_ticket = new_number
                elif ticket_type == "senior":
                    current_senior_ticket = new_number
                elif ticket_type == "disabled":
                    current_disabled_ticket = new_number
            
            case "14": # Switch to a new roll of tickets
                clear()
                print("Replace Ticket Roll")
                print("===================")
                print("")
                roll_type = input("Select a roll to replace: [1] Day use | [2] Senior | [3] Disabled | [C] Cancel: ")
                match roll_type.upper():
                    case "1": # replace a roll of dayuse tickets
                        new_ticket = ticket_validation("Enter the first ticket number of the new roll: ")
                        print(new_ticket[1])
                        dayuse_roll_2_letter = new_ticket[0]
                        dayuse_roll_2_starting_number = new_ticket[1]
                        current_dayuse_ticket_2 = dayuse_roll_2_starting_number
                    case "2": # Replace a roll of senior tickets
                        new_ticket = ticket_validation("Enter the first ticket number of the new roll: ")
                        senior_roll_2_letter = new_ticket[0]
                        senior_roll_2_starting_number = new_ticket[1]
                        current_senior_ticket_2 = senior_roll_2_starting_number
                    case "3": # Replace a roll of disabled tickets
                        new_ticket = ticket_validation("Enter the first ticket number of the new roll: ")
                        disabled_roll_2_letter = new_ticket[0]
                        disabled_roll_2_starting_number = new_ticket[1]
                        current_disabled_ticket_2 = disabled_roll_2_starting_number
                    case "C":
                        continue

            case "15": # Display current ticket numbers
                clear()
                print("""Current Ticket Numbers
                ======================""")
                if dayuse_roll_2_starting_number == 0:
                    print(f"Current Day Use Ticket: {dayuse_letter}{current_dayuse_ticket}")
                    print(f"Total Day Use Sales: {int(current_dayuse_ticket) - int(starting_dayuse_ticket)}\n")
                else:
                    print(f'Current Day Use Ticket: {dayuse_roll_2_letter}{current_dayuse_ticket_2}')
                    total_dayuse_sales = (int(current_dayuse_ticket) - int(starting_dayuse_ticket)) + (int(current_dayuse_ticket_2) - int(dayuse_roll_2_starting_number))
                    print(f'Total Day Use Sales: {total_dayuse_sales}\n')
                
                if senior_roll_2_starting_number == 0:
                    print(f"Current Senior Ticket: {senior_letter}{current_senior_ticket}")
                    print(f"Total Senior Sales: {int(current_senior_ticket) - int(starting_senior_ticket)}\n")
                else:
                    print(f'Current Senior Day Use Ticket: {senior_roll_2_letter}{current_senior_ticket_2}')
                    total_senior_sales = (int(current_senior_ticket) - int(starting_senior_ticket)) + (int(current_senior_ticket_2) - int(senior_roll_2_starting_number))
                    print(f'Total Day Use Sales: {total_senior_sales}\n')
                
                if disabled_roll_2_starting_number == 0:
                    print(f"Current Disabled Discount Ticket: {disabled_letter}{current_disabled_ticket}")
                    print(f"Total Disabled Discount Sales: {int(current_disabled_ticket) - int(starting_disabled_ticket)}\n")
                else:
                    print(f'Current Disabled Discount Day Use Ticket: {disabled_roll_2_letter}{current_disabled_ticket_2}')
                    total_disabled_sales = (int(current_disabled_ticket) - int(starting_disabled_ticket)) + (int(current_disabled_ticket_2) - int(disabled_roll_2_starting_number))
                    print(f'Total Disabled Discount Day Use Sales: {total_disabled_sales}\n')

                print("====")
                print(f"Golden Poppy sales: {str(total_golden_poppy)}")
                print(f"California Explorer sales: {str(total_california_explorer)}")
                print(f"Total Extra Vehicle Sales: {str(total_xv)}")
                input("Press Enter to return to main menu")
                clear()

            case "16": # VOID TICKET (needs work)
                void_report = void_ticket()
                with open(xfilename, 'a') as xfile:
                    xfile.write(void_report)
                    xfile.close()

            case "X": # XREPORT
                final_dayuse_ticket = current_dayuse_ticket
                final_senior_ticket = current_senior_ticket
                final_disabled_ticket = current_disabled_ticket

                final_dayuse_ticket_2 = current_dayuse_ticket_2
                final_senior_ticket_2 = current_senior_ticket_2
                final_disabled_ticket_2 = current_disabled_ticket_2

                total_dayuse_sales_2 = 0
                total_senior_sales_2 = 0
                total_disabled_sales_2 = 0

                if final_dayuse_ticket_2 == 0: 
                    total_dayuse_sales = int(final_dayuse_ticket) - int(starting_dayuse_ticket)
                elif final_dayuse_ticket_2 > 0:
                    total_dayuse_sales = (int(final_dayuse_ticket) - int(starting_dayuse_ticket)) + (int(final_dayuse_ticket_2) - int(dayuse_roll_2_starting_number))
                
                if final_senior_ticket_2 == 0:
                    total_senior_sales = int(final_senior_ticket) - int(starting_senior_ticket)
                elif final_senior_ticket_2 > 0:
                    total_senior_sales = (int(final_senior_ticket) - int(starting_senior_ticket)) + (int(final_senior_ticket_2) - int(current_senior_ticket_2))
                
                total_disabled_sales = int(final_disabled_ticket) - int(starting_disabled_ticket)

                xreport = "XREPORT\n"
                xreport += "=======\n"
                xreport += today + '\n'
                xreport += f'Starting Day Use Ticket: {dayuse_letter}{starting_dayuse_ticket}\n'
                xreport += f'Starting Senior Ticket: {senior_letter}{starting_senior_ticket}\n'
                xreport += f'Starting Disabled Ticket: {disabled_letter}{starting_disabled_ticket}\n\n'

                if final_dayuse_ticket_2 > 0:
                    xreport += f'Second Day Use Roll started: {dayuse_roll_2_letter}{dayuse_roll_2_starting_number}\n'
                    xreport += f'Unsold Day Use Ticket: {dayuse_roll_2_letter}{final_dayuse_ticket_2}\n'
                else:
                    xreport += f'Unsold Day Use Ticket: {dayuse_letter}{final_dayuse_ticket}\n'

                if final_senior_ticket_2 > 0:
                    xreport += f'Second Senior Roll started: {senior_roll_2_letter}{senior_roll_2_starting_number}\n'
                    xreport += f'Unsold Senior Ticket: {senior_roll_2_letter}{final_senior_ticket_2}\n'
                else:
                    xreport += f'Unsold Senior Day Use Ticket: {senior_letter}{final_senior_ticket}\n'

                if final_disabled_ticket_2 > 0:
                    xreport += f'Second Disabled Roll started: {disabled_roll_2_letter}{disabled_roll_2_starting_number}\n'
                    xreport += f'Unsold Disabled Ticket: {disabled_roll_2_letter}{final_disabled_ticket_2}\n\n'
                else:
                    xreport += f'Unsold Disabled Day Use Ticket: {disabled_letter}{final_disabled_ticket}\n\n'



                xreport += "DAILY TOTALS\n"
                xreport += "============\n"
                xreport += ""
                xreport += f'Total Day Use sales: {total_dayuse_sales}\n'
                xreport += f'Total Senior Day Use sales: {total_senior_sales}\n'
                xreport += f'Total Disabled Day Use sales: {total_disabled_sales}\n'
                xreport += f'Total Small Buses: {total_small_buses}\n'
                xreport += f'Total Large Buses: {total_large_buses}\n'
                xreport += f'Total Regular Campsites: {total_regular_campsite}\n'
                xreport += f'Total Senior Campsites: {total_senior_campsite}\n'
                xreport += f'Total Disabled Discount Campsites: {total_disabled_campsite}\n'
                xreport += f'Total Extra Vehicle Sales: {total_xv}\n'
                xreport += f'Total Trail Camp Sales: {total_tc}\n'
                xreport += f'Total Hike/Bike Sales: {total_hb}\n'
                xreport += f'Total Golden Poppy sales: {total_golden_poppy}\n'
                xreport += f'Total California Explorer sales: {total_california_explorer}\n'
                xreport += "\n"
                xreport += f'Total Cash: ${total_cash:.2f}\n'
                xreport += f'Total Card: ${total_card:.2f}\n'
                xreport += f'Total Check: ${total_check:.2f}'
                with open(xfilename, 'a') as xfile:
                    xfile.write(xreport)
                    xfile.close()
                clear()
                print(f'XReport saved in {xfilename}.')
                print('\n'.join(xreport.splitlines()[-19:]))
                print("")
                subprocess.run(["notepad",xfilename])
                input("Press 'Enter' when finished.")
                return
            case _:
                continue

if __name__ == "__main__":
    main()