from dataclasses import dataclass
from typing import Optional

time_difference = 5


@dataclass
class Record:
    username: str
    email: str
    password: str
    access: int
    active: int
    start_active_time: Optional[float]

    def __eq__(self, record: Optional['Record']):
        if not isinstance(record, Record):
            return False
        if self.start_active_time is not None and record.start_active_time is not None:
            difference = abs(self.start_active_time - record.start_active_time)
            start_time_equal = difference <= time_difference
        else:
            start_time_equal = self.start_active_time is None and record.start_active_time is None

        return (self.username == record.username
                and self.email == record.email
                and self.password == record.password
                and self.access == record.access
                and self.active == record.active
                and start_time_equal)
