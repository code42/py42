import pytest

from tests.integration.conftest import assert_successful_response

role = "Desktop User"


@pytest.mark.integration
class TestUser:
    def test_add_role(self, connection, new_user):
        response = connection.users.add_role(new_user["userId"], role)
        assert_successful_response(response)

    def test_get_by_uid(self, connection, new_user):
        response = connection.users.get_by_uid(new_user["userUid"])
        assert_successful_response(response)

    def test_get_roles(self, connection, new_user):
        response = connection.users.get_roles(new_user["userId"])
        assert_successful_response(response)

    def test_unblock(self, connection, new_user):
        response = connection.users.unblock(new_user["userId"])
        assert_successful_response(response)

    def test_block(self, connection, new_user):
        response = connection.users.block(new_user["userId"])
        assert_successful_response(response)

    def test_get_all(self, connection):
        response_gen = connection.users.get_all()
        for response in response_gen:
            assert_successful_response(response)

    def test_get_by_username(self, connection, new_user):
        response = connection.users.get_by_username(new_user["username"])
        assert_successful_response(response)

    def test_get_scim_data_by_uid(self, connection, new_user):
        response = connection.users.get_scim_data_by_uid(new_user["userUid"])
        assert_successful_response(response)

    def test_change_org_assignment(self, connection, new_user, org):
        response = connection.users.change_org_assignment(
            new_user["userId"], org["parentOrgId"]
        )
        assert_successful_response(response)

    def test_get_available_roles(self, connection):
        response = connection.users.get_available_roles()
        assert_successful_response(response)

    def test_get_current(self, connection):
        response = connection.users.get_current()
        assert_successful_response(response)

    @pytest.mark.skip("Fails when whole test suite is executed.")
    def test_deactivate(self, connection, new_user):
        response = connection.users.deactivate(new_user["userId"])
        assert_successful_response(response)

    def test_reactivate(self, connection, new_user):
        response = connection.users.get_roles(new_user["userId"])
        assert_successful_response(response)

    def test_get_by_id(self, connection, new_user):
        response = connection.users.get_by_id(new_user["userId"])
        assert_successful_response(response)

    def test_get_page(self, connection):
        response = connection.users.get_page(1)
        assert_successful_response(response)

    def test_remove_role(self, connection, new_user):
        response = connection.users.remove_role(new_user["userId"], role)
        assert_successful_response(response)
