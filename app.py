from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime, timezone
db = SQLAlchemy()

app = Flask(__name__)

db_name = 'blog.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

def error(e: Exception) -> str:
    errorText = "<p>The error:<br>" + str(e) + "</p>"
    hed = '<h1>Something is broken.</h1>'
    return hed + errorText

class Blog(db.Model):
    __tablename__ = 'Blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    content = db.Column(db.String)
    category = db.Column(db.String)
    createdAt = db.Column(db.String)
    updatedAt = db.Column(db.String)
    
    def __init__(self, title, content, category, updatedAt, createdAt) -> None:
        self.title = title
        self.content = content
        self.category = category
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    def dictionary(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
    
@app.get("/posts")
def get_all_blogs():
    try:
        posts = db.session.query(Blog).all()
        newList = []
        for post in posts:
            newList.append(post.dictionary())
        return newList
    except Exception as e:
        return error(e)

@app.get("/posts/<int:id>")
def get_blog(id: int):
    try:
        post = db.session.query(Blog).filter_by(id = id).one()
        return post.dictionary()
    except Exception as e:
        return error(e)


@app.post("/posts")
def post_blog():
    try:
        title = request.json['title']
        content = request.json['content']
        category = request.json['category']
        createdAt = datetime.now(timezone.utc)
        updatedAt = datetime.now(timezone.utc)

        record = Blog(
            title,
            content,
            category,
            createdAt,
            updatedAt
        )
        db.session.add(record)
        db.session.commit()
        
        message = f"Your blog {title} has been posted"
        return message
    except Exception as e:
        return error(e)

@app.put("/posts")
def update_blog():
    try:
        post = db.session.query(Blog).filter_by(title = request.json['title']).one()
        setattr(post, "title", request.json['title'])
        setattr(post, "content", request.json['content'])
        setattr(post, "category", request.json['category'])
        db.session.commit()
        return post.dictionary()  

    except Exception as e:
        return error(e)

if __name__ == '__main__':
    app.run(debug=True)