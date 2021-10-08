import uuid


# 20211004 KYB add 아이디 생성
def get_ID(prefix=None):
    if prefix:
        ID = f"{prefix}{uuid.uuid4()}"
    else:
        ID = f"{uuid.uuid4()}"
    return ID