from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.util import get_attribute_keys_from_class


class RiskIndicator(FileEventFilterStringField):
    """Class that filters events by risk indicator.

    Available options are provided as class attributes:
        - :attr:`RiskIndicator.CloudDataExposures.PUBLIC_CORPORATE_BOX`
        - :attr:`RiskIndicator.CloudDataExposures.PUBLIC_CORPORATE_GOOGLE_DRIVE`
        - :attr:`RiskIndicator.CloudDataExposures.PUBLIC_CORPORATE_ONEDRIVE`
        - :attr:`RiskIndicator.CloudDataExposures.SENT_CORPORATE_GMAIL`
        - :attr:`RiskIndicator.CloudDataExposures.SHARED_CORPORATE_BOX`
        - :attr:`RiskIndicator.CloudDataExposures.SHARED_CORPORATE_GOOGLE_DRIVE`
        - :attr:`RiskIndicator.CloudDataExposures.SHARED_CORPORATE_ONEDRIVE`
        - :attr:`RiskIndicator.CloudStorageUploads.AMAZON_DRIVE`
        - :attr:`RiskIndicator.CloudStorageUploads.BOX`
        - :attr:`RiskIndicator.CloudStorageUploads.DROPBOX`
        - :attr:`RiskIndicator.CloudStorageUploads.GOOGLE_DRIVE`
        - :attr:`RiskIndicator.CloudStorageUploads.ICLOUD`
        - :attr:`RiskIndicator.CloudStorageUploads.MEGA`
        - :attr:`RiskIndicator.CloudStorageUploads.ONEDRIVE`
        - :attr:`RiskIndicator.CloudStorageUploads.ZOHO`
        - :attr:`RiskIndicator.CodeRepositoryUploads.BITBUCKET`
        - :attr:`RiskIndicator.CodeRepositoryUploads.GITHUB`
        - :attr:`RiskIndicator.CodeRepositoryUploads.GITLAB`
        - :attr:`RiskIndicator.CodeRepositoryUploads.SOURCEFORGE`
        - :attr:`RiskIndicator.CodeRepositoryUploads.STASH`
        - :attr:`RiskIndicator.EmailServiceUploads.ONESIXTHREE_DOT_COM`
        - :attr:`RiskIndicator.EmailServiceUploads.ONETWOSIX_DOT_COM`
        - :attr:`RiskIndicator.EmailServiceUploads.AOL`
        - :attr:`RiskIndicator.EmailServiceUploads.COMCAST`
        - :attr:`RiskIndicator.EmailServiceUploads.GMAIL`
        - :attr:`RiskIndicator.EmailServiceUploads.ICLOUD`
        - :attr:`RiskIndicator.EmailServiceUploads.MAIL_DOT_COM`
        - :attr:`RiskIndicator.EmailServiceUploads.OUTLOOK`
        - :attr:`RiskIndicator.EmailServiceUploads.PROTONMAIL`
        - :attr:`RiskIndicator.EmailServiceUploads.QQMAIL`
        - :attr:`RiskIndicator.EmailServiceUploads.SINA_MAIL`
        - :attr:`RiskIndicator.EmailServiceUploads.SOHU_MAIl`
        - :attr:`RiskIndicator.EmailServiceUploads.YAHOO`
        - :attr:`RiskIndicator.EmailServiceUploads.ZOHO_MAIL`
        - :attr:`RiskIndicator.RemovableMedia.AIRDROP`
        - :attr:`RiskIndicator.RemovableMedia.REMOVABLE_MEDIA`
        - :attr:`RiskIndicator.FileCategories.AUDIO`
        - :attr:`RiskIndicator.FileCategories.DOCUMENT`
        - :attr:`RiskIndicator.FileCategories.EXECUTABLE`
        - :attr:`RiskIndicator.FileCategories.IMAGE`
        - :attr:`RiskIndicator.FileCategories.PDF`
        - :attr:`RiskIndicator.FileCategories.PRESENTATION`
        - :attr:`RiskIndicator.FileCategories.SCRIPT`
        - :attr:`RiskIndicator.FileCategories.SOURCE_CODE`
        - :attr:`RiskIndicator.FileCategories.SPREADSHEET`
        - :attr:`RiskIndicator.FileCategories.VIDEO`
        - :attr:`RiskIndicator.FileCategories.VIRTUAL_DISK_IMAGE`
        - :attr:`RiskIndicator.FileCategories.ZIP`
        - :attr:`RiskIndicator.MessagingServiceUploads.FACEBOOK_MESSENGER`
        - :attr:`RiskIndicator.MessagingServiceUploads.MICROSOFT_TEAMS`
        - :attr:`RiskIndicator.MessagingServiceUploads.SLACK`
        - :attr:`RiskIndicator.MessagingServiceUploads.WHATSAPP`
        - :attr:`RiskIndicator.Other.OTHER`
        - :attr:`RiskIndicator.Other.UNKNOWN`
        - :attr:`RiskIndicator.SocialMediaUploads.FACEBOOK`
        - :attr:`RiskIndicator.SocialMediaUploads.LINKEDIN`
        - :attr:`RiskIndicator.SocialMediaUploads.REDDIT`
        - :attr:`RiskIndicator.SocialMediaUploads.TWITTER`
        - :attr:`RiskIndicator.UserBehavior.FILE_MISMATCH`
        - :attr:`RiskIndicator.UserBehavior.OFF_HOURS`
        - :attr:`RiskIndicator.UserBehavior.REMOTE`
    """

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
        AMAZON_DRIVE = u"Amazon Drive upload"
        BOX = u"Box upload"
        DROPBOX = u"Dropbox upload"
        GOOGLE_DRIVE = u"Google Drive upload"
        ICLOUD = u"iCloud upload"
        MEGA = u"Mega upload"
        ONEDRIVE = u"OneDrive upload"
        ZOHO = u"Zoho WorkDrive upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.CloudStorageUploads)

    class CodeRepositoryUploads(object):
        BITBUCKET = u"Bitbucket upload"
        GITHUB = u"GitHub upload"
        GITLAB = u"GitLab upload"
        SOURCEFORGE = u"SourceForge upload"
        STASH = u"Stash upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.CodeRepositoryUploads)

    class EmaiServiceUploads(object):
        ONESIXTHREE_DOT_COM = u"163.com upload"
        ONETWOSIX_DOT_COM = u"126.com upload"
        AOL = u"AOL upload"
        COMCAST = u"Comcast upload"
        GMAIL = u"Gmail upload"
        ICLOUD = u"iCloud Mail upload"
        MAIL_DOT_COM = u"Mail.com upload"
        OUTLOOK = u"Outlook upload"
        PROTONMAIL = u"ProtonMail upload"
        QQMAIL = u"QQMail upload"
        SINA_MAIL = u"Sina Mail upload"
        SOHU_MAIl = u"Sohu Mail upload"
        YAHOO = u"Yahoo upload"
        ZOHO_MAIL = u"Zoho Mail upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.EmaiServiceUploads)

    class ExternalDevices(object):
        AIRDROP = u"AirDrop"
        REMOVABLE_MEDIA = u"Removable media"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.ExternalDevices)

    class FileCategories(object):
        AUDIO = u"Audio"
        DOCUMENT = u"Document"
        EXECUTABLE = u"Executable"
        IMAGE = u"Image"
        PDF = u"PDF"
        PRESENTATION = u"Presentation"
        SCRIPT = u"Script"
        SOURCE_CODE = u"Source code"
        SPREADSHEET = u"Spreadsheet"
        VIDEO = u"Video"
        VIRTUAL_DISK_IMAGE = u"Virtual Disk Image"
        ZIP = u"Zip"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.FileCategories)

    class MessagingServiceUploads(object):
        FACEBOOK_MESSENGER = u"Facebook Messenger upload"
        MICROSOFT_TEAMS = u"Microsoft Teams upload"
        SLACK = u"Slack upload"
        WHATSAPP = u"WhatsApp upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.MessagingServiceUploads)

    class Other(object):
        OTHER = u"Other destination"
        UNKNOWN = u"Unknown destination"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.Other)

    class SocialMediaUploads(object):
        FACEBOOK = u"Facebook upload"
        LINKEDIN = u"LinkedIn upload"
        REDDIT = u"Reddit upload"
        TWITTER = u"Twitter upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.SocialMediaUploads)

    class UserBehavior(object):
        FILE_MISMATCH = u"File mismatch"
        OFF_HOURS = u"Off hours"
        REMOTE = u"Remote"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.UserBehavior)


class RiskSeverity(FileEventFilterStringField):
    """Class that filters events by risk severity.

    Available options are provided as class attributes:
        - :attr:`RiskSeverity.LOW`
        - :attr:`RiskSeverity.MODERATE`
        - :attr:`RiskSeverity.HIGH`
        - :attr:`RiskSeverity.CRITICAL`
        - :attr:`RiskSeverity.NO_RISK_INDICATED`
    """

    _term = u"riskSeverity"

    CRITICAL = u"CRITICAL"
    HIGH = u"HIGH"
    MODERATE = u"MODERATE"
    LOW = u"LOW"
    NO_RISK_INDICATED = u"NO_RISK_INDICATED"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(RiskSeverity)
