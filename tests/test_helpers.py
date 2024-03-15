import pytest

from repytile.exceptions import InvalidElementType
from repytile.helpers import _split_keep, split_nodes_delimiter, text_node_to_html_node
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


def test_split_textnodes_raises_exception_on_invalid_textnode_type() -> None:
    with pytest.raises(InvalidElementType):
        split_nodes_delimiter(
            old_nodes=[TextNode("test", text_type="none")],
            delimiter=".",
            text_type="type",
        )


@pytest.mark.parametrize(
    "input_str,sep,expected",
    [
        pytest.param(
            "This has **bold** text",
            "**",
            ["This has ", "**bold**", " text"],
            id="bold-text",
        ),
        pytest.param(
            "apple*banana*cherry",
            "*",
            ["apple", "*banana*", "cherry"],
            id="italic-text",
        ),
        pytest.param(
            "`code` block",
            "`",
            ["`code`", " block"],
            id="code-block",
        ),
    ],
)
def test_split_with_delimiters_keeps_separator(
    input_str: str, sep: str, expected: list[str]
) -> None:
    assert _split_keep(input_str, sep) == expected


@pytest.mark.parametrize(
    "input_str,sep,expected",
    [
        pytest.param(
            "This has **bold text",
            "**",
            ["This has **bold text"],
            id="bold-sep",
        ),
        pytest.param(
            "apple*banana cherry",
            "*",
            ["apple*banana cherry"],
            id="italic-sep",
        ),
        pytest.param(
            "code` block",
            "`",
            ["code` block"],
            id="code-sep",
        ),
    ],
)
def test_split_with_delimiters_only_splits_when_separator_pairs_exist(
    input_str: str, sep: str, expected: list[str]
) -> None:
    result = _split_keep(input_str, sep)
    assert len(result) == 1
    assert result == expected


@pytest.mark.parametrize(
    "input_str,sep,expected",
    [
        pytest.param(
            "This has **bold** text and *italic*",
            "**",
            ["This has ", "**bold**", " text and *italic*"],
            id="bold-text-with-italic-after",
        ),
        pytest.param(
            "This has **bold with *italic* text**",
            "**",
            ["This has ", "**bold**", " text and *italic*"],
            id="bold-text-with-italic-inside",
        ),
    ],
)
def test_split_with_multiple_text_types_only_handles_passed_separator(
    input_str: str, sep: str, expected: list[str]
) -> None:
    assert _split_keep(input_str, sep) == expected


@pytest.mark.parametrize(
    "input_str,sep,expected",
    [
        pytest.param(
            "This has **bold** text and more **bolder** text",
            "**",
            ["This has ", "**bold**", " text and more ", "**bolder**", " text"],
            id="multiple-bold-text",
        ),
        pytest.param(
            "This has **bold** **bolder** text",
            "**",
            ["This has ", "**bold**", " ", "**bolder**", " text"],
            id="consecultive-bold-text",
        ),
    ],
)
def test_split_with_multiple_occurences(
    input_str: str, sep: str, expected: list[str]
) -> None:
    assert _split_keep(input_str, sep) == expected


@pytest.mark.parametrize(
    "input_str,sep,expected",
    [
        pytest.param(
            "This has **bold* text is wrong",
            "**",
            [
                "This has **bold* text is wrong",
            ],
            id="bold-text-with-mismatching-sep",
        ),
    ],
)
def test_split_with_mismatching_separators_keeps_string_unchanged(
    input_str: str, sep: str, expected: list[str]
) -> None:
    assert _split_keep(input_str, sep) == expected
