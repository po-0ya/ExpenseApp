'''Private errors to handle some conflicts'''

class Error(Exception):
    pass

class RemoveCantUseWithAdd(Error):
    pass

class RemoveCantUseWithView(Error):
    pass

class AddCantUseWithView(Error):
    pass

class AddCantUseWithJson(Error):
    pass