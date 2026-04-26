from datetime import datetime
def isHtmlFormat(datetimeStr):
    try:
        datetime.strptime(datetimeStr,"%Y-%m-%dT%H:%M")
        return True
    except ValueError:
        return False

def isSqlFormat(datetimeStr):
    try:
        datetime.strptime(datetimeStr,"%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False