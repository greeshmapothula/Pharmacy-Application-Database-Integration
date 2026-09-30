#! /usr/bin/env python

#  runPharmacyApplication Solution

import psycopg2, sys, datetime

# The three Python functions for Lab4 should appear below.
# Write those functions, as described in Lab4 Section 4 (and Section 5,
# which describes the Stored Function used by the third Python function).
#
# Write the tests of those function in main, as described in Section 6
# of Lab4.


 # countNumberOfCustomers (myConn, thePharmacyID):
 # The Purchase table tells us about purchases made by a customer (customerID) in a pharmacy (pharmacyID).
 #
 # Besides the database connection, the countNumberOfCustomers function has one parameter, an
 # integer, thePharmacyID.
 #
 # countNumberOfCustomers counts the number of different customers that the pharmacy with thePharmacyID has,
 # based on the number of different customerID values that appears in the Purchase table.
 #
 # countNumberOfCustomers returns that value.
 #
 # For more details, including error handling and return codes, see the Lab4 pdf.

def countNumberOfCustomers (myConn, thePharmacyID):
    # pass

    # Python function to be supplied by students
 
 
 # ====================================   
    # Psuedocode in countNumberOfCustomers(conn, pharmacyID):
    try:
        cursor = myConn.cursor()

        # Step 1: SQL to check if the pharmacy exists
        check_sql = "SELECT 1 FROM Pharmacy WHERE pharmacyID = %s;"
        cursor.execute(check_sql, (thePharmacyID,))
        
        # fetchone() returns None if no row is found
        if cursor.fetchone() is None:
            # Step 2: Pharmacy not found, return the specified error code
            return -1
        else:
            # Step 3: Pharmacy exists, so count its distinct customers
            count_sql = "SELECT COUNT(DISTINCT customerID) FROM Purchase WHERE pharmacyID = %s;"
            cursor.execute(count_sql, (thePharmacyID,))
        
            # The result of a COUNT query is a single row with a single column, e.g., (5,)
            customer_count = cursor.fetchone()[0]
        
            # Step 4: Return the final count
            return customer_count

    # except Exception as e: 

    finally:
        if cursor:
            cursor.close()
 # ====================================   


# end countNumberOfCustomers


# updateOrderStatus (myConn, currentYear):
# In the OrderSuppy table, the value of status is either 'dlvd' (delivered), 'pndg' (pending), or 'cnld' (cancelled). 
#
# Besides the database connection, updateOrderStatus has another parameter, currentYear, which is an integer.
# If currentYear is between 2000 and 2030 (inclusive), then updateOrderStatus should append ' AS OF <currentYear>' at the end of the status value
# if status is not 'cnld'.
# Other values of currentYear are errors.
#
# updateOrderStatus should return the number of orders whose status values were updated.
#
# For more details, including error handling, see the Lab4 pdf.

def updateOrderStatus (myConn, currentYear):
    # pass
    
    # Python function to be supplied by students
    # You'll need to figure out value to return.

# ================================

    # In updateOrderStatus(conn, currentYear):
    # Step 1: Validate the year first
    if not (2000 <= currentYear <= 2030):
        return -1 # Return the error code for an invalid year

    try:
        cursor = myConn.cursor()
        
        # Step 2: Construct the SQL UPDATE command
        # The new status should be the old status plus ' AS OF ' and the year
        update_sql = "UPDATE OrderSupply SET status = status || ' AS OF ' || %s WHERE status IN ('dlvd', 'pndg');"

        cursor.execute(update_sql, (str(currentYear),))
        
        # Step 4: Get the number of rows that were updated
        rows_affected = cursor.rowcount # What is the name of the cursor attribute?
        
        # Step 3: IMPORTANT! Commit the changes to make them permanent
        myConn.commit()
        
        return rows_affected

    finally:
        if cursor:
            cursor.close()
    
    # Then return the number of rows affected (via cursor.rowcount).


# ================================

# end updateOrderStatus


# deleteSomeOrders (myConn, maxOrderDeletions):
# Besides the database connection, this Python function has one other parameter,
# maxOrderDeletions, which is an integer.
#
# deleteSomeOrders invokes a Stored Function, deleteSomeOrdersFunction, that you will need to
# implement and store in the database according to the description in Section 5.  The Stored
# Function deleteSomeOrdersFunction has all the same parameters as deleteSomeOrders (except
# for the database connection, which is not a parameter for the Stored Function), and it returns
# an integer.
#
# Section 5 of the Lab4 tells you which orders to delete and explains the integer value
# that deleteSomeOrdersFunction returns.  The deleteSomeOrders Python function returns the
# the same integer value that the deleteSomeOrdersFunction Stored Function returns.
#
# deleteSomeOrdersFunction doesnt print anything.  The deleteSomeOrders function must only
# invoke the Stored Function deleteSomeOrdersFunction, which does all of the work for this part
# of the assignment; deleteSomeOrders should not do any of the work itself.
#
# For more details, see the Lab4 pdf.

def deleteSomeOrders (myConn, maxOrderDeletions):

# We're giving you the code for deleteSomeOrders, but you'll have to write the
# Stored Function deleteSomeOrdersFunction yourselves in a PL/pgSQL file named
# deleteSomeOrdersFunction.pgsql
        
    try:
        myCursor = myConn.cursor()
        sql = "SELECT deleteSomeOrdersFunction(%s)"
        myCursor.execute(sql, (maxOrderDeletions, ))
    except:
        print("Call of deleteSomeOrdersFunction with argument", maxOrderDeletions, "had error", file=sys.stderr)
        myCursor.close()
        myConn.close()
        sys.exit(-1)
    
    row = myCursor.fetchone()
    myCursor.close()
    return(row[0])

#end deleteSomeOrders


def main():
    port = "5432"
    userID = "cse182"
    pwd = "database4me"

    # Try to make a connection to the database
    try:
        myConn = psycopg2.connect(port=port, user=userID, password=pwd)
    except:
        print("Connection to database failed", file=sys.stderr)
        sys.exit(-1)
        
    # We're making every SQL statement a transaction that commits.
    # Don't need to explicitly begin a transaction.
    # Could have multiple statement in a transaction, using myConn.commit when we want to commit.
    
    myConn.autocommit = True
    
    # cursor = myConn.cursor()
    
    # There are other correct ways of writing all of these calls correctly in Python.
        
    # Perform tests of countNumberOfCustomers, as described in Section 6 of Lab4.
    # Print their outputs (including error outputs) here, not in countNumberOfCustomers.
    # You may use a Python method to help you do the printing.


# TESTS 

    print("\n--- Testing countNumberOfCustomers ---")
    for pharmacyID in [11, 17, 44, 66]:
        result = countNumberOfCustomers(myConn, pharmacyID)
        if result is None or result < 0:
            print(f"\nError: countNumberOfCustomers failed for pharmacyID {pharmacyID}")
        else:
            print(f"\nNumber of customers for pharmacy {pharmacyID} is {result}")


    # Perform tests of updateOrderStatus, as described in Section 6 of Lab4.
    # Print their outputs (including error outputs) here, not in updateOrderStatus.
    # You may use a Python method to help you do the printing.

    print("\n ---Testing updateOrderStatus ---")
    for currentYear in [1999, 2025, 2031]:
        result = updateOrderStatus(myConn, currentYear)
        if result is None or result < 0:
            print(f"\nError: Invalid year {currentYear} passed to updateOrderStatus")
        else:
            print(f"\nNumber of orders whose status values were updated by updateOrderStatus is {result}")
 
 
    # Perform tests of deleteSomeOrders, as described in Section 6 of Lab4,
    # Print their outputs (including error outputs) here, not in deleteSomeOrders.
    # You may use a Python method to help you do the printing.

    print("\n ---Testing deleteSomeOrders ---")
    for maxOrderDeletions in [2, 4, 3, 1]:
        result = deleteSomeOrders(myConn, maxOrderDeletions)
        if result is None or result < 0:
            print(f"\nError : deleteSomeOrders failed for maxOrderDeletions value {maxOrderDeletions}")
        else:
            print(f"\nNumber of orders which were deleted for maxOrderDeletions value {maxOrderDeletions} is {result}")
  
    myConn.close()
    sys.exit(0)
#end

#------------------------------------------------------------------------------
if __name__=='__main__':

    main()

# end
