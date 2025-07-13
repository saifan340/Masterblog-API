from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        return create_post()
    return get_posts()

def get_posts():
    return jsonify(POSTS), 200

def create_post():
    if not request.json or  'title' not in request.json or 'content'  not in request.json:
        return jsonify({'error': 'Missing required parameters'}), 400

    new_id= max( post['id'] for post in POSTS ) + 1 if POSTS else 1
    title= request.json['title']
    content= request.json['content']
    new_post= {"id":new_id, "title":title, "content":content}
    POSTS.append( new_post)

    return jsonify( new_post), 201

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error handler."""
    return jsonify({"error": "Page not found"}), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Custom 500 error handler."""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
