from py42.sdk.queries.fileevents.filters.email_query import EmailRecipients, EmailSender
from ..conftest import EXISTS, IS, IS_IN, IS_NOT, NOT_EXISTS, NOT_IN


def test_email_recipients_exists_str_gives_correct_json_representation():
    _filter = EmailRecipients.exists()
    expected = EXISTS.format("emailRecipients")
    assert str(_filter) == expected


def test_email_recipients_not_exists_str_gives_correct_json_representation():
    _filter = EmailRecipients.not_exists()
    expected = NOT_EXISTS.format("emailRecipients")
    assert str(_filter) == expected


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
