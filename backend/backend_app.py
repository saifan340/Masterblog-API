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
    """
       Handles fetching all posts and creating a new post.

       GET:
           Returns a list of all posts. Can be sorted by 'title' or 'content'.
           Query Params:
               sort (str, optional): Field to sort by ('title', 'content').
               direction (str, optional): Sort direction ('asc', 'desc').
       POST:
           Creates a new post. Expects a JSON body with 'title' and 'content'.
           Returns the newly created post.
    """
    if request.method == 'POST':
        return create_post()
    sort_key = request.args.get('sort')
    if sort_key:
       return sort_posts(sort_key)
    return get_posts()

def get_posts():
    """
        Returns a JSON list of all posts without sorting.
    """
    return jsonify(POSTS), 200

def create_post():
    """
        Creates a new post from JSON body.
        Requires 'title' and 'content' in request.
        Returns the newly created post or error if data is missing.
    """
    if not request.json or  'title' not in request.json or 'content'  not in request.json:
        return jsonify({'error': 'Missing required parameters'}), 400

    new_id= max( post['id'] for post in POSTS ) + 1 if POSTS else 1
    title= request.json['title']
    content= request.json['content']
    new_post= {"id":new_id, "title":title, "content":content}
    POSTS.append( new_post)

    return jsonify( new_post), 201
def sort_posts(sort_key):
    """
        Sorts posts by a specified key.

        Args:
            sort_key (str): Field to sort by ('title', 'content', or 'id').

        Query Params:
            direction (str): 'asc' (default) or 'desc' for sorting order.

        Returns:
            JSON list of sorted posts or error if sort_key is invalid.
    """
    direction = request.args.get('direction', 'asc')
    reverse_order = (direction == 'desc')

    if sort_key not in ['title', 'content', 'id']:
        return jsonify({"error": f"Invalid sort key: '{sort_key}'"}), 400

    sorted_posts = sorted(
    POSTS,
        key=lambda post: post.get(sort_key, '').lower(),
        reverse=reverse_order
         )
    return jsonify(sorted_posts), 200

@app.route('/api/posts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def post_by_id(id):
    """
    Handles operations on a single post identified by its ID.

    Args:
        id (int): The ID of the post to fetch, update, or delete.

    GET: Returns the specified post.
    PUT: Updates the specified post. Expects JSON with 'title' and 'content'.
    DELETE: Deletes the specified post.
    """
    post = next((p for p in POSTS if p['id'] == id), None)

    if post is None:
        return jsonify({"error": "Post not found"}), 404

    if request.method == 'GET':
        return jsonify(post), 200

    if request.method == 'DELETE':
        POSTS.remove(post)
        return jsonify(
            {"message": f"Post with id {id} has been deleted successfully."}
        ), 200

    if request.method == 'PUT':
        # Safely get data from the request body
        title = request.json.get('title')
        content = request.json.get('content')

        if title and content:
           post["title"] = title
           post["content"] = content
           return jsonify(post), 200
        else:
           return jsonify({"error": "Missing title or content"}), 400
@app.route('/api/posts/search', methods= ['GET'])
def search_posts():
    """
        Searches posts by title and/or content.

        Query Params:
            title (str): Substring to search in post titles.
            content (str): Substring to search in post contents.

        Returns:
            JSON list of matching posts or error if no parameters provided.
    """
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    if title_query is None and content_query is None:
        return jsonify({"error": "Missing required parameters"}), 400
        # Start with a copy of all posts to filter
    results = POSTS[:]

    if title_query:
        results = [
            post for post in results
            if title_query.lower() in post['title'].lower()
        ]

    if content_query:
        results = [
            post for post in results
            if content_query.lower() in post['content'].lower()
        ]

    return jsonify(results), 200


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
