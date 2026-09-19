from idlelib.rpc import response_queue
import pytest

from API.conftest import cleanup_booking, auth_token
from utils.payloads.booking_payload import booking_payload
from utils.payloads.update_payload import update_payload
from utils.support.waiters import wait_until_deleted
from utils.payloads.updarteparcial_payload import update_parcial_payload
import time

def test_usercreate(request_context, cleanup_booking):
    response = request_context.post(
        "/booking",
        data=booking_payload
    )

    body = response.json()

    print(body)

    assert response.status == 200
    assert body["booking"] == booking_payload

    booking_id = body["bookingid"]


    cleanup_booking.append(booking_id)

def test_bookingid_fixture(bookingid):
    print(bookingid)


def test_getbook(request_context, bookingid):
    response = request_context.get (f"/booking/{bookingid}")

    assert response.status == 200

    body = response.json()

    print(body)

    assert body == booking_payload

def test_updatebooking(request_context, bookingid, auth_token):
    response = request_context.put(
        f"/booking/{bookingid}",
        headers={"Cookie": f"token={auth_token}"},
        data=update_payload
    )
    assert response.status == 200

    body = response.json()

    assert body == update_payload

    response = request_context.get(f"/booking/{bookingid}")

    assert response.status == 200

    body = response.json()

    assert body == update_payload


def test_deletebooking(request_context, auth_token):
    response = request_context.post(
        "/booking",
        data=booking_payload
    )
    assert  response.status == 200

    body = response.json()
    booking_id = body["bookingid"]

    response = request_context.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )

    assert response.status in (200, 201)

    aux = wait_until_deleted(request_context, booking_id, attempts=3, delay=1)

    assert aux


def test_update_parcial(request_context, auth_token, bookingid):


    original_response = request_context.get(
        f"/booking/{bookingid}"
    )

    assert original_response.status == 200

    original_body = original_response.json()


    response = request_context.patch(
        f"/booking/{bookingid}",
        headers={"Cookie": f"token={auth_token}"},
        data=update_parcial_payload
    )


    assert response.status == 200

    updated_body = response.json()


    for field, expected_value in update_parcial_payload.items():
        assert updated_body[field] == expected_value


    for field, original_value in original_body.items():
        if field not in update_parcial_payload:
            assert updated_body[field] == original_value


    response = request_context.get(
        f"/booking/{bookingid}"
    )

    assert response.status == 200

    persisted_body = response.json()

    for field, expected_value in update_parcial_payload.items():
        assert persisted_body[field] == expected_value

def test_get_booking_inexistente(request_context):
    response = request_context.get(
        "/booking/{9999999999999999}"
    )

    assert response.status == 404


def test_update_without_token(request_context, bookingid):
    response = request_context.put(
        f"/booking/{bookingid}",
        data=update_payload
    )

    assert response.status == 403


@pytest.mark.parametrize("campo", [
    "firstname",
    "lastname",
    "totalprice",
    "depositpaid",
    "bookingdates"
])
def test_new_incomplete_booking(campo,request_context):

    payload = booking_payload.copy()
    payload.pop(campo)

    response = request_context.post(
        "/booking",
        data=payload
    )

    # API não valida corretamente payloads incompletos: ao invés de 400,
    # retorna 500

    assert response.status == 500




