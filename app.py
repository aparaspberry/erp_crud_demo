from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)
 
VENDORS = [
    {"vendor_no": "V1001", "name": "Acme Corp", "type": "Supplier", "status": "Active"},
    {"vendor_no": "V1002", "name": "Global Logistics", "type": "Freight", "status": "Active"},
    {"vendor_no": "V1003", "name": "Apex Industrial", "type": "Manufacturer", "status": "Active"},
    {"vendor_no": "V1004", "name": "Metro Tech Solutions", "type": "IT Services", "status": "Inactive"},
]
 
@app.route("/")
def home():
    return send_file("index.html")
 
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200
 
@app.route("/api/vendors", methods=["GET"])
def get_vendors():
    return jsonify(VENDORS), 200
 
@app.route("/api/vendors", methods=["POST"])
def add_vendor():
    data = request.json or {}
    if not data.get("vendor_no") or not data.get("name"):
        return jsonify({"success": False, "message": "vendor_no and name are required"}), 400
    if any(v["vendor_no"] == data["vendor_no"] for v in VENDORS):
        return jsonify({"success": False, "message": "vendor_no already exists"}), 409
    VENDORS.append({
        "vendor_no": data["vendor_no"],
        "name": data["name"],
        "type": data.get("type", "Supplier"),
        "status": data.get("status", "Active"),
    })
    return jsonify({"success": True, "message": "Vendor added"}), 201
 
# FIX: <vendor_no> was missing from the route path, so Flask never captured it
# and this endpoint would 500 on every call.
@app.route("/api/vendors/<vendor_no>", methods=["DELETE"])
def delete_vendor(vendor_no):
    global VENDORS
    before = len(VENDORS)
    VENDORS = [v for v in VENDORS if v["vendor_no"] != vendor_no]
    if len(VENDORS) == before:
        return jsonify({"success": False, "message": "Vendor not found"}), 404
    return jsonify({"success": True, "message": "Vendor deleted"}), 200
 
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
 