import pytest
import allure


@allure.feature('Create Booking')
@allure.story('Test successful booking creation')
def test_create_booking(api_client, booking_dates, generate_booking_random_data):
    booking_data = {
        **generate_booking_random_data,
        "bookingdates": booking_dates
    }

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
@allure.story('Test presence of bookingid in response')
def test_bookingid_in_response(api_client, booking_dates, generate_booking_random_data):
    booking_data = {
        **generate_booking_random_data,
        "bookingdates": booking_dates
    }

    with allure.step('Sending request for booking creation'):
        response = api_client.create_booking(booking_data)

    with allure.step('Verifying bookingid in response'):
        assert "bookingid" in response, "bookingid is missing in response"
