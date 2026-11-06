from src import packet

CHUNK_SIZE = 64

def chunk(file: str):
     with open(file, 'rb') as f:
          content = f.read()

     for i in range(0, len(content), CHUNK_SIZE):
          chunk_data = content[i : i + CHUNK_SIZE]
          yield b'$chunks:' + chunk_data