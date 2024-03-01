import sqlite3

def query_all():
    """
        return all accounts in the bank's database
    """
    conn = sqlite3.connect('Bank_Accounts.db')
    #create cursor
    c = conn.cursor()

    c.execute('SELECT *, oid FROM Accounts')
    records = c.fetchall()

    #commit changes
    conn.commit()
    #close connection
    conn.close()
    return records

def query(oid):
    """
        returns account details of the account whose account number\n
        has been passed as an arg.
    """
    conn = sqlite3.connect('Bank_Accounts.db')
    #create cursor
    c = conn.cursor()

    c.execute('SELECT *, oid FROM Accounts WHERE oid='+oid)
    records = c.fetchall()

    #commit changes
    conn.commit()
    #close connection
    conn.close()
    return records

def delete(oid):
    """
        delete account whose account number corresponds\n
        with the one passed as an arg
    """
    #create db or conect to one
    conn = sqlite3.connect('Bank_Accounts.db')
    #create cursor
    c = conn.cursor()

    c.execute('DELETE from Accounts WHERE oid= '+ str(oid))
    print('Account deleted successfully')

    #commit changes
    conn.commit()
    #close connection
    conn.close()

def reset_tries(tries):
    """
        reset tries incase a new user want to log in
    """
    tries = 0
    return tries


