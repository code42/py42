from py42.choices import _Choices
from py42.sdk.queries.fileevents.util import _FileEventFilterComparableField
from py42.sdk.queries.fileevents.util import _FileEventFilterStringField
from py42.sdk.queries.query_filter import _QueryFilterBooleanField
from py42.sdk.queries.query_filter import _QueryFilterStringField


class Indicators(_FileEventFilterStringField):
    """V2 filter class that filters events by the type of risk indicator.

    Available options are provided as class attributes:
        - :attr:`risk.Indicators.CloudDataExposures.PUBLIC_CORPORATE_BOX`
        - :attr:`risk.Indicators.CloudDataExposures.PUBLIC_CORPORATE_GOOGLE_DRIVE`
        - :attr:`risk.Indicators.CloudDataExposures.PUBLIC_CORPORATE_ONEDRIVE`
        - :attr:`risk.Indicators.CloudDataExposures.SENT_CORPORATE_GMAIL`
        - :attr:`risk.Indicators.CloudDataExposures.SHARED_CORPORATE_BOX`
        - :attr:`risk.Indicators.CloudDataExposures.SHARED_CORPORATE_GOOGLE_DRIVE`
        - :attr:`risk.Indicators.CloudDataExposures.SHARED_CORPORATE_ONEDRIVE`
        - :attr:`risk.Indicators.CloudStorageUploads.AMAZON_DRIVE`
        - :attr:`risk.Indicators.CloudStorageUploads.BOX`
        - :attr:`risk.Indicators.CloudStorageUploads.DROPBOX`
        - :attr:`risk.Indicators.CloudStorageUploads.GOOGLE_DRIVE`
        - :attr:`risk.Indicators.CloudStorageUploads.ICLOUD`
        - :attr:`risk.Indicators.CloudStorageUploads.MEGA`
        - :attr:`risk.Indicators.CloudStorageUploads.ONEDRIVE`
        - :attr:`risk.Indicators.CloudStorageUploads.ZOHO`
        - :attr:`risk.Indicators.CodeRepositoryUploads.BITBUCKET`
        - :attr:`risk.Indicators.CodeRepositoryUploads.GITHUB`
        - :attr:`risk.Indicators.CodeRepositoryUploads.GITLAB`
        - :attr:`risk.Indicators.CodeRepositoryUploads.SOURCEFORGE`
        - :attr:`risk.Indicators.CodeRepositoryUploads.STASH`
        - :attr:`risk.Indicators.EmailServiceUploads.ONESIXTHREE_DOT_COM`
        - :attr:`risk.Indicators.EmailServiceUploads.ONETWOSIX_DOT_COM`
        - :attr:`risk.Indicators.EmailServiceUploads.AOL`
        - :attr:`risk.Indicators.EmailServiceUploads.COMCAST`
        - :attr:`risk.Indicators.EmailServiceUploads.GMAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.ICLOUD`
        - :attr:`risk.Indicators.EmailServiceUploads.MAIL_DOT_COM`
        - :attr:`risk.Indicators.EmailServiceUploads.OUTLOOK`
        - :attr:`risk.Indicators.EmailServiceUploads.PROTONMAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.QQMAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.SINA_MAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.SOHU_MAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.YAHOO`
        - :attr:`risk.Indicators.EmailServiceUploads.ZOHO_MAIL`
        - :attr:`risk.Indicators.ExternalDevices.AIRDROP`
        - :attr:`risk.Indicators.ExternalDevices.REMOVABLE_MEDIA`
        - :attr:`risk.Indicators.FileCategories.AUDIO`
        - :attr:`risk.Indicators.FileCategories.DOCUMENT`
        - :attr:`risk.Indicators.FileCategories.EXECUTABLE`
        - :attr:`risk.Indicators.FileCategories.IMAGE`
        - :attr:`risk.Indicators.FileCategories.PDF`
        - :attr:`risk.Indicators.FileCategories.PRESENTATION`
        - :attr:`risk.Indicators.FileCategories.SCRIPT`
        - :attr:`risk.Indicators.FileCategories.SOURCE_CODE`
        - :attr:`risk.Indicators.FileCategories.SPREADSHEET`
        - :attr:`risk.Indicators.FileCategories.VIDEO`
        - :attr:`risk.Indicators.FileCategories.VIRTUAL_DISK_IMAGE`
        - :attr:`risk.Indicators.FileCategories.ZIP`
        - :attr:`risk.Indicators.MessagingServiceUploads.FACEBOOK_MESSENGER`
        - :attr:`risk.Indicators.MessagingServiceUploads.MICROSOFT_TEAMS`
        - :attr:`risk.Indicators.MessagingServiceUploads.SLACK`
        - :attr:`risk.Indicators.MessagingServiceUploads.WHATSAPP`
        - :attr:`risk.Indicators.Other.OTHER`
        - :attr:`risk.Indicators.Other.UNKNOWN`
        - :attr:`risk.Indicators.SocialMediaUploads.FACEBOOK`
        - :attr:`risk.Indicators.SocialMediaUploads.LINKEDIN`
        - :attr:`risk.Indicators.SocialMediaUploads.REDDIT`
        - :attr:`risk.Indicators.SocialMediaUploads.TWITTER`
        - :attr:`risk.Indicators.UserBehavior.FILE_MISMATCH`
        - :attr:`risk.Indicators.UserBehavior.OFF_HOURS`
        - :attr:`risk.Indicators.UserBehavior.REMOTE`
        - :attr:`risk.Indicators.UserBehavior.FIRST_DESTINATION_USE`
        - :attr:`risk.Indicators.UserBehavior.RARE_DESTINATION_USE`
    """

    _term = "risk.indicators.name"

    @staticmethod
    def choices():
        return (
            Indicators.CloudDataExposures.choices()
            + Indicators.CloudStorageUploads.choices()
            + Indicators.CodeRepositoryUploads.choices()
            + Indicators.EmailServiceUploads.choices()
            + Indicators.ExternalDevices.choices()
            + Indicators.FileCategories.choices()
            + Indicators.MessagingServiceUploads.choices()
            + Indicators.Other.choices()
            + Indicators.SocialMediaUploads.choices()
            + Indicators.UserBehavior.choices()
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


class Severity(_FileEventFilterStringField, _Choices):
    """V2 filter class that filters events by risk severity.

    Available options are provided as class attributes:
        - :attr:`risk.Severity.LOW`
        - :attr:`risk.Severity.MODERATE`
        - :attr:`risk.Severity.HIGH`
        - :attr:`risk.Severity.CRITICAL`
        - :attr:`risk.Severity.NO_RISK_INDICATED`
    """

    _term = "risk.severity"

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    NO_RISK_INDICATED = "NO_RISK_INDICATED"


class Score(_QueryFilterStringField, _FileEventFilterComparableField):
    """V2 filter class that filters events by risk score."""

    _term = "risk.score"


class Trusted(_QueryFilterBooleanField):
    """V2 filter class that filters events based on whether activity can be trusted."""

    _term = "risk.trusted"


class TrustReason(_QueryFilterStringField, _Choices):
    """V2 filter class that filters events based on the trust reason for the activity.

    Available options are provided as class attributes:
        - :attr: `risk.TrustReason.TRUSTED_DOMAIN_BROWSER_URL`
        - :attr: `risk.TrustReason.TRUSTED_BROWSER_URL_PATH`
        - :attr: `risk.TrustReason.TRUSTED_DOMAIN_BROWSER_TAB_TITLE`
        - :attr: `risk.TrustReason.TRUSTED_BROWSER_TAB_INFOS`
        - :attr: `risk.TrustReason.TRUSTED_DOMAIN_EMAIL_RECIPIENT`
        - :attr: `risk.TrustReason.TRUSTED_DOMAIN_CLOUD_SYNC_USERNAME`
        - :attr: `risk.TrustReason.TRUSTED_SLACK_WORKSPACE`
        - :attr: `risk.TrustReason.EVENT_PAIRING_SERVICE_MATCH`
        - :attr: `risk.TrustReason.EVENT_PAIRING_SERVICE_ENDPOINT_MATCH`
        - :attr: `risk.TrustReason.DOWNLOAD_TO_A_MANAGED_DEVICE`
        - :attr: `risk.TrustReason.SHARED_WITH_TRUSTED_USERS`
    """

    _term = "risk.trustReason"

    TRUSTED_DOMAIN_BROWSER_URL = "Trusted browser URL"
    TRUSTED_BROWSER_URL_PATH = "Trusted specific URL path"
    TRUSTED_DOMAIN_BROWSER_TAB_TITLE = "Trusted browser tab title"
    TRUSTED_BROWSER_TAB_INFOS = "Trusted browser URL and/or tab title"
    TRUSTED_DOMAIN_EMAIL_RECIPIENT = "Trusted email recipient"
    TRUSTED_DOMAIN_CLOUD_SYNC_USERNAME = "Trusted sync username"
    TRUSTED_SLACK_WORKSPACE = "Trusted Slack workspace"
    EVENT_PAIRING_SERVICE_MATCH = "Event matched with cloud activity"
    EVENT_PAIRING_SERVICE_ENDPOINT_MATCH = "Event matched with endpoint activity"
    DOWNLOAD_TO_A_MANAGED_DEVICE = "Download to a managed device"
    SHARED_WITH_TRUSTED_USERS = "Shared with trusted users"
