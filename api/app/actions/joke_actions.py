import requests

from ..schemas.joke import Joke


class JokeActions:
    def get(self) -> Joke:
        joke = requests.get('https://icanhazdadjoke.com', headers={"Accept": "application/json"}).json()
        # return {'joke': joke.json()['joke']}
        return Joke(**joke)


joke = JokeActions()
