
def test_health(request_context):
    response = request_context.get("/ping")

    assert response.status == 201

    body = response.text()

    assert body.lower() == "created"





