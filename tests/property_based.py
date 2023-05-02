import schemathesis

from api.main import app

schema = schemathesis.from_asgi("/openapi.json", app)


@schema.parametrize()
def test_api(case):
    response = case.call_asgi()
    #if response.status_code == 404:
    #    assert response.content == b'{"detail":"No names available"}'
    #else:
    case.validate_response(response)