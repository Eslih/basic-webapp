from random import randint

from ..schemas.cat import Cat

cats = [
    {
        "name": "garfield",
        "url": "https://i0.wp.com/vandaagindegeschiedenis.nl/wp-content/uploads-pvandag1/2013/06/garfield-560.jpg?ssl=1"
    },
    {
        "name": "grumpy cat",
        "url": "https://media.wired.com/photos/5cdefc28b2569892c06b2ae4/master/w_2560%2Cc_limit/Culture-Grumpy-Cat-487386121-2.jpg"
    },
]


class CatActions:
    def get(self) -> Cat:
        return Cat(**cats[randint(0, (len(cats)) - 1)])


cat = CatActions()
