from validators import validate_filename, validate_url


def test_validate_url_requires_http_scheme():
    assert validate_url("ftp://example.com/video") == "Enter a valid http or https URL."


def test_validate_url_accepts_https():
    assert validate_url("https://example.com/watch?v=abc") is None


def test_validate_filename_rejects_bad_characters():
    assert validate_filename('bad/name') == 'Do not use these characters: < > : " / \\ | ? *'


def test_validate_filename_accepts_simple_name():
    assert validate_filename("my-song-file") is None
