from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterComparableField as _FileEventFilterComparableField,
)
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)
from py42.sdk.queries.fileevents.v2.filters.risk_indicator_terms import Destinations
from py42.sdk.queries.query_filter import (
    QueryFilterBooleanField as _QueryFilterBooleanField,
)
from py42.sdk.queries.query_filter import (
    QueryFilterStringField as _QueryFilterStringField,
)


class Indicators(_FileEventFilterStringField):
    """V2 filter class that filters events by the type of risk indicator.

    Available options are provided as class attributes:
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
        - :attr:`risk.Indicators.UserBehavior.FILE_MISMATCH`
        - :attr:`risk.Indicators.UserBehavior.OFF_HOURS`
        - :attr:`risk.Indicators.UserBehavior.REMOTE`
        - :attr:`risk.Indicators.UserBehavior.FIRST_DESTINATION_USE`
        - :attr:`risk.Indicators.UserBehavior.RARE_DESTINATION_USE`
        - :attr:`risk.Indicators.UserBehavior.CONTRACT`
        - :attr:`risk.Indicators.UserBehavior.DEPARTING`
        - :attr:`risk.Indicators.UserBehavior.ELEVATED_ACCESS`
        - :attr:`risk.Indicators.UserBehavior.FLIGHT_RISK`
        - :attr:`risk.Indicators.UserBehavior.HIGH_IMPACT`
        - :attr:`risk.Indicators.UserBehavior.HIGH_RISK`
        - :attr:`risk.Indicators.UserBehavior.PERFORMANCE_CONCERNS`
        - :attr:`risk.Indicators.UserBehavior.POOR_SECURITY_PRACTICES`
        - :attr:`risk.Indicators.UserBehavior.SUSPICIOUS_SYSTEM_ACTIVITY`
        - :attr:`risk.Indicators.CloudStorageUploads.AMAZON_DRIVE`
        - :attr:`risk.Indicators.CloudStorageUploads.BAIDU_NET_DISK_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.BOX`
        - :attr:`risk.Indicators.CloudStorageUploads.CRASHPLAN_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.DRAKE_PORTALS_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.DROPBOX`
        - :attr:`risk.Indicators.CloudStorageUploads.FILE_DOT_IO_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.FILESTACK_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.GOOGLE_DRIVE`
        - :attr:`risk.Indicators.CloudStorageUploads.OPEN_TEXT_HIGHTAIL_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.ICLOUD`
        - :attr:`risk.Indicators.CloudStorageUploads.MEGA`
        - :attr:`risk.Indicators.CloudStorageUploads.ONEDRIVE`
        - :attr:`risk.Indicators.CloudStorageUploads.SECURE_FIRM_PORTAL_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.SHAREFILE_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.SMART_VAULT_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.SUGAR_SYNC_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.WE_TRANSFER_UPLOAD`
        - :attr:`risk.Indicators.CloudStorageUploads.ZOHO`
        - :attr:`risk.Indicators.EmailServiceUploads.ONESIXTHREE_DOT_COM`
        - :attr:`risk.Indicators.EmailServiceUploads.ONETWOSIX_DOT_COM`
        - :attr:`risk.Indicators.EmailServiceUploads.AOL`
        - :attr:`risk.Indicators.EmailServiceUploads.COMCAST`
        - :attr:`risk.Indicators.EmailServiceUploads.FASTMAIL_UPLOAD`
        - :attr:`risk.Indicators.EmailServiceUploads.GMAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.GMX_UPLOAD`
        - :attr:`risk.Indicators.EmailServiceUploads.ICLOUD`
        - :attr:`risk.Indicators.EmailServiceUploads.LYCOS_UPLOAD`
        - :attr:`risk.Indicators.EmailServiceUploads.MAIL_DOT_COM_UPLOAD`
        - :attr:`risk.Indicators.EmailServiceUploads.OUTLOOK`
        - :attr:`risk.Indicators.EmailServiceUploads.PROTONMAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.QQMAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.SINA_MAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.SOHU_MAIL`
        - :attr:`risk.Indicators.EmailServiceUploads.TUTANOTA_UPLOAD`
        - :attr:`risk.Indicators.EmailServiceUploads.YAHOO`
        - :attr:`risk.Indicators.EmailServiceUploads.ZIX_UPLOAD`
        - :attr:`risk.Indicators.EmailServiceUploads.ZOHO_MAIL`
        - :attr:`risk.Indicators.ExternalDevices.AIRDROP`
        - :attr:`risk.Indicators.ExternalDevices.SALESFORCE_DOWNLOAD`
        - :attr:`risk.Indicators.ExternalDevices.REMOVABLE_MEDIA`
        - :attr:`Indicators.CloudDataExposures.PUBLIC_CORPORATE_BOX`
        - :attr:`Indicators.CloudDataExposures.PUBLIC_CORPORATE_GOOGLE_DRIVE`
        - :attr:`Indicators.CloudDataExposures.PUBLIC_CORPORATE_ONEDRIVE`
        - :attr:`Indicators.CloudDataExposures.SENT_CORPORATE_GMAIL`
        - :attr:`Indicators.CloudDataExposures.SENT_CORPORATE_OFFICE365`
        - :attr:`Indicators.CloudDataExposures.SHARED_CORPORATE_BOX`
        - :attr:`Indicators.CloudDataExposures.SHARED_CORPORATE_GOOGLE_DRIVE`
        - :attr:`Indicators.CloudDataExposures.SHARED_CORPORATE_ONEDRIVE`
        - :attr:`risk.Indicators.FileConversionToolUploads.CLOUD_CONVERT_UPLOAD`
        - :attr:`risk.Indicators.FileConversionToolUploads.COMPRESS_JPEG_UPLOAD`
        - :attr:`risk.Indicators.FileConversionToolUploads.FREE_CONVERT_UPLOAD`
        - :attr:`risk.Indicators.FileConversionToolUploads.HEIC_TO_JPEG_UPLOAD`
        - :attr:`risk.Indicators.FileConversionToolUploads.TINY_PNG_UPLOAD`
        - :attr:`risk.Indicators.MessagingServiceUploads.DISCORD_UPLOAD`
        - :attr:`risk.Indicators.MessagingServiceUploads.FACEBOOK_MESSENGER`
        - :attr:`risk.Indicators.MessagingServiceUploads.GOOGLE_MESSAGES_UPLOAD`
        - :attr:`risk.Indicators.MessagingServiceUploads.GOOGLE_CHAT_UPLOAD`
        - :attr:`risk.Indicators.MessagingServiceUploads.GOOGLE_HANGOUTS_UPLOAD`
        - :attr:`risk.Indicators.MessagingServiceUploads.MICROSOFT_TEAMS`
        - :attr:`risk.Indicators.MessagingServiceUploads.SLACK`
        - :attr:`risk.Indicators.MessagingServiceUploads.TELEGRAM_UPLOAD`
        - :attr:`risk.Indicators.MessagingServiceUploads.WEBEX_UPLOAD`
        - :attr:`risk.Indicators.MessagingServiceUploads.WE_CHAT_UPLOAD`
        - :attr:`risk.Indicators.MessagingServiceUploads.WHATSAPP`
        - :attr:`risk.Indicators.MessagingServiceUploads.ZOOM_UPLOAD`
        - :attr:`risk.Indicators.Other.OTHER_DESTINATION`
        - :attr:`risk.Indicators.Other.UNKNOWN_DESTINATION`
        - :attr:`risk.Indicators.PdfManagerUploads.ADOBE_ACROBAT_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.COMBINE_PDF_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.FREE_PDF_CONVERT_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.I_LOVE_PDF_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.JPG2_PDF_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.PDF24_TOOLS_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.PDF_ESCAPE_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.PDF_FILLER_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.PDF_SIMPLI_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.SEJDA_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.SMALL_PDF_UPLOAD`
        - :attr:`risk.Indicators.PdfManagerUploads.SODA_PDF_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.ADOBE_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.CANVA_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.EVERNOTE_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.FIGMA_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.GOOGLE_KEEP_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.GOOGLE_JAMBOARD_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.IMAGE_COLOR_PICKER_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.KAPWING_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.MIRO_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.MONDAY_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.MURAL_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.NOTION_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.OVERLEAF_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.PHOTOPEA_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.PIXLR_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.REMOVE_DOT_BG_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.TRELLO_UPLOAD`
        - :attr:`risk.Indicators.ProductivityToolUploads.VEED_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.FOUR_CHAN_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.FACEBOOK`
        - :attr:`risk.Indicators.SocialMediaUploads.IMGUR_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.LINKEDIN`
        - :attr:`risk.Indicators.SocialMediaUploads.ODNOKLASSNIKI_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.OK_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.QZONE_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.REDDIT`
        - :attr:`risk.Indicators.SocialMediaUploads.STACK_OVERFLOW_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.TUMBLR_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.TWITCH_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.TWITTER`
        - :attr:`risk.Indicators.SocialMediaUploads.VIMEO_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.VK_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.WEIBO_UPLOAD`
        - :attr:`risk.Indicators.SocialMediaUploads.YOU_TUBE_UPLOAD`
        - :attr:`risk.Indicators.CodeRepositoryUploads.BITBUCKET_UPLOAD`
        - :attr:`risk.Indicators.CodeRepositoryUploads.COLABORATORY_UPLOAD`
        - :attr:`risk.Indicators.CodeRepositoryUploads.GITHUB`
        - :attr:`risk.Indicators.CodeRepositoryUploads.GITLAB`
        - :attr:`risk.Indicators.CodeRepositoryUploads.GOOGLE_APPS_SCRIPT_UPLOAD`
        - :attr:`risk.Indicators.CodeRepositoryUploads.GOOGLE_CLOUD_SHELL_UPLOAD`
        - :attr:`risk.Indicators.CodeRepositoryUploads.SOURCE_FORGE`
        - :attr:`risk.Indicators.CodeRepositoryUploads.STASH`
        - :attr:`risk.Indicators.WebHostingUploads.GIT_HUB_PAGES_UPLOAD`
        - :attr:`risk.Indicators.WebHostingUploads.GOOGLE_SITES_UPLOAD`
        - :attr:`risk.Indicators.WebHostingUploads.WIX_UPLOAD`
        - :attr:`risk.Indicators.WebHostingUploads.WORD_PRESS_UPLOAD`
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
            + Indicators.FileConversionToolUploads.choices()
            + Indicators.PdfManagerUploads.choices()
            + Indicators.ProductivityToolUploads.choices()
            + Indicators.WebHostingUploads.choices()
        )

    class CloudDataExposures(_Choices):
        PUBLIC_CORPORATE_BOX = Destinations.PUBLIC_LINK_FROM_CORPORATE_BOX
        PUBLIC_CORPORATE_GOOGLE_DRIVE = (
            Destinations.PUBLIC_LINK_FROM_CORPORATE_GOOGLE_DRIVE
        )
        PUBLIC_CORPORATE_ONEDRIVE = Destinations.PUBLIC_LINK_FROM_CORPORATE_ONE_DRIVE
        SENT_CORPORATE_GMAIL = Destinations.SENT_FROM_CORPORATE_GMAIL
        SENT_CORPORATE_OFFICE365 = Destinations.SENT_FROM_CORPORATE_OFFICE365
        SHARED_CORPORATE_BOX = Destinations.SHARED_FROM_CORPORATE_BOX
        SHARED_CORPORATE_GOOGLE_DRIVE = Destinations.SHARED_FROM_CORPORATE_GOOGLE_DRIVE
        SHARED_CORPORATE_ONEDRIVE = Destinations.SHARED_FROM_CORPORATE_ONE_DRIVE

    class CloudStorageUploads(_Choices):
        AMAZON_DRIVE = Destinations.AMAZON_DRIVE_UPLOAD
        BAIDU_NET_DISK_UPLOAD = Destinations.BAIDU_NET_DISK_UPLOAD
        BOX = Destinations.BOX_UPLOAD
        CRASHPLAN_UPLOAD = Destinations.CRASHPLAN_UPLOAD
        DRAKE_PORTALS_UPLOAD = Destinations.DRAKE_PORTALS_UPLOAD
        DROPBOX = Destinations.DROPBOX_UPLOAD
        FILE_DOT_IO_UPLOAD = Destinations.FILE_DOT_IO_UPLOAD
        FILESTACK_UPLOAD = Destinations.FILESTACK_UPLOAD
        GOOGLE_DRIVE = Destinations.GOOGLE_DRIVE_UPLOAD
        OPEN_TEXT_HIGHTAIL_UPLOAD = Destinations.OPEN_TEXT_HIGHTAIL_UPLOAD
        ICLOUD = Destinations.ICLOUD_UPLOAD
        MEGA = Destinations.MEGA_UPLOAD
        ONEDRIVE = Destinations.ONE_DRIVE_UPLOAD
        SECURE_FIRM_PORTAL_UPLOAD = Destinations.SECURE_FIRM_PORTAL_UPLOAD
        SHAREFILE_UPLOAD = Destinations.SHAREFILE_UPLOAD
        SMART_VAULT_UPLOAD = Destinations.SMART_VAULT_UPLOAD
        SUGAR_SYNC_UPLOAD = Destinations.SUGAR_SYNC_UPLOAD
        WE_TRANSFER_UPLOAD = Destinations.WE_TRANSFER_UPLOAD
        ZOHO = Destinations.ZOHO_WORK_DRIVE_UPLOAD

    class CodeRepositoryUploads(_Choices):
        BITBUCKET = Destinations.BITBUCKET_UPLOAD
        COLABORATORY_UPLOAD = Destinations.COLABORATORY_UPLOAD
        GITHUB = Destinations.GIT_HUB_UPLOAD
        GITLAB_UPLOAD = Destinations.GIT_LAB_UPLOAD
        GOOGLE_APPS_SCRIPT_UPLOAD = Destinations.GOOGLE_APPS_SCRIPT_UPLOAD
        GOOGLE_CLOUD_SHELL_UPLOAD = Destinations.GOOGLE_CLOUD_SHELL_UPLOAD
        SOURCEFORGE = Destinations.SOURCE_FORGE_UPLOAD
        STASH = Destinations.STASH_UPLOAD

    class EmailServiceUploads(_Choices):
        ONESIXTHREE_DOT_COM = Destinations.ONE_SIX_THREE_DOT_COM_UPLOAD
        ONETWOSIX_DOT_COM = Destinations.ONE_TWO_SIX_DOT_COM_UPLOAD
        AOL = Destinations.AOL_UPLOAD
        COMCAST = Destinations.COMCAST_UPLOAD
        FASTMAIL_UPLOAD = Destinations.FASTMAIL_UPLOAD
        GMAIL = Destinations.GMAIL_UPLOAD
        GMX_UPLOAD = Destinations.GMX_UPLOAD
        ICLOUD = Destinations.ICLOUD_MAIL_UPLOAD
        LYCOS_UPLOAD = Destinations.LYCOS_UPLOAD
        MAIL_DOT_COM = Destinations.MAIL_COM_UPLOAD
        OUTLOOK = Destinations.OUTLOOK_UPLOAD
        PROTONMAIL = Destinations.PROTON_MAIL_UPLOAD
        QQMAIL = Destinations.QQMAIL_UPLOAD
        SINA_MAIL = Destinations.SINA_MAIL_UPLOAD
        SOHU_MAIL = Destinations.SOHU_MAIL_UPLOAD
        TUTANOTA_UPLOAD = Destinations.TUTANOTA_UPLOAD
        YAHOO = Destinations.YAHOO_UPLOAD
        ZIX_UPLOAD = Destinations.ZIX_UPLOAD
        ZOHO_MAIL = Destinations.ZOHO_MAIL_UPLOAD

    class ExternalDevices(_Choices):
        AIRDROP = Destinations.AIR_DROP
        SALES_FORCE_DOWNLOAD = Destinations.SALESFORCE_DOWNLOAD
        REMOVABLE_MEDIA = Destinations.REMOVABLE_MEDIA

    class MessagingServiceUploads(_Choices):
        DISCORD_UPLOAD = Destinations.DISCORD_UPLOAD
        FACEBOOK_MESSENGER = Destinations.FACEBOOK_MESSENGER_UPLOAD
        GOOGLE_MESSAGES_UPLOAD = Destinations.GOOGLE_MESSAGES_UPLOAD
        GOOGLE_CHAT_UPLOAD = Destinations.GOOGLE_CHAT_UPLOAD
        GOOGLE_HANGOUTS_UPLOAD = Destinations.GOOGLE_HANGOUTS_UPLOAD
        MICROSOFT_TEAMS = Destinations.MICROSOFT_TEAMS_UPLOAD
        SLACK = Destinations.SLACK_UPLOAD
        TELEGRAM_UPLOAD = Destinations.TELEGRAM_UPLOAD
        WEBEX_UPLOAD = Destinations.WEBEX_UPLOAD
        WE_CHAT_UPLOAD = Destinations.WE_CHAT_UPLOAD
        WHATSAPP = Destinations.WHATS_APP_UPLOAD
        ZOOM_UPLOAD = Destinations.ZOOM_UPLOAD

    class FileConversionToolUploads(_Choices):
        CLOUD_CONVERT_UPLOAD = Destinations.CLOUD_CONVERT_UPLOAD
        COMPRESS_JPEG_UPLOAD = Destinations.COMPRESS_JPEG_UPLOAD
        FREE_CONVERT_UPLOAD = Destinations.FREE_CONVERT_UPLOAD
        HEIC_TO_JPEG_UPLOAD = Destinations.HEIC_TO_JPEG_UPLOAD
        TINY_PNG_UPLOAD = Destinations.TINY_PNG_UPLOAD

    class PdfManagerUploads(_Choices):
        ADOBE_ACROBAT_UPLOAD = Destinations.ADOBE_ACROBAT_UPLOAD
        COMBINE_PDF_UPLOAD = Destinations.COMBINE_PDF_UPLOAD
        FREE_PDF_CONVERT_UPLOAD = Destinations.FREE_PDF_CONVERT_UPLOAD
        I_LOVE_PDF_UPLOAD = Destinations.I_LOVE_PDF_UPLOAD
        JPG2_PDF_UPLOAD = Destinations.JPG2_PDF_UPLOAD
        PDF24_TOOLS_UPLOAD = Destinations.PDF24_TOOLS_UPLOAD
        PDF_ESCAPE_UPLOAD = Destinations.PDF_ESCAPE_UPLOAD
        PDF_FILLER_UPLOAD = Destinations.PDF_FILLER_UPLOAD
        PDF_SIMPLI_UPLOAD = Destinations.PDF_SIMPLI_UPLOAD
        SEJDA_UPLOAD = Destinations.SEJDA_UPLOAD
        SMALL_PDF_UPLOAD = Destinations.SMALL_PDF_UPLOAD
        SODA_PDF_UPLOAD = Destinations.SODA_PDF_UPLOAD

    class ProductivityToolUploads(_Choices):
        ADOBE_UPLOAD = Destinations.ADOBE_UPLOAD
        CANVA_UPLOAD = Destinations.CANVA_UPLOAD
        EVERNOTE_UPLOAD = Destinations.EVERNOTE_UPLOAD
        FIGMA_UPLOAD = Destinations.FIGMA_UPLOAD
        GOOGLE_KEEP_UPLOAD = Destinations.GOOGLE_KEEP_UPLOAD
        GOOGLE_JAMBOARD_UPLOAD = Destinations.GOOGLE_JAMBOARD_UPLOAD
        IMAGE_COLOR_PICKER_UPLOAD = Destinations.IMAGE_COLOR_PICKER_UPLOAD
        KAPWING_UPLOAD = Destinations.KAPWING_UPLOAD
        MIRO_UPLOAD = Destinations.MIRO_UPLOAD
        MONDAY_UPLOAD = Destinations.MONDAY_UPLOAD
        MURAL_UPLOAD = Destinations.MURAL_UPLOAD
        NOTION_UPLOAD = Destinations.NOTION_UPLOAD
        OVERLEAF_UPLOAD = Destinations.OVERLEAF_UPLOAD
        PHOTOPEA_UPLOAD = Destinations.PHOTOPEA_UPLOAD
        PIXLR_UPLOAD = Destinations.PIXLR_UPLOAD
        REMOVE_DOT_BG_UPLOAD = Destinations.REMOVE_DOT_BG_UPLOAD
        TRELLO_UPLOAD = Destinations.TRELLO_UPLOAD
        VEED_UPLOAD = Destinations.VEED_UPLOAD

    class WebHostingUploads(_Choices):
        GIT_HUB_PAGES_UPLOAD = Destinations.GIT_HUB_PAGES_UPLOAD
        GOOGLE_SITES_UPLOAD = Destinations.GOOGLE_SITES_UPLOAD
        WIX_UPLOAD = Destinations.WIX_UPLOAD
        WORD_PRESS_UPLOAD = Destinations.WORD_PRESS_UPLOAD

    class Other(_Choices):
        OTHER = Destinations.OTHER_DESTINATION
        UNKNOWN = Destinations.UNKNOWN_DESTINATION

    class SocialMediaUploads(_Choices):
        FOUR_CHAN_UPLOAD = Destinations.FOUR_CHAN_UPLOAD
        FACEBOOK = Destinations.FACEBOOK_UPLOAD
        IMGUR_UPLOAD = Destinations.IMGUR_UPLOAD
        LINKEDIN = Destinations.LINKED_IN_UPLOAD
        ODNOKLASSNIKI_UPLOAD = Destinations.ODNOKLASSNIKI_UPLOAD
        OK_UPLOAD = Destinations.OK_UPLOAD
        QZONE_UPLOAD = Destinations.QZONE_UPLOAD
        REDDIT = Destinations.REDDIT_UPLOAD
        STACK_OVERFLOW_UPLOAD = Destinations.STACK_OVERFLOW_UPLOAD
        TUMBLR_UPLOAD = Destinations.TUMBLR_UPLOAD
        TWITCH_UPLOAD = Destinations.TWITCH_UPLOAD
        TWITTER = Destinations.TWITTER_UPLOAD
        VIMEO_UPLOAD = Destinations.VIMEO_UPLOAD
        VK_UPLOAD = Destinations.VK_UPLOAD
        WEIBO_UPLOAD = Destinations.WEIBO_UPLOAD
        YOU_TUBE_UPLOAD = Destinations.YOU_TUBE_UPLOAD

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

    class UserBehavior(_Choices):
        FILE_MISMATCH = "File mismatch"
        OFF_HOURS = "Off hours"
        REMOTE = "Remote"
        FIRST_DESTINATION_USE = "First use of destination"
        RARE_DESTINATION_USE = "Rare use of destination"
        CONTRACT = "Contract"
        DEPARTING = "Departing"
        ELEVATED_ACCESS = "Elevated access"
        FLIGHT_RISK = "Flight risk"
        HIGH_IMPACT = "High impact"
        HIGH_RISK = "High risk"
        PERFORMANCE_CONCERNS = "Performance concerns"
        POOR_SECURITY_PRACTICES = "Poor security practices"
        SUSPICIOUS_SYSTEM_ACTIVITY = "Suspicious system activity"


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


class IndicatorsWeight(_QueryFilterStringField, _FileEventFilterComparableField):
    """V2 filter class that filters events by the risk indicator weight."""

    _term = "risk.indicators.weight"
