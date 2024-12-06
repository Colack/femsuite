import os

def save_piece(file_path, piece_index, piece_data, piece_length):
    with open(file_path, 'r+b') as f:
        f.seek(piece_index * piece_length)
        f.write(piece_data)

def assemble_file(torrent_info, pieces_data):
    file_path = torrent_info['name']
    piece_length = torrent_info['piece_length']
    file_length = torrent_info['length']

    with open(file_path, 'wb') as f:
        f.truncate(file_length)

    for piece_index, piece_data in enumerate(pieces_data):
        save_piece(file_path, piece_index, piece_data, piece_length)
