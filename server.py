# server/server.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# Shared queue reference
target_queue = None
event_loop = None

def set_queue(queue):
    """
    Receive asyncio queue from main.py
    """

    global target_queue
    target_queue = queue

def set_loop(loop):
    """
    Receive asyncio event loop from main.py
    """

    global event_loop
    event_loop = loop 


@app.route("/", methods=["GET"])
def home():

    return "🚀 Drone server running", 200


@app.route("/drone-data", methods=["POST"])
def receive_target():

    global target_queue

    try:

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "No JSON received"
            }), 400

        # Extract target coordinates
        lat = data.get("lat")
        lon = data.get("lon")
        alt = data.get("alt", 5)

        # -----------------------------------
        # BASIC VALIDATION
        # -----------------------------------

        if lat is None or lon is None:

            return jsonify({
                "error": "Missing coordinates"
            }), 400

        target = {
            "lat": lat,
            "lon": lon,
            "alt": alt
        }

        print("\n📡 Emergency request received")
        print(target)

        # -----------------------------------
        # SEND TO MAIN MISSION LOOP
        # -----------------------------------

        if target_queue and event_loop:
            # Thread-safe communication
            event_loop.call_soon_threadsafe(
            target_queue.put_nowait,
            target
    )
        return jsonify({
            "status": "accepted",
            "target": target
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500