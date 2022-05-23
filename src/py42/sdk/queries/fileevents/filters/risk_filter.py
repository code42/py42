from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterComparableField as _FileEventFilterComparableField,
)
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)
from py42.sdk.queries.query_filter import (
    QueryFilterStringField as _QueryFilterStringField,
)


class RiskIndicator(_FileEventFilterStringField):
    """V1 filter class that filters events by risk indicator.

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
        - :attr:`RiskIndicator.EmailServiceUploads.SOHU_MAIL`
        - :attr:`RiskIndicator.EmailServiceUploads.YAHOO`
        - :attr:`RiskIndicator.EmailServiceUploads.ZOHO_MAIL`
        - :attr:`RiskIndicator.ExternalDevices.AIRDROP`
        - :attr:`RiskIndicator.ExternalDevices.REMOVABLE_MEDIA`
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
        - :attr:`RiskIndicator.UserBehavior.FIRST_DESTINATION_USE`
        - :attr:`RiskIndicator.UserBehavior.RARE_DESTINATION_USE`
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

    class CloudDataExposures(_Choices):
        PUBLIC_CORPORATE_BOX = "Public link from corporate Box"
        PUBLIC_CORPORATE_GOOGLE_DRIVE = "Public link from corporate Google Drive"
        PUBLIC_CORPORATE_ONEDRIVE = "Public link from corporate OneDrive"
        SENT_CORPORATE_GMAIL = "Sent from corporate Gmail"
        SHARED_CORPORATE_BOX = "Shared from corporate Box"
        SHARED_CORPORATE_GOOGLE_DRIVE = "Shared from corporate Google Drive"
        SHARED_CORPORATE_ONEDRIVE = "Shared from corporate OneDrive"

    class CloudStorageUploads(_Choices):
        AMAZON_DRIVE = "Amazon Drive upload"
        BOX = "Box upload"
        DROPBOX = "Dropbox upload"
        GOOGLE_DRIVE = "Google Drive upload"
        ICLOUD = "iCloud upload"
        MEGA = "Mega upload"
        ONEDRIVE = "OneDrive upload"
        ZOHO = "Zoho WorkDrive upload"

    class CodeRepositoryUploads(_Choices):
        BITBUCKET = "Bitbucket upload"
        GITHUB = "GitHub upload"
        GITLAB = "GitLab upload"
        SOURCEFORGE = "SourceForge upload"
        STASH = "Stash upload"

    class EmailServiceUploads(_Choices):
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
        SOHU_MAIL = "Sohu Mail upload"
        YAHOO = "Yahoo upload"
        ZOHO_MAIL = "Zoho Mail upload"

    class ExternalDevices(_Choices):
        AIRDROP = "AirDrop"
        REMOVABLE_MEDIA = "Removable media"

    class FileCategories(_Choices):
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

    class MessagingServiceUploads(_Choices):
        FACEBOOK_MESSENGER = "Facebook Messenger upload"
        MICROSOFT_TEAMS = "Microsoft Teams upload"
        SLACK = "Slack upload"
        WHATSAPP = "WhatsApp upload"

    class Other(_Choices):
        OTHER = "Other destination"
        UNKNOWN = "Unknown destination"

    class SocialMediaUploads(_Choices):
        FACEBOOK = "Facebook upload"
        LINKEDIN = "LinkedIn upload"
        REDDIT = "Reddit upload"
        TWITTER = "Twitter upload"

    class UserBehavior(_Choices):
        FILE_MISMATCH = "File mismatch"
        OFF_HOURS = "Off hours"
        REMOTE = "Remote"
        FIRST_DESTINATION_USE = "First use of destination"
        RARE_DESTINATION_USE = "Rare use of destination"


class RiskSeverity(_FileEventFilterStringField, _Choices):
    """V1 filter class that filters events by risk severity.

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


class RiskScore(_QueryFilterStringField, _FileEventFilterComparableField):
    """V1 filter class that filters events by risk score."""

    _term = "riskScore"
