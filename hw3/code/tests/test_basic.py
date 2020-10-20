import pytest

from api.my_target_client import MyTargetClient
from utils import generate_segment_name


@pytest.mark.API
def test_auth(my_target_client: MyTargetClient):
    pass


@pytest.mark.API
# for multithreading
@pytest.mark.parametrize("prefix", ["first", "second", "third"])
def test_create(my_target_client: MyTargetClient, prefix: str):
    segment_name = generate_segment_name(prefix)
    segment_id = my_target_client.create_segment(segment_name)
    assert my_target_client.has_segment(segment_id)


@pytest.mark.API
# for multithreading
@pytest.mark.parametrize("prefix", ["first", "second", "third"])
def test_delete(my_target_client: MyTargetClient, prefix: str):
    segment_name = generate_segment_name(prefix)
    segment_id = my_target_client.create_segment(segment_name)
    my_target_client.delete_segment(segment_id)
    assert not my_target_client.has_segment(segment_id)
