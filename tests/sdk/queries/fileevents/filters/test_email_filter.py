from tests.sdk.queries.conftest import IS
from tests.sdk.queries.conftest import IS_IN
from tests.sdk.queries.conftest import IS_NOT
from tests.sdk.queries.conftest import NOT_IN

from py42.sdk.queries.fileevents.filters.email_filter import EmailFrom
from py42.sdk.queries.fileevents.filters.email_filter import EmailPolicyName
from py42.sdk.queries.fileevents.filters.email_filter import EmailRecipients
from py42.sdk.queries.fileevents.filters.email_filter import EmailSender
from py42.sdk.queries.fileevents.filters.email_filter import EmailSubject


def test_email_recipients_eq_str_gives_correct_json_representation():
    _filter = EmailRecipients.eq("test_recipient")
    expected = IS.format("emailRecipients", "test_recipient")
    assert str(_filter) == expected


def test_email_recipients_not_eq_str_gives_correct_json_representation():
    _filter = EmailRecipients.not_eq("test_recipient")
    expected = IS_NOT.format("emailRecipients", "test_recipient")
    assert str(_filter) == expected


def test_email_recipients_is_in_str_gives_correct_json_representation():
    items = ["EmailRecipients1", "EmailRecipients2", "EmailRecipients3"]
    _filter = EmailRecipients.is_in(items)
    expected = IS_IN.format("emailRecipients", *items)
    assert str(_filter) == expected


def test_email_recipients_not_in_str_gives_correct_json_representation():
    items = ["EmailRecipients1", "EmailRecipients2", "EmailRecipients3"]
    _filter = EmailRecipients.not_in(items)
    expected = NOT_IN.format("emailRecipients", *items)
    assert str(_filter) == expected


def test_email_sender_eq_str_gives_correct_json_representation():
    _filter = EmailSender.eq("test_category")
    expected = IS.format("emailSender", "test_category")
    assert str(_filter) == expected


def test_email_sender_not_eq_str_gives_correct_json_representation():
    _filter = EmailSender.not_eq("test_category")
    expected = IS_NOT.format("emailSender", "test_category")
    assert str(_filter) == expected


def test_email_sender_is_in_str_gives_correct_json_representation():
    items = ["email_sender1", "email_sender2", "email_sender3"]
    _filter = EmailSender.is_in(items)
    expected = IS_IN.format("emailSender", *items)
    assert str(_filter) == expected


def test_email_sender_not_in_str_gives_correct_json_representation():
    items = ["email_sender1", "email_sender2", "email_sender3"]
    _filter = EmailSender.not_in(items)
    expected = NOT_IN.format("emailSender", *items)
    assert str(_filter) == expected


def test_email_subject_eq_str_gives_correct_json_representation():
    _filter = EmailSubject.eq("test_subject")
    expected = IS.format("emailSubject", "test_subject")
    assert str(_filter) == expected


def test_email_subject_not_eq_str_gives_correct_json_representation():
    _filter = EmailSubject.not_eq("test_subject")
    expected = IS_NOT.format("emailSubject", "test_subject")
    assert str(_filter) == expected


def test_email_subject_is_in_str_gives_correct_json_representation():
    items = ["test_subject1", "test_subject2", "test_subject3"]
    _filter = EmailSubject.is_in(items)
    expected = IS_IN.format("emailSubject", *items)
    assert str(_filter) == expected


def test_email_subject_not_in_str_gives_correct_json_representation():
    items = ["test_subject1", "test_subject2", "test_subject3"]
    _filter = EmailSubject.not_in(items)
    expected = NOT_IN.format("emailSubject", *items)
    assert str(_filter) == expected


def test_email_policy_name_eq_str_gives_correct_json_representation():
    _filter = EmailPolicyName.eq("test_policy")
    expected = IS.format("emailDlpPolicyNames", "test_policy")
    assert str(_filter) == expected


def test_email_policy_name_not_eq_str_gives_correct_json_representation():
    _filter = EmailPolicyName.not_eq("test_policy")
    expected = IS_NOT.format("emailDlpPolicyNames", "test_policy")
    assert str(_filter) == expected


def test_email_policy_name_is_in_str_gives_correct_json_representation():
    items = ["test_policy1", "test_policy2", "test_policy3"]
    _filter = EmailPolicyName.is_in(items)
    expected = IS_IN.format("emailDlpPolicyNames", *items)
    assert str(_filter) == expected


def test_email_policy_name_not_in_str_gives_correct_json_representation():
    items = ["test_policy1", "test_policy2", "test_policy3"]
    _filter = EmailPolicyName.not_in(items)
    expected = NOT_IN.format("emailDlpPolicyNames", *items)
    assert str(_filter) == expected


def test_email_from_eq_str_gives_correct_json_representation():
    _filter = EmailFrom.eq("email_from")
    expected = IS.format("emailFrom", "email_from")
    assert str(_filter) == expected


def test_email_from_not_eq_str_gives_correct_json_representation():
    _filter = EmailFrom.not_eq("email_from")
    expected = IS_NOT.format("emailFrom", "email_from")
    assert str(_filter) == expected


def test_email_from_is_in_str_gives_correct_json_representation():
    items = ["email_from1", "email_from2", "email_from3"]
    _filter = EmailFrom.is_in(items)
    expected = IS_IN.format("emailFrom", *items)
    assert str(_filter) == expected


def test_email_from_not_in_str_gives_correct_json_representation():
    items = ["email_from1", "email_from2", "email_from3"]
    _filter = EmailFrom.not_in(items)
    expected = NOT_IN.format("emailFrom", *items)
    assert str(_filter) == expected
