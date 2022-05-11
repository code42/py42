from py42.choices import Choices
from py42.sdk.queries.fileevents.util import _FileEventFilterComparableField
from py42.sdk.queries.fileevents.util import _FileEventFilterStringField
from py42.sdk.queries.query_filter import _QueryFilterBooleanField
from py42.sdk.queries.query_filter import _QueryFilterStringField


class Risk:
    class Indicators(_FileEventFilterStringField):
        """V2 filter class that filters events by the type of risk indicator.

        Available options are provided as class attributes:
            - :attr:`Indicators.CloudDataExposures.PUBLIC_CORPORATE_BOX`
            - :attr:`Indicators.CloudDataExposures.PUBLIC_CORPORATE_GOOGLE_DRIVE`
            - :attr:`Indicators.CloudDataExposures.PUBLIC_CORPORATE_ONEDRIVE`
            - :attr:`Indicators.CloudDataExposures.SENT_CORPORATE_GMAIL`
            - :attr:`Indicators.CloudDataExposures.SHARED_CORPORATE_BOX`
            - :attr:`Indicators.CloudDataExposures.SHARED_CORPORATE_GOOGLE_DRIVE`
            - :attr:`Indicators.CloudDataExposures.SHARED_CORPORATE_ONEDRIVE`
            - :attr:`Indicators.CloudStorageUploads.AMAZON_DRIVE`
            - :attr:`Indicators.CloudStorageUploads.BOX`
            - :attr:`Indicators.CloudStorageUploads.DROPBOX`
            - :attr:`Indicators.CloudStorageUploads.GOOGLE_DRIVE`
            - :attr:`Indicators.CloudStorageUploads.ICLOUD`
            - :attr:`Indicators.CloudStorageUploads.MEGA`
            - :attr:`Indicators.CloudStorageUploads.ONEDRIVE`
            - :attr:`Indicators.CloudStorageUploads.ZOHO`
            - :attr:`Indicators.CodeRepositoryUploads.BITBUCKET`
            - :attr:`Indicators.CodeRepositoryUploads.GITHUB`
            - :attr:`Indicators.CodeRepositoryUploads.GITLAB`
            - :attr:`Indicators.CodeRepositoryUploads.SOURCEFORGE`
            - :attr:`Indicators.CodeRepositoryUploads.STASH`
            - :attr:`Indicators.EmailServiceUploads.ONESIXTHREE_DOT_COM`
            - :attr:`Indicators.EmailServiceUploads.ONETWOSIX_DOT_COM`
            - :attr:`Indicators.EmailServiceUploads.AOL`
            - :attr:`Indicators.EmailServiceUploads.COMCAST`
            - :attr:`Indicators.EmailServiceUploads.GMAIL`
            - :attr:`Indicators.EmailServiceUploads.ICLOUD`
            - :attr:`Indicators.EmailServiceUploads.MAIL_DOT_COM`
            - :attr:`Indicators.EmailServiceUploads.OUTLOOK`
            - :attr:`Indicators.EmailServiceUploads.PROTONMAIL`
            - :attr:`Indicators.EmailServiceUploads.QQMAIL`
            - :attr:`Indicators.EmailServiceUploads.SINA_MAIL`
            - :attr:`Indicators.EmailServiceUploads.SOHU_MAIL`
            - :attr:`Indicators.EmailServiceUploads.YAHOO`
            - :attr:`Indicators.EmailServiceUploads.ZOHO_MAIL`
            - :attr:`Indicators.ExternalDevices.AIRDROP`
            - :attr:`Indicators.ExternalDevices.REMOVABLE_MEDIA`
            - :attr:`Indicators.FileCategories.AUDIO`
            - :attr:`Indicators.FileCategories.DOCUMENT`
            - :attr:`Indicators.FileCategories.EXECUTABLE`
            - :attr:`Indicators.FileCategories.IMAGE`
            - :attr:`Indicators.FileCategories.PDF`
            - :attr:`Indicators.FileCategories.PRESENTATION`
            - :attr:`Indicators.FileCategories.SCRIPT`
            - :attr:`Indicators.FileCategories.SOURCE_CODE`
            - :attr:`Indicators.FileCategories.SPREADSHEET`
            - :attr:`Indicators.FileCategories.VIDEO`
            - :attr:`Indicators.FileCategories.VIRTUAL_DISK_IMAGE`
            - :attr:`Indicators.FileCategories.ZIP`
            - :attr:`Indicators.MessagingServiceUploads.FACEBOOK_MESSENGER`
            - :attr:`Indicators.MessagingServiceUploads.MICROSOFT_TEAMS`
            - :attr:`Indicators.MessagingServiceUploads.SLACK`
            - :attr:`Indicators.MessagingServiceUploads.WHATSAPP`
            - :attr:`Indicators.Other.OTHER`
            - :attr:`Indicators.Other.UNKNOWN`
            - :attr:`Indicators.SocialMediaUploads.FACEBOOK`
            - :attr:`Indicators.SocialMediaUploads.LINKEDIN`
            - :attr:`Indicators.SocialMediaUploads.REDDIT`
            - :attr:`Indicators.SocialMediaUploads.TWITTER`
            - :attr:`Indicators.UserBehavior.FILE_MISMATCH`
            - :attr:`Indicators.UserBehavior.OFF_HOURS`
            - :attr:`Indicators.UserBehavior.REMOTE`
            - :attr:`Indicators.UserBehavior.FIRST_DESTINATION_USE`
            - :attr:`Indicators.UserBehavior.RARE_DESTINATION_USE`
        """

        _term = "risk.indicators.name"

        @staticmethod
        def choices():
            return (
                Risk.Indicators.CloudDataExposures.choices()
                + Risk.Indicators.CloudStorageUploads.choices()
                + Risk.Indicators.CodeRepositoryUploads.choices()
                + Risk.Indicators.EmailServiceUploads.choices()
                + Risk.Indicators.ExternalDevices.choices()
                + Risk.Indicators.FileCategories.choices()
                + Risk.Indicators.MessagingServiceUploads.choices()
                + Risk.Indicators.Other.choices()
                + Risk.Indicators.SocialMediaUploads.choices()
                + Risk.Indicators.UserBehavior.choices()
            )

        class CloudDataExposures(Choices):
            PUBLIC_CORPORATE_BOX = "Public link from corporate Box"
            PUBLIC_CORPORATE_GOOGLE_DRIVE = "Public link from corporate Google Drive"
            PUBLIC_CORPORATE_ONEDRIVE = "Public link from corporate OneDrive"
            SENT_CORPORATE_GMAIL = "Sent from corporate Gmail"
            SHARED_CORPORATE_BOX = "Shared from corporate Box"
            SHARED_CORPORATE_GOOGLE_DRIVE = "Shared from corporate Google Drive"
            SHARED_CORPORATE_ONEDRIVE = "Shared from corporate OneDrive"

        class CloudStorageUploads(Choices):
            AMAZON_DRIVE = "Amazon Drive upload"
            BOX = "Box upload"
            DROPBOX = "Dropbox upload"
            GOOGLE_DRIVE = "Google Drive upload"
            ICLOUD = "iCloud upload"
            MEGA = "Mega upload"
            ONEDRIVE = "OneDrive upload"
            ZOHO = "Zoho WorkDrive upload"

        class CodeRepositoryUploads(Choices):
            BITBUCKET = "Bitbucket upload"
            GITHUB = "GitHub upload"
            GITLAB = "GitLab upload"
            SOURCEFORGE = "SourceForge upload"
            STASH = "Stash upload"

        class EmailServiceUploads(Choices):
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

        class ExternalDevices(Choices):
            AIRDROP = "AirDrop"
            REMOVABLE_MEDIA = "Removable media"

        class FileCategories(Choices):
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

        class MessagingServiceUploads(Choices):
            FACEBOOK_MESSENGER = "Facebook Messenger upload"
            MICROSOFT_TEAMS = "Microsoft Teams upload"
            SLACK = "Slack upload"
            WHATSAPP = "WhatsApp upload"

        class Other(Choices):
            OTHER = "Other destination"
            UNKNOWN = "Unknown destination"

        class SocialMediaUploads(Choices):
            FACEBOOK = "Facebook upload"
            LINKEDIN = "LinkedIn upload"
            REDDIT = "Reddit upload"
            TWITTER = "Twitter upload"

        class UserBehavior(Choices):
            FILE_MISMATCH = "File mismatch"
            OFF_HOURS = "Off hours"
            REMOTE = "Remote"
            FIRST_DESTINATION_USE = "First use of destination"
            RARE_DESTINATION_USE = "Rare use of destination"

    class Severity(_FileEventFilterStringField, Choices):
        """V2 filter class that filters events by risk severity.

        Available options are provided as class attributes:
            - :attr:`Severity.LOW`
            - :attr:`Severity.MODERATE`
            - :attr:`Severity.HIGH`
            - :attr:`Severity.CRITICAL`
            - :attr:`Severity.NO_RISK_INDICATED`
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

    class TrustReason(_QueryFilterStringField, Choices):
        """V2 filter class that filters events based on the trust reason for the activity.

        Available options are provided as class attributes:
            - :attr: `TrustReason.TRUSTED_DOMAIN_BROWSER_URL`
            - :attr: `TrustReason.TRUSTED_BROWSER_URL_PATH`
            - :attr: `TrustReason.TRUSTED_DOMAIN_BROWSER_TAB_TITLE`
            - :attr: `TrustReason.TRUSTED_BROWSER_TAB_INFOS`
            - :attr: `TrustReason.TRUSTED_DOMAIN_EMAIL_RECIPIENT`
            - :attr: `TrustReason.TRUSTED_DOMAIN_CLOUD_SYNC_USERNAME`
            - :attr: `TrustReason.TRUSTED_SLACK_WORKSPACE`
            - :attr: `TrustReason.EVENT_PAIRING_SERVICE_MATCH`
            - :attr: `TrustReason.EVENT_PAIRING_SERVICE_ENDPOINT_MATCH`
            - :attr: `TrustReason.DOWNLOAD_TO_A_MANAGED_DEVICE`
            - :attr: `TrustReason.SHARED_WITH_TRUSTED_USERS`
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
