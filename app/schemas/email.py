from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict


@dataclass
class ValueRange:
    """
    Represents a range of integer values with lower and upper bounds.

    Attributes:
        lo (int): The lower bound of the range.
        hi (int): The upper bound of the range.
    """
    lo: int
    hi: int


class EmailIn(BaseModel):
    """
    Schema for sending email input.

    Attributes:
        subject (str): The subject of the email.
        body (str): The body content of the email.
        msg_type (str): The type of the email message.
    """
    subject: str
    body: str
    msg_type: str

    model_config = ConfigDict(from_attributes=True)
