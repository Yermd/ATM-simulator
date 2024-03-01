from tkinter import messagebox
import customtkinter as ctk
import cv2
import pygame
from customtkinter import *

from atm_utils import *

pygame.mixer.init()

button_click_sound = pygame.mixer.Sound('buttonsound.wav')

def play_button_click_sound():
    button_click_sound.play()

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('dark-blue')

TRIES = 0

global root
root = ctk.CTk()
root.title('Root Win')
# root window init
root.geometry('1920x1080')

f_name_lb = ctk.CTkLabel(root, text='ATM SIMULATOR', anchor="center", width=500, height=40)
f_name_lb.pack(pady=15)

quit_button = ctk.CTkButton(root, text='Quit', command=lambda: [play_button_click_sound(), root.destroy()], width=200, height=75)
quit_button.pack(pady=10, side='left', expand=True)

start_button = ctk.CTkButton(root, text='Start', command=lambda: [play_button_click_sound(), root.destroy(), start_win()], width=200, height=75)
start_button.pack(pady=10, side='right', expand=True)

def start_win():
    """
        gui design for start window
    """
    global root2
    root2 = CTk()
    root2.title('ATM BANK')
    root2.geometry('1920x1080')

    f_name_lb = ctk.CTkLabel(root2, text='WELCOME TO ATM BANK!', anchor="center", width=500, height=60)
    f_name_lb.pack(pady=20)

    lb = ctk.CTkFrame(root2, width=800, height=500, corner_radius=8)
    lb.pack(pady=20)

    service_lb = ctk.CTkLabel(lb, text='ATM Services')
    service_lb.pack(pady=(30, 5))

    create_acct_btn = ctk.CTkButton(lb, text="Create Account", command=lambda: [play_button_click_sound(), create_acct_win()], width=250, height=60)
    create_acct_btn.pack(pady=(15, 5))

    login_btn = ctk.CTkButton(lb, text="Input Card (Acct No.)", command=lambda: [reset_tries(TRIES), play_button_click_sound(), login_win(),], width=250, height=60)
    login_btn.pack(pady=(5, 20))

    quit_btn = ctk.CTkButton(root2, text='Quit', command=lambda: [root2.destroy(), play_button_click_sound(), messagebox.showinfo('Information','Thank You for Banking with us')], width=200, height=60)
    quit_btn.pack(pady=(15, 10))

    root2.mainloop()


def create_acct_win():
    """
        gui design for account creation window
    """
    global createwin
    createwin = CTk()
    createwin.title('ATM')
    createwin.geometry('1920x1080')
    font_settings = ('Arial', 24)

    f_name_lb = CTkLabel(createwin, text='Create Account', font=font_settings)
    f_name_lb.grid(row=0, column=0, padx=100, pady=(50, 20))

    fr = CTkFrame(createwin, width=1600, height=900)
    fr.grid(row=1, column=0, padx=160, pady=(50, 30))

    name_lb = CTkLabel(fr, text='Enter Name: ', font=font_settings)
    name_lb.grid(row=1, column=0, pady=(50, 20), sticky='W')

    pin_lb = CTkLabel(fr, text='Enter Pin: ', font=font_settings)
    pin_lb.grid(row=2, column=0, sticky='W')

    balance_lb = CTkLabel(fr, text='Deposit: ', font=font_settings)
    balance_lb.grid(row=3, column=0, sticky='W')

    entry_font_settings = ('Arial', 22)
    name = CTkEntry(fr, width=400, corner_radius=10, border_width=2, placeholder_text='Full Name', font=entry_font_settings)
    name.grid(row=1, column=1, padx=40, pady=(50, 20))

    pin = CTkEntry(fr, width=400, corner_radius=10, border_width=2, placeholder_text='4 digit pin', font=entry_font_settings)
    pin.grid(row=2, column=1)

    balance = CTkEntry(fr, width=400, corner_radius=10, border_width=2, placeholder_text='Initial Deposit', font=entry_font_settings)
    balance.grid(row=3, column=1)

    acct_create = CTkButton(fr, text='Create Now', font=font_settings, command=lambda: [play_button_click_sound(), create_acct(name.get(), pin.get(), balance.get())])
    acct_create.grid(row=4, column=1, padx=40, pady=(40, 30), ipadx=50)

    CTkButton(createwin, text='Quit', font=font_settings, command=lambda: [play_button_click_sound(), createwin.destroy(), start_win()]).grid(row=6, column=0, padx=100, pady=50)

    try:
        root2.destroy()
    except NameError:
        pass

    createwin.mainloop()


def create_acct(name, pin, balance=0):
    """
        collects user's name, pin and initial deposit\n
        stores this information in the database\n
        and generates an account number for the new user
    """
    if (name == '' or pin == ''):
        messagebox.showerror('error', 'You need a name and a pin number to create an account')
    else:
        assert pin.isdigit() and len(pin) == 4, messagebox.showerror('error', 'You need a four digit pin please')
        if balance == '':
            messagebox.showinfo('information', 'Your Bank Balance is 0.00')
        conn = sqlite3.connect('Bank_Accounts.db')
        c = conn.cursor()
        c.execute('INSERT INTO Accounts VALUES(:Name, :Pin, :Balance)',
                  {
                      'Name': name,
                      'Pin': pin,
                      'Balance': float(balance)
                  }
                  )
        accounts = query_all()
        createwin.destroy()
        messagebox.showinfo('information',
                            f'Account created Successfully! \n Account Number is: {accounts[-1][-1] + 1}')

        conn.commit()
        conn.close()

        print('Account Created Succesfully')

        start_win()


def login_win():
    """
        gui design for login window
    """
    global loginwin

    loginwin = CTk()
    loginwin.title('ATM')
    loginwin.geometry('1920x1080')

    font_settings = ('Arial', 24)

    card_lb = CTkLabel(loginwin, text='Card Received !', font=font_settings)
    card_lb.grid(row=0, column=0, columnspan=2, padx=20, pady=(100, 20))

    num_lb = CTkLabel(loginwin, text='Account No: ', font=font_settings)
    num_lb.grid(row=1, column=0, pady=(20, 10))

    a_num = CTkEntry(loginwin, width=400, corner_radius=10, border_width=2, font=('Arial', 22))
    a_num.grid(row=1, column=1, padx=40, pady=(20, 10))

    pin_lb = CTkLabel(loginwin, text='Enter Pin: ', font=font_settings)
    pin_lb.grid(row=2, column=0, pady=(20, 10))

    enter_pin = CTkEntry(loginwin, width=400, corner_radius=10, border_width=2, font=('Arial', 22))
    enter_pin.grid(row=2, column=1, padx=40, pady=(20, 10))

    login_acct = CTkButton(loginwin, text='Login', font=font_settings, command=lambda: [play_button_click_sound(), login(a_num.get(), enter_pin.get())])
    login_acct.grid(row=3, column=0, columnspan=2, padx=40, pady=(50, 20), ipadx=50)

    loginwin.mainloop()



def login(acct_number, pin):
    """
        Login account functionality\n
        collects the user's account number and pin\n
        queries database to return account details and grant access\n
        user get only 3 attempts at loggin in
    """
    global TRIES
    global acct_num

    assert acct_number != '', messagebox.showerror('error', 'Please, Input your account number')
    assert acct_number.isdigit(), messagebox.showerror('error', 'Letters not Allowed')
    assert pin != '', messagebox.showerror('error', 'Please, Input your pin')
    assert pin.isdigit(), messagebox.showerror('error', 'Letters Forbidden, Input your pin')

    acct_num = acct_number
    conn = sqlite3.connect('Bank_Accounts.db')
    c = conn.cursor()

    c.execute('SELECT *, oid from Accounts WHERE oid=' + acct_num)
    account = c.fetchall()

    if account == []:
        messagebox.showerror('error', 'This Account... Does not exist...')
        messagebox.showinfo('information', 'If you do not have an account try creating one.. It is really easy')
        return

    pin_value = int(pin)
    if TRIES >= 3:
        messagebox.showerror('error', f'Tries Limit Reached !!')
        loginwin.destroy()
        return

    if pin_value == account[0][1]:
        messagebox.showinfo('information', f'Pin Correct \n Welcome {account[0][0]}')
        main_win()

    else:
        messagebox.showerror('error', f'Pin Incorrect \n {3 - TRIES} more trie(s)')
        print(TRIES, "try: ", pin_value)
        TRIES = TRIES + 1
        loginwin.destroy()
        login_win()


def main_win():
    """
        gui design for the main window
    """
    global mainwin
    account = query(acct_num)
    name = account[0][0]
    mainwin = CTk()
    mainwin.title('ATM BANK')
    mainwin.geometry('1920x1080')
    font_settings = ('Arial', 30)

    f_name_lb = CTkLabel(mainwin, text=f'Welcome {name}', font=font_settings)
    f_name_lb.grid(row=0, column=0, pady=50, sticky='nsew')

    fr = CTkFrame(mainwin, width=1200, height=600)
    fr.grid(row=1, column=0, pady=50)
    fr.grid_propagate(False)
    fr.grid_columnconfigure(0, weight=1)

    button_font_settings = ('Arial', 24)
    check_bal = CTkButton(fr, text='Check Balance', font=button_font_settings, command=lambda:[play_button_click_sound(), check_balance()])
    check_bal.grid(row=2, column=0, pady=(30, 20), ipadx=20, ipady=10)

    withdraw = CTkButton(fr, text='Withdraw', font=button_font_settings, command=lambda: [play_button_click_sound(), withdrawal_win()])
    withdraw.grid(row=3, column=0, pady=(30, 20), ipadx=20, ipady=10)

    deposit = CTkButton(fr, text='Deposit', font=button_font_settings, command=lambda:[play_button_click_sound(), deposit_win()])
    deposit.grid(row=4, column=0, pady=(30, 20), ipadx=20, ipady=10)

    CTkButton(mainwin, text='Quit', font=button_font_settings, command=lambda: [play_button_click_sound(), mainwin.destroy(), messagebox.showinfo
    ('information', f'Thank You for Banking with us')]).grid(row=6, column=0, pady=(50, 20), ipadx=20, ipady=10)

    try:
        loginwin.destroy()
    except NameError:
        pass

    try:
        root2.destroy()
    except NameError:
        pass

    mainwin.grid_columnconfigure(0, weight=1)

    mainwin.mainloop()


def check_balance():
    """
        window displays basic account details
        i.e account balance, account name, and account number
    """
    global balwin
    balwin = CTk()
    balwin.title('ATM BANK')
    balwin.state('zoomed')
    balwin.geometry('1920x1080')

    account = query(acct_num)
    balance = account[0][-2]

    font_settings = ('Arial', 30)

    f_name_lb = CTkLabel(balwin, text='Account Details', font=font_settings)
    f_name_lb.grid(row=0, column=1, pady=50, sticky='nsew')

    fr = CTkFrame(balwin, width=1200, height=600)
    fr.grid(row=1, column=1, pady=30)
    fr.grid_propagate(False)
    fr.grid_columnconfigure(1, weight=1)

    name = CTkLabel(fr, text='Account Name:', font=font_settings)
    name.grid(row=2, column=0, pady=15, sticky='e')

    a_name = CTkLabel(fr, text=f'{account[0][0]}', font=font_settings, anchor='w')
    a_name.grid(row=2, column=2, pady=15)

    num = CTkLabel(fr, text='Account Number:', font=font_settings)
    num.grid(row=3, column=0, pady=15, sticky='e')

    a_num = CTkLabel(fr, text=f'{account[0][-1]}', font=font_settings, anchor='w')
    a_num.grid(row=3, column=2, pady=15)

    acct_bal = CTkLabel(fr, text='Account Balance:', font=font_settings)
    acct_bal.grid(row=4, column=0, pady=15, sticky='e')

    bal = CTkLabel(fr, text=f'{balance}', font=font_settings, anchor='w')
    bal.grid(row=4, column=2, pady=15)

    CTkButton(balwin, text='Quit', font=font_settings, command=balwin.destroy).grid(row=2, column=1, pady=50, sticky='nsew')

    balwin.grid_columnconfigure(1, weight=1)

    balwin.mainloop()



def withdrawal_win():
    """
        gui design for withdrawal window
    """
    global withdrawalwin
    withdrawalwin = CTk()
    withdrawalwin.state('zoomed')
    withdrawalwin.geometry('1920x1080')
    withdrawalwin.title('ATM BANK')

    account = query(acct_num)
    balance = account[0][-2]

    font_settings = ('Arial', 30)

    f_name_lb = CTkLabel(withdrawalwin, text='Withdrawal Menu', font=font_settings)
    f_name_lb.grid(row=0, column=0, padx=80, pady=40, columnspan=2, sticky='nsew')

    fr = CTkFrame(withdrawalwin, width=1200, height=600)
    fr.grid(row=1, column=0, pady=30, padx=360, columnspan=2)
    fr.grid_propagate(False)
    fr.grid_columnconfigure(0, weight=1)

    acct_bal = CTkLabel(fr, text=f'Account Balance: {balance}', font=font_settings)
    acct_bal.grid(row=2, column=0, columnspan=2, sticky='nsew')

    amount_lb = CTkLabel(fr, text='Withdrawal Amount: ', font=font_settings)
    amount_lb.grid(row=3, column=0, sticky='e')

    w_amount = CTkEntry(fr, width=400, corner_radius=10, border_width=2, font=('Arial', 22))
    w_amount.grid(row=3, column=1, padx=40, pady=(20, 0), sticky='w')

    pin_lb = CTkLabel(fr, text='Enter Pin: ', font=font_settings)
    pin_lb.grid(row=4, column=0, sticky='e')

    w_pin = CTkEntry(fr, width=400, corner_radius=10, border_width=2, font=('Arial', 22))
    w_pin.grid(row=4, column=1, padx=40, pady=(20, 0), sticky='w')

    w_sub = CTkButton(fr, text='Withdraw', font=font_settings, command=lambda: [play_button_click_sound(), Withdrawal(w_amount.get(), w_pin.get())])
    w_sub.grid(row=5, column=0, columnspan=2, pady=(30, 20), sticky='nsew', ipadx=20, ipady=10)

    CTkButton(withdrawalwin, text='Quit', font=font_settings, command=lambda: [play_button_click_sound(), withdrawalwin.destroy()]).grid(row=6, column=0, columnspan=2, pady=(30, 20), sticky='nsew')

    withdrawalwin.grid_columnconfigure(0, weight=1)

    withdrawalwin.mainloop()





def Withdrawal(amount, wd_pin):
    """
        collects the amount (in naira) the user wants to withdraw\n
        and user's pin, returns a massage box showing the transaction status\n
        (successful or unsuccessful -- as the case maybe)
    """
    global TRIES
    global acct_num

    account = query(acct_num)

    assert amount != '', messagebox.showerror('error', 'Please, Enter withdrawal amount')
    assert amount.isdigit(), messagebox.showerror('error', 'Letters Forbidden')
    assert wd_pin != '', messagebox.showerror('error', 'Piease, Input your pin')
    assert wd_pin.isdigit(), messagebox.showerror('error', 'Letters Forbidden, Input your pin')

    amount, wd_pin = int(amount), int(wd_pin)

    if wd_pin == account[0][1]:
        if amount > account[0][-2]:
            withdrawalwin.destroy()
            messagebox.showerror('error', f'Insufficient Balance')
        else:
            play_video()
            account = query(acct_num)
            new_bal = account[0][-2] - amount
            conn = sqlite3.connect('Bank_Accounts.db')
            c = conn.cursor()
            c.execute('''
                        UPDATE Accounts SET
                        Balance = :Balance
                        WHERE oid = :oid
                    ''',
                      {
                          'Balance': new_bal,
                          'oid': account[0][-1]
                      })

            conn.commit()
            conn.close()
            withdrawalwin.destroy()
            messagebox.showinfo('information', f'Transaction Successful')

    else:
        withdrawalwin.destroy()
        messagebox.showerror('error', f'Pin Incorrect')


def deposit_win():
    """
        gui display for deposit window
    """
    global depositwin

    depositwin = CTk()
    depositwin.state('zoomed')
    depositwin.geometry('1920x1080')
    depositwin.title('Deposit')

    account = query(acct_num)
    balance = account[0][-2]

    font_settings = ('Arial', 30)

    f_name_lb = CTkLabel(depositwin, text='Deposit Menu', font=font_settings)
    f_name_lb.grid(row=0, column=0, padx=80, pady=40, columnspan=2, sticky='nsew')

    fr = CTkFrame(depositwin, width=1200, height=600)
    fr.grid(row=1, column=0, pady=30, padx=360, columnspan=2)
    fr.grid_propagate(False)
    fr.grid_columnconfigure(0, weight=1)

    acct_bal = CTkLabel(fr, text=f'Account Balance: {balance}', font=font_settings)
    acct_bal.grid(row=1, column=0, columnspan=2, sticky='nsew')

    amount_lb = CTkLabel(fr, text='Deposit Amount: ', font=font_settings)
    amount_lb.grid(row=2, column=0, sticky='e')

    d_amount = CTkEntry(fr, width=400, corner_radius=10, border_width=2, font=('Arial', 22))
    d_amount.grid(row=2, column=1, padx=40, pady=(20, 0), sticky='w')

    pin_lb = CTkLabel(fr, text='Enter Pin: ', font=font_settings)
    pin_lb.grid(row=3, column=0, sticky='e')

    d_pin = CTkEntry(fr, width=400, corner_radius=10, border_width=2, font=('Arial', 22))
    d_pin.grid(row=3, column=1, padx=40, pady=(20, 0), sticky='w')

    d_sub = CTkButton(fr, text='Deposit', font=font_settings, command=lambda: [play_button_click_sound(), Deposit(d_amount.get(), d_pin.get())])
    d_sub.grid(row=4, column=0, columnspan=2, pady=(30, 20), sticky='nsew')

    CTkButton(depositwin, text='Quit', font=font_settings, command=lambda: [play_button_click_sound(), depositwin.destroy()]).grid(row=6, column=0, columnspan=2, pady=(30, 20), sticky='nsew')

    depositwin.grid_columnconfigure(0, weight=1)

    depositwin.mainloop()


def Deposit(amount, dp_pin):
    """
        collects the amount (in naira) the user wants to deposit\n
        and user's pin, returns a massage box showing the transaction status\n
        (successful or unsuccessful -- as the case maybe)
    """
    global acct_num

    account = query(acct_num)

    assert amount != '', messagebox.showerror('error', 'Please, Enter Deposit amount')
    assert amount.isdigit(), messagebox.showerror('error', 'You can\'t deposit letters')
    assert dp_pin != '', messagebox.showerror('error', 'Please, Input your pin')
    assert dp_pin.isdigit(), messagebox.showerror('error', 'Your pin are not letters')

    amount, dp_pin = int(amount), int(dp_pin)

    if dp_pin == account[0][1]:
        play_video()
        account = query(acct_num)
        new_bal = account[0][-2] + amount
        conn = sqlite3.connect('Bank_Accounts.db')
        c = conn.cursor()
        c.execute('''
                        UPDATE Accounts SET
                        Balance = :Balance
                        WHERE oid = :oid
                    ''',
                  {
                      'Balance': new_bal,
                      'oid': account[0][-1]
                  })

        conn.commit()
        conn.close()
        depositwin.destroy()
        messagebox.showinfo('information', f'Transaction Successful')
    else:
        depositwin.destroy()
        messagebox.showerror('error', f'Pin Incorrect')

def play_video():
    play_sound()
    cap = cv2.VideoCapture('finally.mp4')

    if not cap.isOpened():
        print("Error: Could not open video file")
        return

    while True:
        ret, frame = cap.read()

        if ret:
            cv2.imshow('Animation', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('cashout.mp3')
    pygame.mixer.music.play()





print(query_all())
root.mainloop()