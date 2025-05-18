from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node


def main() -> None:
    node = TextNode("This is a text node", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    print(f'{html_node}')

if __name__ == '__main__':
    main()