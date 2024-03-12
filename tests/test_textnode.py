import pytest
from repytile.inline_elements import TextNode


def test_textnode_is_created_without_url() -> None:
    text_node = TextNode(text="text", text_type="type")

    assert text_node.text == "text"
    assert text_node.text_type == "type"
    assert text_node.url is None


def test_textnode_is_created_with_url() -> None:
    text_node = TextNode(text="text", text_type="type", url="https://www.example.com")

    assert text_node.text == "text"
    assert text_node.text_type == "type"
    assert text_node.url == "https://www.example.com"


@pytest.mark.parametrize(
    "text_nodes,expected",
    [
        pytest.param(
            (TextNode("text", "type"), TextNode("text", "type")), True, id="both_equal"
        ),
        pytest.param(
            (TextNode("text", "type"), TextNode("text1", "type")),
            False,
            id="both_different",
        ),
    ],
)
def test_textnode_eq_method_evaluates_correctly(
    text_nodes: tuple[TextNode, TextNode], expected: bool
) -> None:
    tn1, tn2 = text_nodes

    assert (tn1 == tn2) is expected


@pytest.mark.parametrize(
    "text_node,expected",
    [
        pytest.param(
            TextNode("text", "type"), "TextNode(text, type, None)", id="without_url"
        ),
        pytest.param(
            TextNode("text", "type", "url"), "TextNode(text, type, url)", id="with_url"
        ),
    ],
)
def test_text_repr_follows_expected_format(text_node: TextNode, expected: str) -> None:
    assert str(text_node) == expected
