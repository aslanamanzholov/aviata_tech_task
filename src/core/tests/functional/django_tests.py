from django.test import Client
from requests import Response

API_URL: str = '/en/api/'


def test_django(db, client: Client) -> None:
    response: Response = client.get('')
    assert 404 == response.status_code


def test_api_root(db, client: Client) -> None:
    response: Response = client.get(API_URL)
    assert 404 == response.status_code
