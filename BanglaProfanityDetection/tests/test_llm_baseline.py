from src.llm_baseline import _parse_groq_response


def test_parse_groq_response_valid():
    response = "1. toxic\n2. non-toxic\n3. toxic"
    labels = _parse_groq_response(response, 3)
    assert labels == [1, 0, 1]


def test_parse_groq_response_wrong_count():
    response = "1. toxic\n2. non-toxic"
    labels = _parse_groq_response(response, 3)
    assert labels is None


def test_parse_groq_response_various_formats():
    response = "1) toxic\n2) non-toxic\n3) toxic"
    labels = _parse_groq_response(response, 3)
    assert labels == [1, 0, 1]

    response = "1: toxic\n2: non-toxic\n3: non toxic"
    labels = _parse_groq_response(response, 3)
    assert labels == [1, 0, 0]
