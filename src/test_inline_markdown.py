import unittest

from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes
)
from textnode import TextNode, TextType

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.text_normal),
                TextNode("text", TextType.text_bold),
                TextNode(" with an ", TextType.text_normal),
                TextNode("italic", TextType.text_italic),
                TextNode(" word and a ", TextType.text_normal),
                TextNode("code block", TextType.text_code),
                TextNode(" and an ", TextType.text_normal),
                TextNode("image", TextType.text_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.text_normal),
                TextNode("link", TextType.text_link, "https://boot.dev"),
            ],
            nodes,
        )


class TestNodeDelimiter(unittest.TestCase):
    def test_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.text_normal)
        new_nodes = split_nodes_delimiter([node], "`", TextType.text_code)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == 'This is text with a '
        assert new_nodes[0].text_type == TextType.text_normal

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.text_normal
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.text_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_normal),
                TextNode("bolded word", TextType.text_bold),
                TextNode(" and ", TextType.text_normal),
                TextNode("another", TextType.text_bold),
            ],
            new_nodes,
        )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and this is with [click here](https://www.boot.dev)"
        )
        self.assertListEqual([("click here", "https://www.boot.dev")], matches)

class TestSplitImagesLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text_normal,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_normal),
                TextNode("image", TextType.text_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text_normal),
                TextNode(
                    "second image", TextType.text_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [click here](https://www.boot.dev) and another [here as well](https://www.youtube.com)",
            TextType.text_normal,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_normal),
                TextNode("click here", TextType.text_link, "https://www.boot.dev"),
                TextNode(" and another ", TextType.text_normal),
                TextNode(
                    "here as well", TextType.text_link, "https://www.youtube.com"
                ),
            ],
            new_nodes,
        )

    def test_split_image_w_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [here as well](https://www.youtube.com)",
            TextType.text_normal,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_normal),
                TextNode("image", TextType.text_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another [here as well](https://www.youtube.com)", TextType.text_normal),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.text_normal,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.text_image, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
