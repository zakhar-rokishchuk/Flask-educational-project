def test_request_example(client):
    response = client.get("/")
    assert b"<h2>Hello, World!</h2>" in response.data