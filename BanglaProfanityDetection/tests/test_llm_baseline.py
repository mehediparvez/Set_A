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


def test_parse_groq_response_reasoning_and_markdown():
    response = "<think>Comment 2 is an insult.</think>\n1. **non-toxic**\n2. Toxic\n3. Non_toxic"
    labels = _parse_groq_response(response, 3)
    assert labels == [0, 1, 0]


def test_parse_groq_response_unclosed_think_fails():
    # Reply cut off mid-reasoning: no labels, so the batch is retried rather than mis-scored
    assert _parse_groq_response("<think>Let me look at each comment", 2) is None
