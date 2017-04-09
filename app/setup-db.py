from app import db
import model

db.create_all()
db.session.commit() 
