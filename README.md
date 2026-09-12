# API Testing — Restful Booker

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-Testing-green?logo=pytest)
![Playwright](https://img.shields.io/badge/Playwright-API%20Testing-orange?logo=playwright)
![API](https://img.shields.io/badge/API-REST-lightgrey)

Automated API testing project developed with **Python, Pytest, and Playwright**, using the public Restful Booker API.

The project focuses on API test automation, authentication, CRUD operations, response validation, reusable fixtures, test data management, and automated cleanup.

## Technologies

* Python
* Pytest
* Playwright
* REST API
* JSON
* Git / GitHub

## Test Coverage

### Health Check

* API availability
* Status code validation
* Response body validation

### Authentication

* Authentication endpoint
* Token generation
* Cookie-based authentication

### Booking

* Create booking
* Get booking
* Update booking
* Partial update
* Delete booking
* Response validation
* Error scenarios

### Test Data

* Reusable payloads
* Dynamic booking IDs
* Pytest fixtures
* Automated test cleanup
* Retry strategy for transient API behavior

## Project Structure

```text
api-testing-restful-booker/
│
├── tests/
│   ├── test_health.py
│   ├── test_auth.py
│   └── test_booking.py
│
├── payloads/
│   └── booking.py
│
├── conftest.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

Clone the repository:

```bash
git clone https://github.com/SEU-USUARIO/api-testing-restful-booker.git
cd api-testing-restful-booker
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
playwright install
```

Configure the environment variables:

```env
BASE_URL=https://restful-booker.herokuapp.com
```

## Running Tests

Run the complete test suite:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_booking.py -v
```

Run tests with output:

```bash
pytest -s
```

## Fixtures and Test Cleanup

The project uses Pytest fixtures to centralize API setup, authentication, and cleanup logic.

Bookings created during test execution are registered for cleanup and automatically deleted after the test finishes.

```text
Create booking
      ↓
Store booking ID
      ↓
Execute test
      ↓
Delete booking
      ↓
Verify resource was deleted
```

This approach helps prevent test data from accumulating in the API and improves test isolation.

## Example

```python
from utils.payloads.booking_payload import booking_payload
def test_create_booking(
    request_context,
    cleanup_booking
):
    response = request_context.post(
        "/booking",
        data=booking_payload
    )

    assert response.status == 200

    body = response.json()
    booking_id = body["bookingid"]

    cleanup_booking.append(booking_id)

    assert body["booking"] == booking_payload 
```

The test validates:

* HTTP status code
* Response JSON
* Booking data
* Generated resource ID
* Automatic cleanup

## Test Results

Example:

```text
============================= test session starts =============================

tests/test_health.py      PASSED
tests/test_auth.py       PASSED
tests/test_booking.py    PASSED

============================== XX passed in XXs ================================
```

The test suite is continuously evolving as new scenarios and validations are added.

## API Documentation

Restful Booker API documentation:

https://restful-booker.herokuapp.com/apidoc/index.html

Base URL:

```text
https://restful-booker.herokuapp.com
```

## Future Improvements

* [ ] Expand negative scenarios
* [ ] Add JSON Schema validation
* [ ] Add Pytest markers
* [ ] Add HTML test reports
* [ ] Add GitHub Actions
* [ ] Add CI/CD execution
* [ ] Improve test data generation
* [ ] Add API contract validation

## Purpose

This project is part of my **QA Automation portfolio**, focusing on practical API testing and automation.

It demonstrates experience with:

* API testing
* Test automation
* Python
* Pytest
* Playwright
* REST APIs
* Authentication
* Fixtures
* CRUD testing
* Response validation
* Test data management
* Test cleanup
* Retry strategies

## Author

**Renan**

Junior QA / Software Quality Analyst focused on software testing, API testing, and test automation.
