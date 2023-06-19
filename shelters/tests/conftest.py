import pytest

from shelters.models import Address


@pytest.fixture()
def create_address():
    def create(street="street", zip_code="12-345", city="city", phone="123456789"):
        address = Address.objects.create(street=street, zip_code=zip_code, city=city, phone=phone)
        return address

    return create
