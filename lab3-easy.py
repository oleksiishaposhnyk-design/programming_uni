from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Users
users = {
    "admin": "1234"
}

# Products
items = {
    1: {"id": 1, "name": "Book", "price": 10, "color": "blue"},
    2: {"id": 2, "name": "Pen", "price": 2, "color": "black"}
}

# Log in check
def check_auth():
    auth = request.authorization
    if not auth:
        return False
    return users.get(auth.username) == auth.password

def auth_error():
    return Response("Auth required", 401,
                    {"WWW-Authenticate": 'Basic realm="Login"'})

# Itms
@app.route("/items", methods=["GET", "POST", "PUT", "DELETE"])
def all_items():
    if not check_auth():
        return auth_error()

    if request.method == "GET":
        return jsonify(list(items.values()))

    if request.method == "POST":
        data = request.json
        new_id = max(items.keys(), default=0) + 1
        data["id"] = new_id
        items[new_id] = data
        return jsonify(data)

    if request.method == "PUT":
        data = request.json
        item_id = data.get("id")
        if item_id in items:
            items[item_id] = data
            return jsonify(data)
        return jsonify({"error": "Item not found"})

    if request.method == "DELETE":
        items.clear()
        return jsonify({"message": "All items deleted"})
    return None


# items id
@app.route("/items/<int:item_id>", methods=["GET", "PUT", "DELETE"])
def one_item(item_id):
    if not check_auth():
        return auth_error()

    if item_id not in items:
        return jsonify({"error": "Item not found"})

    if request.method == "GET":
        return jsonify(items[item_id])

    if request.method == "PUT":
        items[item_id] = request.json
        items[item_id]["id"] = item_id
        return jsonify(items[item_id])

    if request.method == "DELETE":
        del items[item_id]
        return jsonify({"message": "Item deleted"})
    return None


if __name__ == "__main__":
    app.run()
