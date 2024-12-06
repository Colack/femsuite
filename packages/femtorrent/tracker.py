import requests
import hashlib
import random
import string
import urllib.parse
import bencodepy

def get_peers_from_tracker(torrent_info):
    info_hash = hashlib.sha1(bencodepy.encode(torrent_info['info'])).digest()
    peer_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20)).encode('utf-8')
    params = {
        'info_hash': info_hash,
        'peer_id': peer_id,
        'left': torrent_info['length'],
        'compact': 1,
        'port': random.randint(6881, 6889),
    }

    peers = []
    for tracker in torrent_info['trackers']:
        url = tracker + '?' + urllib.parse.urlencode(params)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = bencodepy.decode(response.content)
                peers += extract_peers(data[b'peers'])
        except Exception as e:
            print(f"Error communicating with tracker {tracker}: {e}")

    return peers

def extract_peers(peers_binary):
    peers = []
    for i in range(0, len(peers_binary), 6):
        ip = '.'.join(str(b) for b in peers_binary[i:i+4])
        port = int.from_bytes(peers_binary[i+4:i+6], byteorder='big')
        peers.append((ip, port))
    return peers
