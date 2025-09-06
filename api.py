from flask import Flask, request, jsonify import requests

app = Flask(name)

@app.route('/check', methods=['GET']) def check_player(): target_id = request.args.get('uid') if not target_id: return jsonify({"success": False, "message": "Missing 'uid' parameter"}), 400

cookies = {
    '_ga': 'GA1.1.2123120599.1674510784',
    '_fbp': 'fb.1.1674510785537.363500115',
    '_ga_7JZFJ14B0B': 'GS1.1.1674510784.1.1.1674510789.0.0.0',
    'source': 'mb',
    'region': 'MA',
    'language': 'ar',
    '_ga_TVZ1LG7BEB': 'GS1.1.1674930050.3.1.1674930171.0.0.0',
    'datadome': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
    'session_key': 'efwfzwesi9ui8drux4pmqix4cosane0y',
}

headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://shop2game.com',
    'Referer': 'https://shop2game.com/app/100067/idlogin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8)',
    'accept': 'application/json',
    'content-type': 'application/json',
    'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'x-datadome-clientid': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
}

json_data = {
    'app_id': 100067,
    'login_id': target_id,
    'app_server_id': 0,
}

try:
    res = requests.post('https://shop2game.com/api/auth/player_id_login', cookies=cookies, headers=headers, json=json_data)
    if res.status_code != 200 or not res.json().get('nickname'):
        return jsonify({"success": False, "message": "Error: ID NOT FOUND"})

    player_data = res.json()
    nickname = player_data.get('nickname', 'N/A')
    region = player_data.get('region', 'N/A')

    ban_url = f'https://ff.garena.com/api/antihack/check_banned?lang=en&uid={target_id}'
    ban_response = requests.get(ban_url, headers=headers)
    ban_data = ban_response.json()

    is_banned = False
    ban_period = 0
    if ban_data.get("status") == "success" and "data" in ban_data:
        is_banned = bool(ban_data["data"].get("is_banned", 0))
        ban_period = int(ban_data["data"].get("period", 0))

    return jsonify({
        "success": True,
        "nickname": nickname,
        "region": region,
        "is_banned": is_banned,
        "ban_period": ban_period,
        "message": "Player found and data retrieved successfully."
    })
except requests.exceptions.RequestException as e:
    return jsonify({"success": False, "message": str(e)})

if name == 'main': app.run(debug=True)

