import socket
import hashlib

def connect_to_peer(peer_ip, peer_port, info_hash, peer_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((peer_ip, peer_port))
        
        protocol = b'BitTorrent protocol'
        reserved = b'\x00' * 8
        handshake = (
            len(protocol).to_bytes(1, 'big') + protocol + reserved + info_hash + peer_id
        )
        sock.sendall(handshake)
        response = sock.recv(68)

        if len(response) < 68 or response[28:48] != info_hash:
            print(f"Invalid handshake from {peer_ip}:{peer_port}")
            sock.close()
            return None
        
        print(f"Handshake successful with {peer_ip}:{peer_port}")
        return sock
    except Exception as e:
        print(f"Error connecting to peer {peer_ip}:{peer_port}: {e}")
        return None
