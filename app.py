from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "people.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        city TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM people")
    people = cursor.fetchall()

    print(f"DEBUG: people = {people}")
    print(f"DEBUG: people type = {type(people)}")
    if people:
        print(f"DEBUG: first person = {people[0]}")
        print(f"DEBUG: first person type = {type(people[0])}")

    conn.close()

    return render_template('index.html', people=people)

@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        city = request.form['city']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO people(name,age,city) VALUES(?,?,?)",
            (name, age, city)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        city = request.form['city']

        cursor.execute("""
        UPDATE people
        SET name=?, age=?, city=?
        WHERE id=?
        """, (name, age, city, id))

        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute("SELECT * FROM people WHERE id=?", (id,))
    person = cursor.fetchone()

    conn.close()

    return render_template('edit.html', person=person)

@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM people WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)