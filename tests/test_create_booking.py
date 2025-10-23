import pytest
import allure
import requests
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature('Create Booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanov",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    with allure.step('Verifying response data matches request data'):
        assert response['booking']['firstname'] == booking_data['firstname'], 'firstname does not match with expected'
        assert response['booking']['lastname'] == booking_data['lastname'], 'lastname does not match with expected'
        assert response['booking']['totalprice'] == booking_data['totalprice'], 'totalprice does not match with expected'
        assert response['booking']['depositpaid'] == booking_data['depositpaid'], 'depositpaid does not match with expected'
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates'][
            'checkin'], 'checkin date does not match with expected'
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates'][
            'checkout'], 'checkout date does not match with expected'
        assert response['booking']['additionalneeds'] == booking_data[
            'additionalneeds'], 'additional needs does not match with expected'


@allure.feature('Create Booking')
@allure.story('Positive: creating booking with random data')
def test_create_booking_with_random_data(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    booking = response["booking"]

    with allure.step('Verifying response data matches request data'):
        assert booking["firstname"] == booking_data["firstname"], 'firstname does not match with expected'
        assert booking["lastname"] == booking_data["lastname"], 'lastname does not match with expected'
        assert booking["totalprice"] == booking_data["totalprice"], 'totalprice does not match with expected'
        assert booking["depositpaid"] == booking_data["depositpaid"], 'depositpaid does not match with expected'
        assert booking["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"], 'checkin date does not match with expected'
        assert booking["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"], 'checkout date does not match with expected'
        assert booking["additionalneeds"] == booking_data["additionalneeds"], 'additional needs does not match with expected'


@allure.feature('Create Booking')
@allure.story('Positive: checking presence of bookingid in response')
def test_bookingid_in_response(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    with allure.step('Verifying bookingid in response'):
        assert "bookingid" in response, "bookingid is missing in response"

    with allure.step('Checking type of bookingid'):
        assert isinstance(response["bookingid"], int), "bookingid is not an integer"


@allure.feature('Create Booking')
@allure.story('Positive: creating booking w/o additionalneeds')
def test_create_booking_without_additionalneeds(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data.copy()
    del booking_data["additionalneeds"]

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    with allure.step('Verifying response data does not contain additionalneeds'):
        assert "additionalneeds" not in response["booking"]


@allure.feature('Create Booking')
@allure.story('Positive: creating booking when checkout greater than checkin date')
def test_create_booking_with_wrong_logic_for_dates(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data.copy()
    booking_data["bookingdates"]["checkin"] = "2026-10-01"
    booking_data["bookingdates"]["checkout"] = "2025-10-01"

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    booking = response["booking"]

    with allure.step('Verifying response data'):
        assert booking["bookingdates"]["checkin"] == "2026-10-01", 'checkin date does not match with expected'
        assert booking["bookingdates"]["checkout"] == "2025-10-01", 'checkout date does not match with expected'


@allure.feature('Create Booking')
@allure.story('Positive: creating booking with wrong format of bookingdates')
def test_create_booking_with_wrong_logic_for_dates(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data.copy()
    booking_data["bookingdates"]["checkin"] = "2026/10/01"
    booking_data["bookingdates"]["checkout"] = "2025/10/01"

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    booking = response["booking"]

    with allure.step('Verifying response data'):
        assert booking["bookingdates"]["checkin"] == "2026-10-01", 'checkin date does not match with expected'
        assert booking["bookingdates"]["checkout"] == "2025-10-01", 'checkout date does not match with expected'


@allure.feature('Create Booking')
@allure.story('Positive: creating booking with depositpaid equals 0')
def test_depositpaid_equals_zero(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data.copy()
    booking_data["depositpaid"] = 0

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    booking = response["booking"]

    with allure.step('Verifying response data'):
        assert booking["depositpaid"] == False, "depositpaid is not False"


@allure.feature('Create Booking')
@allure.story('Positive: creating booking with depositpaid equals 1')
def test_depositpaid_equals_zero(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data.copy()
    booking_data["depositpaid"] = 1

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    booking = response["booking"]

    with allure.step('Verifying response data'):
        assert booking["depositpaid"] == True, "depositpaid is not True"


@allure.feature('Create Booking')
@allure.story('Positive: creating booking with depositpaid equals random number')
def test_depositpaid_equals_zero(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data.copy()
    booking_data["depositpaid"] = 456

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    booking = response["booking"]

    with allure.step('Verifying response data'):
        assert booking["depositpaid"] == True, "depositpaid is not True"


@allure.feature('Create Booking')
@allure.story('Positive: creating booking with totalprice = "123" (string with digits)')
def test_totalprice_string_with_digits(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data.copy()
    booking_data["totalprice"] = "123"

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    with allure.step('Verifying totalprice value in response'):
        assert response['booking']['totalprice'] == 123, 'totalprice does not match with expected'
        assert isinstance(response["booking"]["totalprice"], int), "bookingid is not an integer"


@allure.feature('Create Booking')
@allure.story('Positive: creating booking with totalprice negative')
def test_totalprice_negative(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data.copy()
    booking_data["totalprice"] = -75

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    with allure.step('Verifying totalprice value in response'):
        assert response["booking"]["totalprice"] == -75, 'totalprice does not match with expected'


@allure.feature('Create Booking')
@allure.story('Positive: creating booking with totalprice equals to invalid string')
def test_totalprice_invalid_string(api_client, generate_booking_random_data):
    booking_data = generate_booking_random_data.copy()
    booking_data["totalprice"] = "one_hundred"

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    with allure.step('Verifying totalprice value in response'):
        assert response["booking"]["totalprice"] is None
        assert "bookingid" in response


@allure.feature('Create Booking')
@allure.story('Negative: creating booking with totalprice equals null')
def test_totalprice_null(api_client, generate_booking_random_data, mocker):
    booking_data = generate_booking_random_data.copy()
    booking_data["totalprice"] = None
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error: totalprice cannot be null"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        f"{mock_response.status_code} Server Error: {mock_response.text}", response=mock_response
    )
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(requests.exceptions.HTTPError, match="500 Server Error: Internal Server Error: totalprice cannot be null"):
            api_client.create_booking(booking_data)


@allure.feature('Create Booking')
@allure.story('Negative: checking firstname equals int')
def test_firstname_equals_int(api_client, generate_booking_random_data, mocker):
    booking_data = generate_booking_random_data.copy()
    booking_data["firstname"] = 12345
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error: firstname cannot be a number"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        f"{mock_response.status_code} Server Error: {mock_response.text}", response=mock_response
    )
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(requests.exceptions.HTTPError,
                       match="500 Server Error: Internal Server Error: firstname cannot be a number"):
        api_client.create_booking(booking_data)


@allure.feature('Create Booking')
@allure.story('Negative: checking lastname equals int')
def test_lastname_equals_int(api_client, generate_booking_random_data, mocker):
    booking_data = generate_booking_random_data.copy()
    booking_data["lastname"] = 12345
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error: lastname cannot be a number"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        f"{mock_response.status_code} Server Error: {mock_response.text}", response=mock_response
    )
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(requests.exceptions.HTTPError,
                       match="500 Server Error: Internal Server Error: lastname cannot be a number"):
        api_client.create_booking(booking_data)


@allure.feature('Create Booking')
@allure.story('Negative: creating booking w/o obligatory fields')
@pytest.mark.parametrize(
    'obligatory_field',
    [
        'firstname',
        'lastname',
        'totalprice',
        'depositpaid',
        'bookingdates'
    ]
)
def test_create_booking_without_obligatory_fields(api_client, generate_booking_random_data, mocker, obligatory_field):
    booking_data = generate_booking_random_data.copy()
    del booking_data[obligatory_field]
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.text = f"Internal Server Error: Missing {obligatory_field} field"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        f"{mock_response.status_code} Server Error: {mock_response.text}", response=mock_response
    )
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(requests.exceptions.HTTPError, match=f"500 Server Error: Internal Server Error: Missing {obligatory_field} field"):
        api_client.create_booking(booking_data)