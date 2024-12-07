from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy()

app = Flask(__name__)

db_name = 'blog.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

#NO TABLE?????
class Blog(db.Model):
    __tablename__ = 'Blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    category = db.Column(db.String)
    createdAt = db.Column(db.String)
    updatedAt = db.Column(db.String)
    
    def __init__(self, title, content, category, updatedAt, createdAt):
        self.title = title
        self.content = content
        self.category = category
        self.createdAt = createdAt
        self.updatedAt = updatedAt
    
@app.get("/posts")
def get_blog():
    return {
        "id": 1,
        "title": "My First Blog Post",
        "content": "This is the content of my first blog post.",
        "category": "Technology",
        "createdAt": "2021-09-01T12:00:00Z",
        "updatedAt": "2021-09-01T12:00:00Z"
    }

@app.post("/posts")
def post_blog():
    try:
        title = request.json['title']
        content = request.json['content']
        category = request.json['category']
        createdAt = request.json['createdAt']
        updatedAt = request.json['updatedAt']

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
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

if __name__ == '__main__':
    app.run(debug=True)