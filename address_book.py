import mysql.connector
from tkinter import *


class AddressBook:
    def __init__(self, master):
        self.frame_list_box = Frame(master)
        self.frame_list_box.place(relx=0.2, rely=0)

        self.scroll = Scrollbar(self.frame_list_box)
        self.list_box = Listbox(self.frame_list_box, yscrollcommand=self.scroll.set, height=12)
        self.scroll.config(command=self.list_box.yview)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.list_box.pack(side=LEFT, fill=BOTH, expand=1)

        self.frame_name = Frame(master)
        self.frame_name.place(relx=0, rely=0.05)

        self.name_lab = Label(self.frame_name, text='NAME:')
        self.name_lab.pack(side=LEFT)
        self.name_ent = Entry(self.frame_name)
        self.name_ent.pack(side=RIGHT)

        self.frame_phone_num = Frame(root)
        self.frame_phone_num.place(relx=0, rely=0.1)

        self.phone_lab = Label(self.frame_phone_num, text='TEL.:')
        self.phone_lab.pack(side=LEFT)
        self.phone_ent = Entry(self.frame_phone_num)
        self.phone_ent.pack(side=RIGHT)

        self.frame_email = Frame(master)
        self.frame_email.place(relx=0, rely=0.15)

        self.email_lab = Label(self.frame_email, text='EMAIL:')
        self.email_lab.pack(side=LEFT)
        self.email_ent = Entry(self.frame_email)
        self.email_ent.pack(side=RIGHT)

        self.btn_view = Button(text='VIEW', width=6, bg='black', fg='white', command=self.show_contacts)
        self.btn_view.place(x=5, y=130)

        self.btn_add = Button(text='ADD', width=6, bg='black', fg='white', command=self.add_contact)
        self.btn_add.place(x=5, y=160)

        self.btn_edit = Button(text='EDIT', width=6, bg='black', fg='white', command=self.edit_contact)
        self.btn_edit.place(x=5, y=190)

        self.btn_del = Button(text='DELETE', width=6, bg='black', fg='white', command=self.del_contact)
        self.btn_del.place(x=5, y=220)

        self.btn_del_all_contacts = Button(text='DELETE ALL CONTACTS', width=18, bg='black', fg='white',
                                           command=self.del_all)
        self.btn_del_all_contacts.place(x=5, y=250)

        self.cnx = mysql.connector.MySQLConnection(host='localhost', user='thomd729', password='cLjq=p(6',
                                                   database='address_book')
        self.cursor = self.cnx.cursor()
        all_names = 'SELECT name FROM address_book'
        self.cursor.execute(all_names)
        names = self.cursor.fetchall()
        for name in names:
            self.list_box.insert(0, name[0])

    def show_contacts(self):
        name = self.name_ent.get()

        query = 'SELECT telephone FROM address_book WHERE name=%s'
        self.cursor.execute(query, (name,))
        phone = self.cursor.fetchone()
        self.phone_ent.delete(0, END)
        self.phone_ent.insert(0, phone[0])

        query = 'SELECT email FROM address_book WHERE name=%s'
        self.cursor.execute(query, (name,))
        email = self.cursor.fetchone()
        self.email_ent.delete(0, END)
        self.email_ent.insert(0, email[0])

    def add_contact(self):
        name = self.name_ent.get()
        phone = self.phone_ent.get()
        email = self.email_ent.get()
        query = 'INSERT INTO address_book (name, telephone, email) VALUES (%s, %s, %s)'
        self.cursor.execute(query, (name, phone, email))
        self.cnx.commit()

        query = 'SELECT name FROM address_book'
        self.cursor.execute(query)
        names = self.cursor.fetchall()
        self.list_box.delete(0, END)
        for name in names:
            self.list_box.insert(0, name[0])

        self.name_ent.delete(0, END)
        self.phone_ent.delete(0, END)
        self.email_ent.delete(0, END)

    def edit_contact(self):
        name = self.name_ent.get()
        phone = self.phone_ent.get()
        email = self.email_ent.get()
        query = 'UPDATE address_book SET telephone=%s, email=%s WHERE name=%s'
        self.cursor.execute(query, (phone, email, name))
        self.cnx.commit()

        self.name_ent.delete(0, END)
        self.phone_ent.delete(0, END)
        self.email_ent.delete(0, END)

    def del_contact(self):
        name = self.name_ent.get()
        query = 'DELETE FROM address_book WHERE name=%s'
        self.cursor.execute(query, (name,))
        self.cnx.commit()

        self.list_box.delete(0, END)
        self.name_ent.delete(0, END)

        query = 'SELECT name FROM address_book'
        self.cursor.execute(query)
        names = self.cursor.fetchall()
        for name in names:
            self.list_box.insert(0, name[0])

    def del_all(self):
        query = 'TRUNCATE TABLE address_book'
        self.cursor.execute(query)
        self.cnx.commit()

        self.list_box.delete(0, END)


root = Tk()
AddressBook(root)
root.mainloop()
