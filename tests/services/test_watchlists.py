
class TestWatchlistsService:

    def test_get_calls_get_with_expected_params(self, mock_connection):
        pass

    def test_get_raises_py42_not_found_when_id_not_found(self, mock_connection):
        pass

    def test_delete_calls_delete_with_expected_params(self, mock_connection):
        pass

    def test_delete_raises_py42_not_found_when_id_not_found(self, mock_connection):
        pass

    def test_list_watchlists_calls_get_with_expected_params(self, mock_connection):
        pass

    def test_list_watchlists_calls_get_with_optional_params(self, mock_connection):
        pass

    def test_create_calls_post_with_expected_params(self, mock_connection):
        pass

    def test_create_raises_py42_invalid_type_when_invalid_watchlist_type(self, mock_connection):
        pass

    def test_get_page_included_users_calls_get_with_expected_params(self, mock_connection):
        pass

    def test_get_all_included_users_calls_get_page_with_expected_params(self, mock_connection):
        pass

    def test_add_included_users_by_watchlist_id_calls_post_with_expected_params(self, mock_connection):
        pass

    def test_add_included_users_by_watchlist_id_raises_py42_not_found_when_id_not_found(self, mock_connection):
        pass

    def test_add_included_users_by_watchlist_type_calls_add_with_expected_params_when_watchlist_exists(self, mock_connection):
        pass

    def test_add_included_users_by_watchlist_type_creates_watchlist_and_calls_with_expected_params_when_watchlist_does_not_exist(self, mock_connection):
        pass

    def test_delete_included_users_by_watchlist_id_calls_post_with_expected_params(self, mock_connection):
        pass

    def test_delete_included_users_by_watchlist_id_raises_py42_not_found_when_id_not_found(self, mock_connection):
        pass

    def test_delete_included_users_by_watchlist_type_calls_add_with_expected_params_when_watchlist_exists(self, mock_connection):
        pass

    def test_delete_included_users_by_watchlist_type_creates_watchlist_and_calls_with_expected_params_when_watchlist_does_not_exist(self, mock_connection):
        pass

    def test_get_page_members_calls_get_with_expected_params(self, mock_connection):
        pass

    def test_get_all_members_calls_get_page_with_expected_params(self, mock_connection):
        pass

    def test_get_watchlist_member_calls_get_with_expected_params(self, mock_connection):
        pass

    def test_get_watchlist_member_raises_py42_not_found_when_id_not_found(self, mock_connection):
        pass


