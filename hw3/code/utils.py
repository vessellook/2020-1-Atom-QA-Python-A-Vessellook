import time
import random


def generate_segment_name(prefix: str = 'Сегмент'):
    return f'{prefix} {time.time()} {random.random()}'
