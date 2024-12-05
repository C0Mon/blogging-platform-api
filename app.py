from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy()

app = Flask(__name__)

db_name = 'blog.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    category = db.Column(db.String)
    tags = db.Column(db.Blob)
    updatedAt = db.Column(db.String)
    createdAt = db.Column(db.String)
    
    def __init__(self, title, content, category, tags, updatedAt, createdAt):
        self.title = title
        self.content = content
        self.category = category
        self.tags = tags
        self.updatedAt = updatedAt
        self.createdAt = createdAt
    
@app.get("/posts")
def get_blog():
    return {
        "id": 1,
        "title": "My First Blog Post",
        "content": "This is the content of my first blog post.",
        "category": "Technology",
        "tags": ["Tech", "Programming"],
        "createdAt": "2021-09-01T12:00:00Z",
        "updatedAt": "2021-09-01T12:00:00Z"
    }

@app.post("/posts")
def post_blog():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

if __name__ == '__main__':
    app.run(debug=True)