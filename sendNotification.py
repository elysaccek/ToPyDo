from plyer import notification
from plyer.utils import platform

def sendNotification(app_name: str, title: str, message: str, timeout: int) -> int:
    try:
        notification.notify(
            app_name = app_name,
            title = title,
            message = message,
            app_icon = 'data/icon.{}'.format(
                '.ico' if platform == 'win' else 'png'
            ),
            timeout = timeout,
        )
        return 0
    except:
        return -1
    