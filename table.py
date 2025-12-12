from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def table():
    data = [
        {'name': 'Виталий', 'age': 20, 'city': 'Тула'},
        {'name': 'Ярослав', 'age': 21, 'city': 'Тула'},
        {'name': 'Макс', 'age': 20, 'city': 'Тула'}
    ]
    return render_template('table.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)