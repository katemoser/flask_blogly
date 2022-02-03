from models import User, db
from app import app
# Create all tables
db.drop_all()
db.create_all()
# If table isn't empty, empty it
User.query.delete()
# Add Users
whiskey = User(first_name='Whiskey', last_name='Moser',image_url="https://media.wired.co.uk/photos/607d91994d40fbb952b6ad64/4:3/w_2664,h_1998,c_limit/wired-meme-nft-brian.jpg")
bowser = User(first_name='Bowser',last_name='Tang', image_url="https://media.wired.co.uk/photos/607d91994d40fbb952b6ad64/4:3/w_2664,h_1998,c_limit/wired-meme-nft-brian.jpg")
spike = User(first_name='Spike',last_name='Spike', image_url="https://media.wired.co.uk/photos/607d91994d40fbb952b6ad64/4:3/w_2664,h_1998,c_limit/wired-meme-nft-brian.jpg")
# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
# Commit--otherwise, this never gets saved!
db.session.commit()
