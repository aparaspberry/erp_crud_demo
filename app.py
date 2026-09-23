from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables Cross-Origin requests for the Desktop App client

# Initial 4 Vendor Records
VENDORS = [
    {"vendor_no": "V1001", "name": "Acme Corp", "type": "Supplier", "status": "Active"},
    {"vendor_no": "V1002", "name": "Global Logistics", "type": "Freight", "status": "Active"},
    {"vendor_no": "V1003", "name": "Apex Industrial", "type": "Manufacturer", "status": "Active"},
    {"vendor_no": "V1004", "name": "Metro Tech Solutions", "type": "IT Services", "status": "Inactive"},
]

# Simple Single-Page Web UI
HTML_TEMPLATE = """



    
    ERP Vendor Manager


"""

--- REST API ROUTES ---
@app.route("/")
def home():
return render_template_string(HTML_TEMPLATE)

@app.route("/health", methods=["GET"])
def health():
return jsonify({"status": "healthy"}), 200

@app.route("/api/vendors", methods=["GET"])
def get_vendors():
return jsonify(VENDORS), 200

@app.route("/api/vendors", methods=["POST"])
def add_vendor():
data = request.json
VENDORS.append(data)
return jsonify({"success": True, "message": "Vendor added"}), 201

@app.route("/api/vendors/", methods=["DELETE"])
def delete_vendor(vendor_no):
global VENDORS
VENDORS = [v for v in VENDORS if v["vendor_no"] != vendor_no]
return jsonify({"success": True, "message": "Vendor deleted"}), 200

if name == "main":
app.run(host="0.0.0.0", port=5000, debug=True)

