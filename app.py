from flask import Flask, render_template, request, redirect, abort

app = Flask(__name__)

people = []
next_id = 1

@app.route('/')
def index():
    return render_template('index.html', people=people)

@app.route('/add', methods=['GET', 'POST'])
def add():
    global next_id

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']

        person = {
            'id': next_id,
            'name': name,
            'age': int(age),
            'city': city
        }
        people.append(person)
        next_id += 1

        return redirect('/')

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    person = next((p for p in people if p['id'] == id), None)
    if person is None:
        abort(404)

    if request.method == 'POST':
        person['name'] = request.form['name']
        person['age'] = int(request.form['age'])
        person['city'] = request.form['city']
        return redirect('/')

    return render_template('edit.html', person=person)

@app.route('/delete/<int:id>')
def delete(id):
    global people
    people = [p for p in people if p['id'] != id]
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)