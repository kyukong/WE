import uuid


# 20211004 KYB add 아이디 생성
def get_ID(prefix=None):
    uuid_str: str = str(uuid.uuid4()).replace('-', '')
    if prefix:
        ID = f"{prefix}{uuid_str}"
    else:
        ID = f"{uuid_str}"
    return ID
