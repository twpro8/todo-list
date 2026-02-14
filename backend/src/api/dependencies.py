from typing import Annotated

from fastapi import Depends


def get_current_user_id():
    user_id = 1
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]
