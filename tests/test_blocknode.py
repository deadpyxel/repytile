import pytest

from repytile.block_elements import HTMLNode, LeafNode, ParentNode


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


@pytest.mark.parametrize(
    "leaf_node,expected_html",
    [
        pytest.param(
            LeafNode(tag="p", value="Hello"), "<p>Hello</p>", id="simple_p_tag"
        ),
        pytest.param(
            LeafNode(tag="div", value="World"), "<div>World</div>", id="simple_div_tag"
        ),
    ],
)
def test_leafnode_without_props_can_generates_valid_html(
    leaf_node: LeafNode, expected_html: str
) -> None:

    assert leaf_node.to_html() == expected_html


def test_leafnode_without_tag_generates_raw_text() -> None:
    node_value = "raw text"
    leaf_node = LeafNode(value=node_value)

    assert leaf_node.to_html() == node_value


def test_leafnode_with_props_can_generates_valid_html() -> None:
    leaf_node = LeafNode(
        tag="a", value="link", props={"href": "https://www.example.com"}
    )
    expected_html = '<a href="https://www.example.com">link</a>'

    assert leaf_node.to_html() == expected_html


def test_leafnode_with_empty_props_can_generates_valid_html() -> None:
    leaf_node = LeafNode(tag="svg", value="<circle />")
    expected_html = "<svg><circle /></svg>"

    assert leaf_node.to_html() == expected_html


def test_parent_node_cannot_generate_html_without_tag() -> None:
    parent_node = ParentNode()

    with pytest.raises(
        ValueError, match="ParentNode instances should have a tag value"
    ):
        parent_node.to_html()


def test_parent_node_cannot_generate_html_without_children() -> None:
    parent_node = ParentNode(tag="p")

    with pytest.raises(
        ValueError, match="ParentNode instances should have at least one children"
    ):
        parent_node.to_html()


def test_parent_node_with_leaf_nodes_generates_valid_html() -> None:
    node = ParentNode(
        tag="p",
        children=[
            LeafNode("b", "bold"),
            LeafNode(None, "normal"),
            LeafNode("i", "italic"),
            LeafNode(None, "normal"),
        ],
    )

    assert node.to_html() == "<p><b>bold</b>normal<i>italic</i>normal</p>"


def test_nested_parent_nodes_generates_valid_html() -> None:
    node = ParentNode(
        tag="div",
        children=[
            ParentNode(
                tag="p",
                children=[
                    LeafNode(tag="b", value="bold"),
                    LeafNode(tag=None, value="normal"),
                ],
            )
        ],
    )

    assert node.to_html() == "<div><p><b>bold</b>normal</p></div>"
