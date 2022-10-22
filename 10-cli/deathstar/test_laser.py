from .laser import fire
from unittest import mock


class TestLaser:
    @mock.patch("deathstar.laser.rich", autospec=True)
    def test_fire_success(self, rich_mock):

        # let mock print return None
        rich_mock.print.return_value = None

        fire("Alderaan")

        assert rich_mock.print.called
        rich_mock.print.assert_called_once_with("💥 Firing laster at [red]Alderaan[/red]")
