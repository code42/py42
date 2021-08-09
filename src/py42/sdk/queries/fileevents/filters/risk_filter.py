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

    _term = "riskIndicatorNames"

    @staticmethod
    def choices():
        return (
            RiskIndicator.CloudDataExposures.choices()
            + RiskIndicator.CloudStorageUploads.choices()
            + RiskIndicator.CodeRepositoryUploads.choices()
            + RiskIndicator.EmailServiceUploads.choices()
            + RiskIndicator.ExternalDevices.choices()
            + RiskIndicator.FileCategories.choices()
            + RiskIndicator.MessagingServiceUploads.choices()
            + RiskIndicator.Other.choices()
            + RiskIndicator.SocialMediaUploads.choices()
            + RiskIndicator.UserBehavior.choices()
        )

    class CloudDataExposures:
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

    class CloudStorageUploads:
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

    class CodeRepositoryUploads:
        BITBUCKET = "Bitbucket upload"
        GITHUB = "GitHub upload"
        GITLAB = "GitLab upload"
        SOURCEFORGE = "SourceForge upload"
        STASH = "Stash upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.CodeRepositoryUploads)

    class EmailServiceUploads:
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
            return get_attribute_keys_from_class(RiskIndicator.EmailServiceUploads)

    class ExternalDevices:
        AIRDROP = "AirDrop"
        REMOVABLE_MEDIA = "Removable media"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.ExternalDevices)

    class FileCategories:
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

    class MessagingServiceUploads:
        FACEBOOK_MESSENGER = "Facebook Messenger upload"
        MICROSOFT_TEAMS = "Microsoft Teams upload"
        SLACK = "Slack upload"
        WHATSAPP = "WhatsApp upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.MessagingServiceUploads)

    class Other:
        OTHER = "Other destination"
        UNKNOWN = "Unknown destination"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.Other)

    class SocialMediaUploads:
        FACEBOOK = "Facebook upload"
        LINKEDIN = "LinkedIn upload"
        REDDIT = "Reddit upload"
        TWITTER = "Twitter upload"

        @staticmethod
        def choices():
            return get_attribute_keys_from_class(RiskIndicator.SocialMediaUploads)

    class UserBehavior:
        FILE_MISMATCH = "File mismatch"
        OFF_HOURS = "Off hours"
        REMOTE = "Remote"

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

    _term = "riskSeverity"

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    NO_RISK_INDICATED = "NO_RISK_INDICATED"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(RiskSeverity)
