from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "")
        return f"<h1>Привет, {name}!</h1>"

    return """
        <form method='post'>
            <input name='name' placeholder='Введите имя'>
            <button type='submit'>Отправить</button>
        </form>
    """

app.run(debug=True)
