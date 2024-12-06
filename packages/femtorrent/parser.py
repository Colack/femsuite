import bencodepy

def parse_torrent(file_path):
    with open(file_path, 'rb') as f:
        torrent_data = bencodepy.decode(f.read())
    
    info = torrent_data[b'info']
    name = info[b'name'].decode('utf-8')
    piece_length = info[b'piece length']
    pieces = info[b'pieces']
    length = info[b'length']
    trackers = [torrent_data[b'announce'].decode('utf-8')]

    if b'announce-list' in torrent_data:
        for tier in torrent_data[b'announce-list']:
            for tracker in tier:
                trackers.append(tracker.decode('utf-8'))

    return {
        'name': name,
        'piece_length': piece_length,
        'pieces': pieces,
        'length': length,
        'trackers': trackers,
        'info': info
    }
