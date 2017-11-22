import sqlite3

db = sqlite3.connect('database.db')

db.execute('''CREATE TABLE PeopleList1 (id INTEGER PRIMARY KEY AUTOINCREMENT, sex TEXT, age INT)''')
db.execute('''CREATE TABLE PeopleList2 (id INTEGER PRIMARY KEY AUTOINCREMENT, sex TEXT, age INT)''')
for i in range(33):
    db.execute("INSERT INTO PeopleList1 (sex, age) VALUES (CASE WHEN abs(random()%2) = 0"
               "    THEN 'Муж'"
               "    ELSE 'Жен'"
               "END, abs(random()%100))")
for i in range(27):
    db.execute("INSERT INTO PeopleList2 (sex, age) VALUES (CASE WHEN abs(random()%2) = 0"
               "    THEN 'Муж'"
               "    ELSE 'Жен'"
               "END, abs(random()%100))")

coeval = db.execute("SELECT * FROM PeopleList1 WHERE PeopleList1.age IN (SELECT age FROM PeopleList2)")
male_count1 = db.execute("SELECT COUNT(*) FROM PeopleList1 WHERE PeopleList1.sex = 'Муж'"
                         " AND PeopleList1.age BETWEEN 18 AND 59")
female_count1 = db.execute("SELECT COUNT(*) FROM PeopleList1 WHERE PeopleList1.sex = 'Жен'"
                           " AND PeopleList1.age BETWEEN 18 AND 54")
male_count2 = db.execute("SELECT COUNT(*) FROM PeopleList2 WHERE PeopleList2.sex = 'Муж'"
                         " AND PeopleList2.age BETWEEN 18 AND 60")
female_count2 = db.execute("SELECT COUNT(*) FROM PeopleList2 WHERE PeopleList2.sex = 'Жен'"
                           " AND PeopleList2.age BETWEEN 18 AND 55")
children_count1 = db.execute("SELECT COUNT(*) FROM PeopleList1 WHERE PeopleList1.age < 18")
children_count2 = db.execute("SELECT COUNT(*) FROM PeopleList2 WHERE PeopleList2.age < 18")
retired_count1 = db.execute("SELECT COUNT(*) FROM PeopleList1 WHERE PeopleList1.sex = 'Муж' AND PeopleList1.age > 59"
                            " OR PeopleList1.sex = 'Жен' AND PeopleList1.age > 54")
retired_count2 = db.execute("SELECT COUNT(*) FROM PeopleList2 WHERE PeopleList2.sex = 'Муж' AND PeopleList2.age > 59"
                            " OR PeopleList2.sex = 'Жен' AND PeopleList2.age > 54")

with db:
    cur1 = db.cursor()
    cur2 = db.cursor()
    cur1.execute("SELECT * FROM PeopleList1")
    cur2.execute("SELECT * FROM PeopleList2")
    rows1 = cur1.fetchall()
    rows2 = cur2.fetchall()

    print('------------------')

    print('Первая группа людей')

    print('------------------')

    print('№', 'пол', 'возраст')

    print('------------------')

    for row in rows1:
        print(row[0], row[1], row[2])

    print('------------------')

    print('Вторая группа людей')

    print('------------------')

    print('№', 'пол', 'возраст')

    print('------------------')

    for row in rows2:
        print(row[0], row[1], row[2])

print('------------------')

print('Список людей из первой группы, имеющих ровесников из второй группы')

print('------------------')

print('№', 'пол', 'возраст')

print('------------------')

rows3 = coeval.fetchall()

for row in rows3:
    print(row[0], row[1], row[2])

print("Количество =", len(rows3))

print('------------------')

print('Количество мужчин, женщин, детей и пенсионеров в первой группе')

print('------------------')

(m_number1, ) = male_count1.fetchone()
(f_number1, ) = female_count1.fetchone()
(c_number1, ) = children_count1.fetchone()
(r_number1, ) = retired_count1.fetchone()

print("Количество мужчин =", m_number1)
print("Количество женщин =", f_number1)
print("Количество детей =", c_number1)
print("Количество пенсионеров =", r_number1)

print('------------------')

print('Количество мужчин, женщин, детей и пенсионеров во второй группе')

print('------------------')

(m_number2, ) = male_count2.fetchone()
(f_number2, ) = female_count2.fetchone()
(c_number2, ) = children_count2.fetchone()
(r_number2, ) = retired_count2.fetchone()

print("Количество мужчин =", m_number2)
print("Количество женщин =", f_number2)
print("Количество детей =", c_number2)
print("Количество пенсионеров =", r_number2)

print('------------------')

if m_number1 > m_number2:
    print("В первой группе мужчин больше")
elif m_number1 == m_number2:
    print("Одинаковое количество мужчин")
else:
    print("Во второй группе мужчин больше")

if f_number1 > f_number2:
    print("В первой группе женщин больше")
elif f_number1 == f_number2:
    print("Одинаковое количество женщин")
else:
    print("Во второй группе женщин больше")

if c_number1 > c_number2:
    print("В первой группе детей больше")
elif c_number1 == c_number2:
    print("Одинаковое количество детей")
else:
    print("Во второй группе детей больше")

if r_number1 > r_number2:
    print("В первой группе пенсионеров больше")
elif r_number1 == r_number2:
    print("Одинаковое количество пенсионеров")
else:
    print("Во второй группе пенсионеров больше")

print('------------------')

print('Отправим часть мужчин из первой группы во вторую')

print('------------------')

db.execute("INSERT INTO PeopleList2 (sex, age) SELECT sex, age FROM PeopleList1 "
           "WHERE sex = 'Муж' AND age BETWEEN 18 AND 59 LIMIT 3")
db.execute("DELETE FROM PeopleList1 WHERE sex = 'Муж' AND age BETWEEN 18 AND 59 LIMIT 3")
male_count3 = db.execute("SELECT COUNT(*) FROM PeopleList2 WHERE PeopleList2.sex = 'Муж'"
                         " AND PeopleList2.age BETWEEN 18 AND 59")
(m_number3, ) = male_count3.fetchone()
print("Теперь мужчин во второй группе =", m_number3)

with db:
    cur3 = db.cursor()
    cur4 = db.cursor()
    cur3.execute("SELECT * FROM PeopleList1")
    cur4.execute("SELECT * FROM PeopleList2")
    rows3 = cur3.fetchall()
    rows4 = cur4.fetchall()

    print('------------------')

    print('Изменённый состав первой группы')

    print('------------------')

    print('№', 'пол', 'возраст')

    print('------------------')

    for row in rows3:
        print(row[0], row[1], row[2])

    print('------------------')

    print('Изменённый состав второй группы')

    print('------------------')

    print('№', 'пол', 'возраст')

    print('------------------')

    for row in rows4:
        print(row[0], row[1], row[2])

db.commit()
db.close()