import os
from urllib import response

import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from utils.payloads.booking_payload import booking_payload
from utils.support.waiters import wait_until_deleted
import time

load_dotenv()


@pytest.fixture
def request_context():
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=os.getenv("BASE_URL")
        )

        yield request_context

        request_context.dispose()


@pytest.fixture
def auth_token(request_context):
    response = request_context.post("/auth", data={"username":"admin", "password":"password123"})
    body = response.json()
    return body["token"]

@pytest.fixture
def bookingid(request_context,cleanup_booking):
    response = request_context.post("/booking", data = booking_payload)

    assert response.status == 200


    booking_id = response.json()["bookingid"]

    yield booking_id

    # cleanup_booking já recebeu auth_token e request_context; aqui só
    # avisamos ela pra deletar esse ID. Por causa da ordem LIFO de
    # teardown do pytest, esse append roda ANTES do for de cleanup_booking,
    # então o delete de fato acontece.

    cleanup_booking.append(booking_id)


@pytest.fixture
def cleanup_booking(request_context, auth_token):
    created_ids = []

    yield created_ids

    for booking_id in created_ids:
        request_context.delete(
            f"/booking/{booking_id}",
            headers={"Cookie": f"token={auth_token}"}
        )

        aux = wait_until_deleted(request_context,booking_id, attempts=3, delay=1)

        assert aux





