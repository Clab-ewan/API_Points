from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

api_key = os.getenv('API_KEY')

app = Flask(__name__)
CORS(app)

# URL de l'API Kiln
KILN_API_BASE_URL = "https://api.kiln.fi/v1/defi/operations"
KILN_API_STAKES_URL = "https://api.kiln.fi/v1/defi/stakes"

# Blockchains autorisées
VALID_BLOCKCHAINS = {"eth", "arb", "bsc", "matic", "op"}

@app.route('/')
def home():
    return "Welcome to the vault dashboard API"

@app.route('/points', methods=['GET'])
def points():
    wallet = request.args.get('wallet')
    vault = request.args.get('vault')

    if not wallet:
        return jsonify({"success": False, "message": "Wallet address is required"}), 400
    if not vault:
        return jsonify({"success": False, "message": "Vault address is required"}), 400
    
    # Split the blockchain from the vault's address
    parts = vault.split("_")
    if len(parts) != 2 or parts[0] not in VALID_BLOCKCHAINS:
        return jsonify({"success": False, "message": "Invalid blockchain or bad Vault format."}), 400


    points, rewards, events_summary = calculate_staking_points(wallet, vault)

    return jsonify({
        "success": True,
        "message": f"Points calculated for the wallet {wallet} and for the vault {vault}.",
        "points": round(points, 2),
        "events": events_summary,
        "total_rewards": rewards
    })

def calculate_staking_points(wallet, vault):
    """
    Retrieves transactions from the selected wallet and vault, then calculates points.
    """
    try:
        url = f"{KILN_API_BASE_URL}?wallets={wallet}&vaults={vault}"
        headers = {
            "accept": "application/json; charset=utf-8",
            "Authorization": f"Bearer {api_key}"
        }
        response = requests.get(url, headers=headers)

        url_stakes = f"{KILN_API_STAKES_URL}?wallets={wallet}&vaults={vault}"
        headers = {
            "accept": "application/json; charset=utf-8",
            "Authorization": f"Bearer {api_key}"
        }
        response_stakes = requests.get(url_stakes, headers=headers)
        data_stakes = response_stakes.json()
        if "data" in data_stakes and len(data_stakes["data"]) > 0:
            total_rewards = float(data_stakes["data"][0]["total_rewards"]) / 10**6 # take care of the decimals
        else:
            total_rewards = 0
        if response.status_code != 200:
            print(f"Erreur API Kiln: {response.status_code}, {response.text}")
            return 0, []

        data = response.json()
        if "data" not in data or not isinstance(data["data"], list) or len(data["data"]) == 0:
            return 0, []

        # Sort the events in the right order
        events = sorted(data["data"], key=lambda x: x["timestamp"])
        
        TVL = 0
        first_timestamp = None
        total_points = 0
        last_time_since_start = 0
        events_summary = []

        for index, event in enumerate(events):
            event_time = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
            event_type = event["type"]
            amount = float(event["assets"]) / 10**6

            if first_timestamp is None:
                first_timestamp = event_time
                time_since_start = 0
            else:
                time_since_start = (event_time - first_timestamp).total_seconds() / 86400

            if index > 0:
                time_elapsed_days = time_since_start - last_time_since_start
                if time_elapsed_days > 0:
                    total_points += TVL * time_elapsed_days 

            if event_type == "deposit":
                TVL += amount
            elif event_type == "withdrawal":
                TVL -= amount
                TVL = max(TVL, 0)

            events_summary.append({
                "timestamp": event["timestamp"],
                "type": event_type,
                "amount": amount,
                "TVL_after_event": TVL,
                "cumulative_points": round(total_points, 2)
            })

            last_time_since_start = time_since_start

        # Calculate the points to now
        now_utc = datetime.now(timezone.utc)
        total_days_since_last_event = (now_utc - event_time).total_seconds() / 3600 / 24 # Duration in days

        if total_days_since_last_event > 0:
            last_period_points = TVL * total_days_since_last_event
            total_points += last_period_points 

        return total_points, total_rewards, events_summary  # Points formating

    except Exception as e:
        print("Erreur dans calculate_staking_points:", str(e))
        return 0, []

if __name__ == '__main__':
    app.run(debug=True)
