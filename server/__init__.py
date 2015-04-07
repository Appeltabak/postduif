from flask import Flask

app = Flask(__name__)
app.config.from_object('config.config')

print(app.config['DATABASE_URI'])