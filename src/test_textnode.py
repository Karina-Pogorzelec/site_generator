import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.text_bold)
        node2 = TextNode("This is a text node", TextType.text_bold)
        self.assertEqual(node, node2)
    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.text_bold)
        node2 = TextNode("This is not a text node", TextType.text_bold)
        self.assertNotEqual(node, node2)
    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.text_bold)
        node2 = TextNode("This is a text node", TextType.text_italic)
        self.assertNotEqual(node, node2)
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.text_bold)
        node2 = TextNode("This is a text node", TextType.text_bold, "https://www.boot.dev")
        self.assertNotEqual(node, node2)
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.text_bold, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.text_bold, "https://www.boot.dev")
        self.assertEqual(node, node2)    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.text_bold, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, bold, https://www.boot.dev)", repr(node)
        )


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.text_normal)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a text node", TextType.text_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
    def test_image(self):
        node = TextNode("This is an image", TextType.text_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

if __name__ == "__main__":
    unittest.main()