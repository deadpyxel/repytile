from typing import Optional

from repytile.exceptions import InvalidElementType


class TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None) -> None:
        """
        Initialize a TextNode object with the given text, text type, and optional URL.

        Parameters:
            text (str): The text content of the node.
            text_type (str): The type of the node, such as 'bold', 'italic', 'image', etc.
            url (Optional[str]): The URL associated with the text content, if applicable.

        Raises:
            InvalidElementType: If text_type is None or empty.

        Returns:
            None
        """
        if not text_type:
            raise InvalidElementType("text_type cannot be None")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, __value: object) -> bool:
        """
        Compare this TextNode object with another object to determine if they are equal.

        Parameters:
            __value (object): The object to compare with this TextNode object.

        Returns:
            bool: True if all fields of the two objects are equal, False otherwise.
        """
        if not isinstance(__value, TextNode):
            return False
        return (
            self.text == __value.text
            and self.text_type == __value.text_type
            and self.url == __value.url
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the TextNode object.

        Returns:
            str: A string representation of the TextNode object in the format "TextNode(text, text_type, url)"
        """
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
