
from model import db, User, Shark, connect_to_db

def create_user(email, password):
    new_user = User(email=email, password=password)
    return(new_user)

def find_user(param1):
    user = User.query.filter_by(email = param1).first()
    return(user) 
    
def create_shark(shark_name, length, weight, diet, price, image_url):
    new_shark = Shark(
        shark_name=shark_name, 
        length=length, 
        weight=weight, 
        diet=diet,
        price=price,
        image_url=image_url
    )
    return(new_shark)

def get_all_sharks():
    return Shark.query.all()

def get_users():
    return User.query.all()    

def get_shark_by_id(shark_id):
    return Shark.query.get(shark_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)