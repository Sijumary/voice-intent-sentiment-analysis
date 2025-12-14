import requests


URL = 'http://localhost:8000/analyze'


def send_file(path):
    with open(path, 'rb') as f:
        files = {'audio': (path, f, 'audio/wav')}
        r = requests.post(URL, files=files)
        print('Status:', r.status_code)
        print(r.json())


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python example_client.py path/to/audio.wav')
        sys.exit(1)
    send_file(sys.argv[1])