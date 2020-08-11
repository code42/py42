# import base64
# import json
# import pytest
# from requests import Response
# from services._connection import Connection
# from py42.response import Py42Response
# from py42.services._auth import BasicAuthProvider
# from py42.services.storage._auth import FileArchiveTmpAuth, SecurityArchiveTmpAuth, \
#     V1Auth
# from py42.services._auth import V3Auth
# USERNAME = "username"
# PASSWORD = "password"
# HOST_ADDRESS = "https://test.code42.com"
# V1_TOKEN_PART1 = "partone"
# V1_TOKEN_PART2 = "parttwo"
# V3_TOKEN = "v3usertokenstring"
# TMP_LOGIN_TOKEN = "tmplogintokenstring"
# STORAGE_HOST_ADDRESS = "https://testsstorage.code42.com"
# STS_BASE_URL = "https://sts-east.us.code42.com"
# SERVER_ENV_EXCEPTION_MESSAGE = "Internal error in /api/ServerEnv"
# @pytest.fixture
# def v1_auth_provider(mocker):
#     auth_session = mocker.MagicMock(spec=Connection)
#     auth_session.host_address = HOST_ADDRESS
#     def mock_post(uri, **kwargs):
#         response = mocker.MagicMock(spec=Response)
#         response.text = json.dumps({"data": [V1_TOKEN_PART1, V1_TOKEN_PART2]})
#         response.status_code = 200
#         return Py42Response(response)
#     auth_session.post.side_effect = mock_post
#     provider = V1Auth(auth_session)
#     return provider
# @pytest.fixture
# def v3_auth_provider(mocker):
#     auth_session = mocker.MagicMock(spec=Connection)
#     auth_session.host_address = HOST_ADDRESS
#     def mock_get(uri, **kwargs):
#         response = mocker.MagicMock(spec=Response)
#         response.text = json.dumps({"data": {"v3_user_token": V3_TOKEN}})
#         response.status_code = 200
#         return Py42Response(response)
#     auth_session.get.side_effect = mock_get
#     provider = V3Auth(auth_session)
#     return provider
# @pytest.fixture
# def login_token_provider(mocker):
#     auth_session = mocker.MagicMock(spec=Connection)
#     auth_session.host_address = HOST_ADDRESS
#     def mock_post(uri, **kwargs):
#         response = mocker.MagicMock(spec=Response)
#         response.text = json.dumps(
#             {"data": {"loginToken": TMP_LOGIN_TOKEN, "serverUrl": STORAGE_HOST_ADDRESS}}
#         )
#         response.status_code = 200
#         return Py42Response(response)
#     auth_session.post.side_effect = mock_post
#     return FileArchiveTmpAuth(auth_session, "my", "device-guid", "destination-guid")
# @pytest.fixture
# def storage_auth_token_provider(mocker):
#     auth_session = mocker.MagicMock(spec=Connection)
#     auth_session.host_address = HOST_ADDRESS
#     def mock_post(uri, **kwargs):
#         response = mocker.MagicMock(spec=Response)
#         response.text = json.dumps(
#             {"data": {"loginToken": TMP_LOGIN_TOKEN, "serverUrl": STORAGE_HOST_ADDRESS}}
#         )
#         response.status_code = 200
#         return Py42Response(response)
#     auth_session.post.side_effect = mock_post
#     return SecurityArchiveTmpAuth(auth_session, "plan-id", "destination-guid")
# @pytest.fixture
# def mock_successful_server_env_get(mocker):
#     def mock_get(uri, **kwargs):
#         if uri == "/api/ServerEnv":
#             response = mocker.MagicMock(spec=Response)
#             response.text = json.dumps({"stsBaseUrl": STS_BASE_URL})
#             response.status_code = 200
#         elif uri == "/c42api/v3/auth/jwt":
#             response = mocker.MagicMock(spec=Response)
#             response.text = json.dumps({"data": {"v3_user_token": V3_TOKEN}})
#             response.status_code = 200
#         return Py42Response(response)
#     return mock_get
# @pytest.fixture
# def mock_unsuccessful_server_env_get(mocker):
#     def mock_get(uri, **kwargs):
#         response = mocker.MagicMock(spec=Response)
#         response.text = json.dumps({})
#         response.status_code = 200
#         return Py42Response(response)
#     return mock_get
# @pytest.fixture
# def mock_server_env_exception():
#     def mock_get(uri, **kwargs):
#         raise Exception(SERVER_ENV_EXCEPTION_MESSAGE)
#     return mock_get
# @pytest.fixture(scope="module")
# def basic_auth_provider():
#     return BasicAuthProvider(USERNAME, PASSWORD)
# def test_basic_provider_constructs_successfully():
#     assert BasicAuthProvider(USERNAME, PASSWORD)
# def test_basic_provider_secret_returns_base64_credentials(basic_auth_provider):
#     expected_credentials = "{}:{}".format(USERNAME, PASSWORD).encode("utf-8")
#     expected_b64_credentials = base64.b64encode(expected_credentials).decode("utf-8")
#     provider_credentials = basic_auth_provider.get_secret_value()
#     assert provider_credentials == expected_b64_credentials
# def test_v1_auth_provider_constructs_successfully(mocker):
#     auth_session = mocker.MagicMock(spec=Connection)
#     auth_session.host_address = HOST_ADDRESS
#     assert V1Auth(auth_session)
# def test_v1_auth_provider_secret_returns_v1_token(v1_auth_provider):
#     assert v1_auth_provider.get_secret_value() == "{}-{}".format(
#         V1_TOKEN_PART1, V1_TOKEN_PART2
#     )
# def test_v3_auth_provider_constructs_successfully(mocker):
#     auth_session = mocker.MagicMock(spec=Connection)
#     auth_session.host_address = HOST_ADDRESS
#     assert V3Auth(auth_session)
# def test_v3_auth_provider_secret_returns_v3_token(v3_auth_provider):
#     assert v3_auth_provider.get_secret_value() == V3_TOKEN
# def test_login_token_provider_constructs_successfully(mocker):
#     auth_session = mocker.MagicMock(spec=Connection)
#     auth_session.host_address = HOST_ADDRESS
#     assert FileArchiveTmpAuth(auth_session, "my", "device-guid", "destination-guid")
# def test_login_token_provider_secret_returns_tmp_login_token(login_token_provider):
#     assert login_token_provider.get_secret_value() == TMP_LOGIN_TOKEN
# def test_storage_auth_token_provider_constructs_successfully(mocker):
#     auth_session = mocker.MagicMock(spec=Connection)
#     auth_session.host_address = HOST_ADDRESS
#     assert SecurityArchiveTmpAuth(auth_session, "plan-id", "destination-guid")
# def test_storage_auth_token_provider_returns_tmp_login_token(
#     storage_auth_token_provider,
# ):
#     assert storage_auth_token_provider.get_secret_value() == TMP_LOGIN_TOKEN
# @pytest.mark.parametrize(
#     "tmp_token_provider",
#     ["login_token_provider", "storage_auth_token_provider"],
#     ids=["login_token_provider", "storage_auth_token_provider"],
# )
# def test_tmp_token_provider_uses_cache_after_get_login_info_called(
#     tmp_token_provider, request, mocker
# ):
#     tmp_token_provider = request.getfixturevalue(tmp_token_provider)
#     mocker.spy(tmp_token_provider, "get_tmp_auth_token")
#     tmp_token_provider.get_login_info()
#     assert (
#         tmp_token_provider.get_tmp_auth_token.call_count == 1
#     ), "get_tmp_auth_token never called"
#     tmp_token_provider.get_login_info()
#     call_count = tmp_token_provider.get_tmp_auth_token.call_count
#     message = "get_tmp_auth_token was called {} times, expected once".format(call_count)
#     assert call_count == 1, message
# @pytest.mark.parametrize(
#     "tmp_token_provider",
#     ["login_token_provider", "storage_auth_token_provider"],
#     ids=["login_token_provider", "storage_auth_token_provider"],
# )
# def test_tmp_token_provider_uses_cache_after_get_secret_value_called(
#     tmp_token_provider, request, mocker
# ):
#     tmp_token_provider = request.getfixturevalue(tmp_token_provider)
#     mocker.spy(tmp_token_provider, "get_tmp_auth_token")
#     tmp_token_provider.get_secret_value()
#     assert (
#         tmp_token_provider.get_tmp_auth_token.call_count == 1
#     ), "get_tmp_auth_token never called"
#     tmp_token_provider.get_secret_value()
#     call_count = tmp_token_provider.get_tmp_auth_token.call_count
#     message = "get_tmp_auth_token was called {} times, expected once".format(call_count)
#     assert call_count == 1, message
