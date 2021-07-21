from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.util import get_attribute_keys_from_class


class RiskIndicator(FileEventFilterStringField):
    """Class that filters events by risk indicator."""

    _term = u"riskIndicatorNames"

    @staticmethod
    def choices():
        return (
            RiskIndicator.CloudDataExposures.choices()
            + RiskIndicator.CloudStorageUploads.choices()
            + RiskIndicator.CodeRepositoryUploads.choices()
            + RiskIndicator.EmaiServiceUploads.choices()
            + RiskIndicator.ExternalDevices.choices()
            + RiskIndicator.FileCategories.choices()
            + RiskIndicator.MessagingServiceUploads.choices()
            + RiskIndicator.Other.choices()
            + RiskIndicator.SocialMediaUploads.choices()
            + RiskIndicator.UserBehavior.choices()
        )

    class CloudDataExposures(object):
        PUBLIC_CORPORATE_BOX = "Public link from corporate Box"
        PUBLIC_CORPORATE_GOOGLE_DRIVE = "Public link from corporate Google Drive"
        PUBLIC_CORPORATE_ONEDRIVE = "Public link from corporate OneDrive"
        SENT_CORPORATE_GMAIL = "Sent from corporate Gmail"
        SHARED_CORPORATE_BOX = "Shared from corporate Box"
        SHARED_CORPORATE_GOOGLE_DRIVE = "Shared from corporate Google Drive"
        SHARED_CORPORATE_ONEDRIVE = "Shared from corporate OneDrive"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.CloudDataExposures)

    class CloudStorageUploads(object):
        AMAZON_DRIVE = "Amazon Drive upload"
        BOX = "Box upload"
        DROPBOX = "Dropbox upload"
        GOOGLE_DRIVE = "Google Drive upload"
        ICLOUD = "iCloud upload"
        MEGA = "Mega upload"
        ONEDRIVE = "OneDrive upload"
        ZOHO = "Zoho WorkDrive upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.CloudStorageUploads)

    class CodeRepositoryUploads(object):
        BITBUCKET = "Bitbucket upload"
        GITHUB = "GitHub upload"
        GITLAB = "GitLab upload"
        SOURCEFORGE = "SourceForge upload"
        STASH = "Stash upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.CodeRepositoryUploads)

    class EmaiServiceUploads(object):
        ONESIXTHREE_DOT_COM = "163.com upload"
        ONETWOSIX_DOT_COM = "126.com upload"
        AOL = "AOL upload"
        COMCAST = "Comcast upload"
        GMAIL = "Gmail upload"
        ICLOUD = "iCloud Mail upload"
        MAIL_DOT_COM = "Mail.com upload"
        OUTLOOK = "Outlook upload"
        PROTONMAIL = "ProtonMail upload"
        QQMAIL = "QQMail upload"
        SINA_MAIL = "Sina Mail upload"
        SOHU_MAIl = "Sohu Mail upload"
        YAHOO = "Yahoo upload"
        ZOHO_MAIL = "Zoho Mail upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.EmaiServiceUploads)

    class ExternalDevices(object):
        AIRDROP = "AirDrop"
        REMOVABLE_MEDIA = "Removable media"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.ExternalDevices)

    class FileCategories(object):
        AUDIO = "Audio"
        DOCUMENT = "Document"
        EXECUTABLE = "Executable"
        IMAGE = "Image"
        PDF = "PDF"
        PRESENTATION = "Presentation"
        SCRIPT = "Script"
        SOURCE_CODE = "Source code"
        SPREADSHEET = "Spreadsheet"
        VIDEO = "Video"
        VIRTUAL_DISK_IMAGE = "Virtual Disk Image"
        ZIP = "Zip"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.FileCategories)

    class MessagingServiceUploads(object):
        FACEBOOK_MESSENGER = "Facebook Messenger upload"
        MICROSOFT_TEAMS = "Microsoft Teams upload"
        SLACK = "Slack upload"
        WHATSAPP = "WhatsApp upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.MessagingServiceUploads)

    class Other(object):
        OTHER = "Other destination"
        UNKNOWN = "Unknown destination"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.Other)

    class SocialMediaUploads(object):
        FACEBOOK = "Facebook upload"
        LINKEDIN = "LinkedIn upload"
        REDDIT = "Reddit upload"
        TWITTER = "Twitter upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.SocialMediaUploads)

    class UserBehavior(object):
        FILE_MISMATCH = "File mismatch"
        OFF_HOURS = "Off hours"
        REMOTE = "Remote"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.UserBehavior)


class RiskSeverity(FileEventFilterStringField):
    """Class that filters events by risk severity."""

    _term = u"riskSeverity"
