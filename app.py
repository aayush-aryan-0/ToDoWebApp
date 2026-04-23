from flask import Flask, flash, render_template, redirect, url_for, session,request

app = Flask(__name__)


@app.route('/',method=['GET'])
def home():
    print("Hello Welcome.... ")
    return f"WELCOME TO WEB"


if __name__ == "__main__":
    app.run()