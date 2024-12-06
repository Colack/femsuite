from parser import parse_torrent
from tracker import get_peers_from_tracker
from peer import connect_to_peer, download_piece
from file_operations import assemble_file
import random
import hashlib
import bencodepy

def main():
    torrent_file = input("Enter the path to the .torrent file: ")
    torrent_info = parse_torrent(torrent_file)

    info_hash = hashlib.sha1(bencodepy.encode(torrent_info['info'])).digest()
    peer_id = ''.join(random.choices("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=20)).encode('utf-8')

    print("Contacting tracker for peer list...")
    peers = get_peers_from_tracker(torrent_info)
    print(f"Found {len(peers)} peers.")

    pieces_data = [None] * (len(torrent_info['pieces']) // 20)

    for peer_ip, peer_port in peers:
        sock = connect_to_peer(peer_ip, peer_port, info_hash, peer_id)
        if sock:
            try:
                piece_index = random.randint(0, len(pieces_data) - 1)
                if pieces_data[piece_index] is None:
                    print(f"Downloading piece {piece_index} from {peer_ip}:{peer_port}")
                    piece_data = download_piece(sock, piece_index, torrent_info['piece_length'])
                    pieces_data[piece_index] = piece_data
                    print(f"Successfully downloaded piece {piece_index}")
            except Exception as e:
                print(f"Error downloading from peer {peer_ip}:{peer_port}: {e}")
            finally:
                sock.close()

    print("Assembling the file...")
    assemble_file(torrent_info, pieces_data)
    print("File assembled successfully!")

if __name__ == "__main__":
    main()
