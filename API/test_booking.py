from API.conftest import cleanup_booking
from utils.payloads.booking_payload import booking_payload

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