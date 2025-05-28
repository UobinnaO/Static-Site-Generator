import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

# def block_to_block_type(block):
#     if re.findall(r"^#+ \w*", block):
#         return BlockType.HEADING
#     if re.findall(r"```[\s\S]*?(\w+)[\s\S]*?```", block):
#         return BlockType.CODE

#     block_split = block.split("\n")

#     first_chars = []
#     for block in block_split:
#         first_chars.append(block[0:3])
#     first_chars_len = len(first_chars)

#     quote_check = [True, first_chars_len]
#     while quote_check[0] == True and quote_check[1] > 0:
#         for char in first_chars:
#             if not re.findall(r"^> +\w", char):
#                 quote_check[0] = False
#                 quote_check[1] = quote_check[1] - 1
#         if quote_check[0] == True:
#             return BlockType.QUOTE

#     unordered_lst_check = [True, first_chars_len]
#     first_chars_len = len(first_chars)
#     while unordered_lst_check[0] == True and unordered_lst_check[1] > 0:
#         for char in first_chars:
#             if not re.findall(r"^-+ \w", char):
#                 unordered_lst_check[0] = False
#                 unordered_lst_check[1] = unordered_lst_check[1] - 1
#         if unordered_lst_check[0] == True:
#             return BlockType.UNORDERED_LIST


#     ordered_lst_check = True
#     first_chars_len = len(first_chars)
#     nums = []
#     for char in first_chars:
#         if re.findall(r"^\d. ", char):
#             str_num = re.findall(r"^\d. ", char)
#             num = re.findall(r"^\d", char)
#             nums.append(int(num[0]))
#         else:
#             ordered_lst_check = False

#     for index, num in enumerate(nums):
#         if index == len(nums) - 1:
#             if num < nums[index - 1]:
#                 ordered_lst_check = False
#         elif index >= 0:
#             if num > nums[index + 1]:
#                 ordered_lst_check = False

#     if ordered_lst_check == True:
#         return BlockType.ORDERED_LIST

#     return BlockType.PARAGRAPH

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.QUOTE:
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
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
