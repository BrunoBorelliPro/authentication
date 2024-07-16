from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from authentication.auth import get_current_user
from authentication.database import get_session
from authentication.models import User

T_form_data = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]
T_current_user = Annotated[User, Depends(get_current_user)]
