import pytest

from shelters.models import Address


@pytest.mark.django_db
def test_create_address(create_address, monkeypatch):
    def mocked_get_coords_by_city(address):
        return 1.0, 1.0

    fields = {"street": "Test", "zip_code": "55-555", "city": "test", "phone": "111222333"}
    monkeypatch.setattr("shelters.models.Address._get_coords_by_city", mocked_get_coords_by_city)
    address = create_address(**fields)

    assert Address.objects.count() == 1
    for k, v in fields.items():
        assert getattr(address, k) == v
    assert address.latitude == 1.0
    assert address.longitude == 1.0
