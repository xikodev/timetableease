import mysql.connector

groups = ['Profesori', '1.E1', '1.E2', '2.E1', '2.E2', '3.E1S', '3.E2S', '3.E1P', '3.E2P', '4.E1S', '4.E2S', '4.E1P', '4.E2P']
hours = ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
minutes = ['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55']
days = ['Ponedjeljak', 'Utorak', 'Srijeda', 'Cetvrtak', 'Petak']
shifts = ['A', 'B']
rooms = range(1, 30)
subjects = [
    ('Hrvatski', 'HRV'), ('Matematika', 'MAT'), ('Engleski', 'ENG'),
    ('Fizika', 'FIZ'), ('Etika', 'ET'), ('Vjeronauk', 'VJ'),
    ('Dizajn baza podataka', 'DBP'), ('Skriptni jezici i web programiranje', 'SJWP'), ('Web dizajn', 'WD'),
    ('Multimedija', 'MM'), ('Primjenjena matematika', 'PM'), ('Sat razrednika', 'SR'),
    ('Grada racunala', 'GRR'), ('Operacijski sustavi', 'OS'), ('Mikro upravljaci', 'MUP'),
    ('Racunalne mreze', 'RM'), ('Tjelesna i zdravstvena kultura', 'TZK'), ('Napredno i objektno programiranje', 'NOP'),
    ('Geografija', 'GEO'), ('Povijest', 'POV'), ('Kemija', 'KEM'),
    ('Biologija', 'BIO')
]
times = [
    (1, '7:45 - 8:25', 1),
    (2, '8:30 - 9:10', 1),
    (3, '9:15 - 9:55', 1),
    (4, '10:00 - 10:40', 1),
    (5, '11:00 - 11:40', 1),
    (6, '11:45 - 12:25', 1),
    (7, '12:30 - 13:10', 1),
    (8, '13:15 - 13:55', 1),
    (1, '13:15 - 13:55', 2),
    (2, '14:00 - 14:40', 2),
    (3, '14:45 - 15:25', 2),
    (4, '15:30 - 16:10', 2),
    (5, '16:30 - 17:10', 2),
    (6, '17:15 - 17:55', 2),
    (7, '18:00 - 18:40', 2),
    (8, '18:45 - 19:25', 2),
]

mydb = mysql.connector.connect(
    host="tsz.myftp.org",
    user="24bkrpan",
    password="KVU52ck8",
    database="raspored"
)
cursor = mydb.cursor()

def exec_command(table_name, field, list_of_values):
    if len(field[0]) > 1:
        command = f'INSERT INTO {table_name} ('
        for i in range(len(field)):
            command += f'{field[i]}'
            if i == len(field) - 1:
                command += ') VALUES ('
            else:
                command += ', '
        for value in list_of_values:
            for i in range(len(field)):
                command += f'"{value[i]}"'
                if i != len(field) - 1:
                    command += ', '
            if list_of_values.index(value) == len(list_of_values) - 1:
                command += ');'
            else:
                command += '), ('
        print(command)
        cursor.execute(command)
    else:
        for value in list_of_values:
            command = f'INSERT INTO {table_name} ({field}) VALUES ("{value}");'
            print(command)
            cursor.execute(command)
    mydb.commit()


# exec_command(table_name='base_hours', field='hour', list_of_values=hours)
# exec_command(table_name='base_minutes', field='minute', list_of_values=minutes)
# exec_command(table_name='base_days', field='name', list_of_values=days)
# exec_command(table_name='base_shifts', field='shift', list_of_values=shifts)
# exec_command(table_name='base_rooms', field='room', list_of_values=rooms)
# exec_command(table_name='base_subjects', field=('long_name', 'short_name'), list_of_values=subjects)
# exec_command(table_name='auth_group', field='name', list_of_values=groups)
# exec_command(table_name='base_times', field=('class_number', 'time', 'shift_id'), list_of_values=times)

mydb.close()
