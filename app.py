from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///german_words.db'
db = SQLAlchemy(app)


class GermanWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(10), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<GermanWord {self.word}>'
    

@app.route('/')
def render_index():
    words = GermanWord.query.all()
    return render_template('index.html', words=words)


@app.route('/api/upload/single_word', methods=['POST'])
def upload_single_word():
    article = request.form['article']
    word = request.form['word']
    meaning = request.form['meaning']
    
     # Check if the word already exists in the database
    existing_word = GermanWord.query.filter_by(word=word).first()
    if existing_word:
        return jsonify({'msg': '이미 등록된 단어입니다.'}, 400)
    
    # Check for empty inputs
    if not article or not word or not meaning:
        return jsonify({'msg': '모든 필드를 입력해주세요.'}, 400)

    new_word = GermanWord(article=article, word=word, meaning=meaning)
    db.session.add(new_word)
    db.session.commit()

    return jsonify({'msg' : '단어 등록에 성공했습니다'}, 200)


if __name__ == "__main__":
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)