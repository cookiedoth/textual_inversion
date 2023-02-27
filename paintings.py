from PIL import Image

class Painting:
    def __init__(self, path, title, artist_url, year):
        self.image = Image.open(path)
        self.image.load()
        self.title = title
        self.artist_url = artist_url
        self.year = year
        self.embedding = None

    def set_embedding(self, embedding):
        self.embedding = embedding

    def get_embedding(self):
        return self.embedding
