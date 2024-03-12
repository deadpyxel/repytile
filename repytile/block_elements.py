from __future__ import annotations

from typing import Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list[HTMLNode]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        """
        Initialize an HTMLNode object with the specified tag, value, children, and properties.

        Parameters:
            tag (str): The HTML tag for the node. If not provided, the node will render as raw text.
            value (str): The value/content of the node. If not provided, the node will be assumed to have children.
            children (list[HTMLNode]): A list of child HTMLNode objects. If not provided, the node will be assumed to have a value.
            props (dict[str, str]): A dictionary of properties/attributes for the node. If not provided, the node will have no attributes.

        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        """
        Converts the properties of an object into HTML attribute format.

        This method takes the properties of an object stored in a dictionary format and converts them into a string of HTML attributes.
        Each key-value pair in the dictionary is converted into a string in the format 'key="value"'.
        If the object has no properties, an empty string is returned.

        Returns:
            str: A string containing the HTML attributes generated from the object's properties.

        Example:
            >>> obj = {'id': 'my_id', 'class': 'my_class', 'style': 'color: red;'}
            >>> obj.props_to_html()
            'id="my_id" class="my_class" style="color: red;"'
        """
        if not self.props:
            return ""
        html_props = []
        for attr, val in self.props.items():
            html_props.append(f'{attr}="{val}"')

        return " ".join(html_props)

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    """
    LeafNodes represent HTML elements without any children
    """

    def to_html(self) -> str:
        """
        Converts the LeafNode object to its HTML representation.

        Returns:
            str: The HTML representation of the LeafNode object.
        """
        html_attrs = self.props_to_html()
        sp = " " if html_attrs else ""
        return f"<{self.tag}{sp}{html_attrs}>{self.value}</{self.tag}>"
