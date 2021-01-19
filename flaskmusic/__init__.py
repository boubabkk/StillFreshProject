from datetime import date

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
# Will protect against modifying cookies and cross site request forgery request
app.config['SECRET_KEY'] = 'R<5DXkZx0,sV`yLaw!,HZU~]GjGx'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# sqlite store the database locally in a file
# Tell our flask app where our configuration is going to be stored
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)  # create the database

from flaskmusic import route

# engine = create_engine('sqlite:///database.db')
# my_metadata = MetaData()
# Base = declarative_base(metadata=my_metadata)
#
# Base.metadata.create_all(engine)
#
#
# session = Session()
#
# artist_1 = Artist('Drake', 'Take care', 'Scorpion', '/static/img/drake.jpg', date(2002, 10, 11))
# artist_2 = Artist('Travis Scott', 'HIGHEST IN THE ROOM', 'HIGHEST IN THE ROOM', '/static/img/tscott.jpg', date(2013, 8, 23))
# artist_3 = Artist('Burna Boy', 'Anybody', 'African Giant', '/static/img/africa.jpg', date(2016, 4, 2))
#
# album_1 = Album('Scorpion', '/static/img/drake.jpg', date(2002, 10, 11), artist_1.id)
# album_2 = Album('HIGHEST IN THE ROOM', '/static/img/tscott.jpg', date(2013, 8, 23), artist_2.id)
# album_3 = Album('African Giant', '/static/img/africa.jpg', date(2016, 4, 2), artist_3.id)
#
# session.add(artist_1)
# session.add(artist_2)
# session.add(artist_3)
#
# session.add(album_1)
# session.add(album_2)
# session.add(album_3)
#
# session.commit()
# session.close()


# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'vegetafinalflash99@gmail.com'
# app.config['MAIL_PASSWORD'] = 'finalFlash99!'
# mail = Mail(app)

