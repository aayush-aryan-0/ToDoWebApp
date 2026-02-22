from flask import Flask
app=Flask(__name__)
@app.route('/')
def hello():
    return '<h2>Welcome to my todo list app</h2>'
if __name__ == "__main__":
    app.run(debug=True)