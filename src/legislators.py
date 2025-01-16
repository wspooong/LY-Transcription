import requests

from src.constants import LY_JSON_API, HEADER


class LegislatorInfo:
    def __init__(self, term: str = "11"):
        self.term = term

    def _create_legisrator_params(self):
        return {
            "id": "9",
            "selectTerm": self.term,
        }

    def run(self):
        response = requests.get(url=LY_JSON_API, params=self._create_legisrator_params(term=self), headers=HEADER)

        data = response.json()["jsonList"]

        return data
