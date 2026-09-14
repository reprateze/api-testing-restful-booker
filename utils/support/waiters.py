import time


def wait_until_deleted(request_context, booking_id, attempts=3, delay=1):
    for attempt in range(attempts):
        response = request_context.get(f"/booking/{booking_id}")
        if response.status == 404:
            return True
        time.sleep(delay)
    return False