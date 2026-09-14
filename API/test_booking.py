from idlelib.rpc import response_queue

from API.conftest import cleanup_booking
from utils.payloads.booking_payload import booking_payload
from utils.payloads.update_payload import update_payload
from utils.support.waiters import wait_until_deleted

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


