import pytest

from atakcots import CotConfig


@pytest.mark.parametrize(
    "attachment_paths",
    [None, [], "my_path", ["my_path"], ["path1", "path2"]],
)
def test_force_list(attachment_paths):
    config = CotConfig(
        uid="test",
        latitude=0.0,
        longitude=0.0,
        attachment_paths=attachment_paths
    )

    assert isinstance(config.attachment_paths, list)
    for path in config.attachment_paths:
        assert isinstance(path, str)
