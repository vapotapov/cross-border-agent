from src import __version__

def test_version_exposed():
    assert __version__ == "0.1.0"
