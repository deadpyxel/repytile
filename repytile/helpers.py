import re

from repytile.block_elements import HTMLNode, LeafNode
from repytile.exceptions import InvalidElementType
from repytile.inline_elements import TextNode


TAG_MAPPING = {
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img",
}


def text_node_to_html_node(tn: TextNode) -> LeafNode:
    """
    Converts a TextNode object to a LeafNode object for HTML representation.

    Arguments:
        tn (TextNode): The TextNode object to be converted.

    Returns:
        LeafNode: The converted LeafNode object for HTML representation.

    Raises:
        InvalidElementType: If the text_type of the TextNode is not in the ALLOWED_TYPES list.

    The function checks if the text_type of the TextNode is allowed for conversion. If it is not in the ALLOWED_TYPES
    tuple, it raises an InvalidElementType exception. Otherwise, it converts the TextNode to a LeafNode object with
    appropriate tag and properties for HTML representation.

    The mapping of text_type to HTML tag is as follows:
    - "text": No tag, just the text value
    - "bold": <b> tag
    - "italic": <i> tag
    - "code": <code> tag
    - "link": <a> tag with href property
    - "image": <img> tag with src and alt properties
    """

    if tn.text_type not in TAG_MAPPING and tn.text_type != "text":
        raise InvalidElementType(
            f"The type of TextNode {tn.text_type} is not allowed for conversion"
        )
    if tn.text_type == "text":
        return LeafNode(value=tn.text)

    tag = TAG_MAPPING[tn.text_type]
    props = {}
    if tn.text_type == "link":
        props["href"] = tn.url
    elif tn.text_type == "image":
        props["src"] = tn.url
        props["alt"] = tn.text

    return LeafNode(tag=tag, value=tn.text, props=props)


def _split_keep(input_str: str, sep: str) -> list[str]:
    """
    Split a string based on a separator while keeping the separator as part of the result.

    Arguments:
        input_str (str): The input string to be split.
        sep (str): The separator to split the input string on.

    Returns:
        list[str]: A list of strings resulting from splitting the input string based on the separator,
                   with the separator included in each split part.

    Example:
        >>> _split_keep("apple,orange,banana", ",")
        ['apple', ',orange,', 'banana']
    """
    # Escape any special characters on separator
    sep = re.escape(sep)
    # Define the regex for extraction, format is sep(words)sep, as separators always should appear in pairs
    # We use parenthesis to keep the separator as part of the capturing group
    expr = rf"({sep}[^*]+{sep})"
    # split the input string into parts using the separator
    result = re.split(expr, input_str)
    # remove any empty strings
    result = [split_part for split_part in result if split_part]
    return result


def split_nodes_delimiter(
    old_nodes: list[TextNode | HTMLNode], delimiter: str, text_type: str
) -> list[TextNode | HTMLNode]:
    allowed_node_types = [TAG_MAPPING.keys()] + ["text"]
    resulting_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            resulting_nodes.append(node)
            continue
        if node.text_type not in allowed_node_types:
            raise InvalidElementType(
                f"The type of TextNode {node.text_type} is not processable."
            )

    return resulting_nodes
