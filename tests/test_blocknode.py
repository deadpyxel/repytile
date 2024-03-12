import pytest

from repytile.block_elements import HTMLNode


def test_convertion_from_props_to_html_matches_expectation() -> None:
    block_node = HTMLNode(props={"href": "https://www.example.com", "target": "_blank"})
    expected_html_props = 'href="https://www.example.com" target="_blank"'

    assert block_node.props_to_html() == expected_html_props


def test_when_props_is_empty_empty_html_is_returned() -> None:
    block_node = HTMLNode()

    assert block_node.props_to_html() == ""


@pytest.mark.parametrize(
    "html_node,expected",
    [
        pytest.param(
            HTMLNode(tag="p"),
            "HTMLNode(tag=p, value=None, children=None, props=None)",
            id="tag_only",
        ),
        pytest.param(
            HTMLNode(value="hello"),
            "HTMLNode(tag=None, value=hello, children=None, props=None)",
            id="value_only",
        ),
        pytest.param(
            HTMLNode(children=[HTMLNode()]),
            "HTMLNode(tag=None, value=None, children=[HTMLNode(tag=None, value=None, children=None, props=None)], props=None)",
            id="children_with_none_fields",
        ),
        pytest.param(
            HTMLNode(children=[HTMLNode(value="p")]),
            "HTMLNode(tag=None, value=None, children=[HTMLNode(tag=None, value=p, children=None, props=None)], props=None)",
            id="children_with_fields",
        ),
        pytest.param(
            HTMLNode(props={"href": "link"}),
            "HTMLNode(tag=None, value=None, children=None, props={'href': 'link'})",
            id="props_only",
        ),
    ],
)
def test_htmlnode_repr_follows_expected_format(
    html_node: HTMLNode, expected: str
) -> None:
    assert str(html_node) == expected


def test_to_html_method_raises_exception_when_not_a_child_class() -> None:
    html_node = HTMLNode()

    with pytest.raises(NotImplementedError):
        html_node.to_html()
