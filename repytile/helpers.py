from repytile.block_elements import LeafNode
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
