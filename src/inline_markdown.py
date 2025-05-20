import re
from textnode import TextType, TextNode

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.text_normal)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.text_bold)
    nodes = split_nodes_delimiter(nodes, "_", TextType.text_italic)
    nodes = split_nodes_delimiter(nodes, "`", TextType.text_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.text_normal:
            text_parts = node.text.split(delimiter)
            if len(text_parts) % 2 != 0:
                for i in range(0, len(text_parts)):
                    if text_parts[i] == "":
                        continue
                    if i % 2 == 0:
                        new_nodes.append(TextNode(text_parts[i], TextType.text_normal))
                    else:
                        new_nodes.append(TextNode(text_parts[i], text_type))
            else:
                raise ValueError("text has invalid Markdown syntax")
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.text_normal:
                images = extract_markdown_images(node.text)
                text = node.text
                if len(images) == 0:
                    new_nodes.append(node)
                else:
                    for image in images:                       
                        image_alt = image[0]
                        image_link = image[1]
                        sections = text.split(f"![{image_alt}]({image_link})", 1)
                        text = sections[1]
                        if sections[0] != "":
                            new_nodes.append(TextNode(sections[0], TextType.text_normal))
                        new_nodes.append(TextNode(image_alt, TextType.text_image, image_link))
                    if text != "":
                        new_nodes.append(TextNode(text, TextType.text_normal))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.text_normal:
                links = extract_markdown_links(node.text)
                text = node.text
                if len(links) == 0:
                    new_nodes.append(node)
                else:
                    for link in links:                       
                        link_text = link[0]
                        link_link = link[1]
                        sections = text.split(f"[{link_text}]({link_link})", 1)
                        text = sections[1]
                        if sections[0] != "":
                            new_nodes.append(TextNode(sections[0], TextType.text_normal))
                        new_nodes.append(TextNode(link_text, TextType.text_link, link_link))
                    if text != "":
                        new_nodes.append(TextNode(text, TextType.text_normal))
        else:
            new_nodes.append(node)
    return new_nodes