import psycopg2
from datetime import datetime
from tabulate import tabulate


def connect():
    return psycopg2.connect(
        database="postgres",
        user="postgres",
        password="sardor2005",
        host="localhost",
        port=5432
    )


# def create_table():
#     conn = connect()
#     cur = conn.cursor()
#
#     cur.execute(
#         '''
#         create table product (
#         id serial primary key ,
#         name varchar(50),
#         price decimal,
#         amount int,
#         time date,
#         expiration date
#         );
#         '''
#     )
#
#     conn.commit()
#     conn.close()
#
#
# create_table()


def insert_medicine(name, price, amount, expiration):
    time = datetime.now().strftime('%Y-%m-%d')

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        '''
        insert into product(name, price, amount, time, expiration)
        values (%s, %s, %s, %s, %s)
        ''', (name, price, amount, time, expiration)
    )

    conn.commit()
    conn.close()


def search_medicine(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        '''
        select * from product where name = %s
        ''', (name,)
    )

    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def delete_medicine(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        '''
        delete from product where name = %s
        ''', (name,)
    )

    conn.commit()
    conn.close()


def delete_expiration_medicine():
    time = datetime.now().strftime('%Y-%m-%d')
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        '''
         delete from product
            where expiration < %s
            ''', (time,)
    )

    conn.commit()
    conn.close()


def monthly_report():
    current_month = datetime.now().strftime('%Y-%m')
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        '''
        select * from product where date_part('year', time) = %s and date_part('month', time) = %s
        ''', (current_month[:4], current_month[5:])
    )

    results = cur.fetchall()
    conn.close()
    return results


def print_tab(arr):
    header = ['ID', 'Name', 'Price', 'Date', 'Expiration']
    table = tabulate(arr, headers=header, tablefmt='grid')
    print(table)


delete_expiration_medicine()


def main():
    while True:
        print('''
        1) Add medicine
        2) Search medicine
        3) Delete medicine
        4) Monthly report
        5) Exit
        ''')
        k = int(input("Choose: "))
        if k == 1:
            name = input("Enter medicine name: ")
            price = input("Enter medicine price: ")
            amount = input("Enter medicine amount: ")
            expiration = input("Enter expiration time: ")
            insert_medicine(name, price, amount, expiration)
            print('Medicine added successfully!')
        elif k == 2:
            name = input("Enter medicine name: ")
            results = search_medicine(name)
            if results:
                print_tab(results)
            else:
                print("Medicine not found.")
        elif k == 3:
            name = input("Enter medicine name: ")
            delete_medicine(name)
            print('Medicine deleted successfully!')
        elif k == 4:
            results = monthly_report()
            if results:
                print_tab(results)
            else:
                print("No data for this month.")
        elif k == 5:
            break
        else:
            print("Invalid choice.")


main()
