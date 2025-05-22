import re 
from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    paragraph = 'paragraph'
    heading = "heading"
    code = 'code'
    quote = 'quote'
    unordered_list = 'unordered_list'
    ordered_list = 'ordered_list'


def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        stripped_block = block.strip()
        if stripped_block:
            blocks.append(stripped_block)
    return blocks


def block_to_block_type(block): 
    lines = block.split('\n') 

    if block.startswith('```') and block.endswith('```'):
        return BlockType.code
    if bool(re.match(r'^[#]{1,6} ', block)):
        return BlockType.heading
    if all(line.startswith('>') for line in lines):
        return BlockType.quote
    if all(line.startswith('- ') for line in lines): 
        return BlockType.unordered_list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.paragraph
            i += 1
        return BlockType.ordered_list

    return BlockType.paragraph  

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.strip().startswith('# '):
            return line.strip("#").strip()
    raise Exception("no title found")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.paragraph:
        return paragraph_to_html_node(block)
    if block_type == BlockType.heading:
        return heading_to_html_node(block)
    if block_type == BlockType.code:
        return code_to_html_node(block)
    if block_type == BlockType.ordered_list:
        return olist_to_html_node(block)
    if block_type == BlockType.unordered_list:
        return ulist_to_html_node(block)
    if block_type == BlockType.quote:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text_node = TextNode(block[4:-3], TextType.text_normal)
    code = ParentNode("code", [text_node_to_html_node(text_node)])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    lines = block.split('\n')
    children_list = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        children_list.append(ParentNode("li", children))
    return ParentNode("ol", children_list)

def ulist_to_html_node(block):
    lines = block.split('\n')
    children_list= []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        children_list.append(ParentNode("li", children))
    return ParentNode("ul", children_list)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = "\n".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)