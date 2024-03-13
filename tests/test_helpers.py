import pytest

from repytile.exceptions import InvalidElementType
from repytile.helpers import text_node_to_html_node
from repytile.inline_elements import TextNode


def test_conversion_from_textnode_to_htmlnode_raise_error_if_type_not_allowed() -> None:
    with pytest.raises(InvalidElementType):
        text_node_to_html_node(TextNode(text="test", text_type="none"))


def test_textnode_to_htmlnode_raw_text():
    tn = TextNode(text="Hello World", text_type="text")
    result = text_node_to_html_node(tn)

    assert result.tag is None
    assert result.value == "Hello World"
    assert result.props == None


def test_textnode_to_htmlnode_bold_text():
    tn = TextNode(text="Bold Text", text_type="bold")
    result = text_node_to_html_node(tn)

    assert result.tag == "b"
    assert result.value == "Bold Text"
    assert result.props == {}


def test_textnode_to_htmlnode_italic_text():
    tn = TextNode(text="Italic Text", text_type="italic")
    result = text_node_to_html_node(tn)

    assert result.tag == "i"
    assert result.value == "Italic Text"
    assert result.props == {}


def test_textnode_to_htmlnode_code_block():
    tn = TextNode(text="Code Block", text_type="code")
    result = text_node_to_html_node(tn)

    assert result.tag == "code"
    assert result.value == "Code Block"
    assert result.props == {}


def test_textnode_to_htmlnode_link():
    tn = TextNode(text="Click Here", text_type="link", url="https://example.com")
    result = text_node_to_html_node(tn)

    assert result.tag == "a"
    assert result.value == "Click Here"
    assert result.props == {"href": "https://example.com"}


def test_textnode_to_htmlnode_image():
    tn = TextNode(
        text="Description", text_type="image", url="https://www.example.com/image.png"
    )
    result = text_node_to_html_node(tn)

    assert result.tag == "img"
    assert result.value == "Description"
    assert result.props == {
        "src": "https://www.example.com/image.png",
        "alt": "Description",
    }
