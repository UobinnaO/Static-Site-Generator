# from textnode import TextNode, TextType

# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     rtn_lst_nodes = list(filter(lambda x: x.text_type != TextType.TEXT, old_nodes))
#     only_texttype_node = list(filter(lambda x: x.text_type == TextType.TEXT, old_nodes))
#     node_text_lst = list(map(lambda x: x.text, only_texttype_node))

#     word_start_end_locations = []

#     def locate_delimiter(str, delimiter, str_not_checked):
#         single_delimiter_location = str.find(delimiter)
#         word_locations_lst_len = len(word_start_end_locations)
#         if delimiter not in str:
#             return
#         single_word_location = 0
#         if word_locations_lst_len % 2 == 0:
#             single_word_location = (
#                 str.find(delimiter) + len(str_not_checked) + len(delimiter)
#             )
#         if word_locations_lst_len % 2 != 0:
#             single_word_location = (
#                 str.find(delimiter)
#                 + len(delimiter)
#                 + len(str_not_checked)
#                 - len(delimiter)
#             )
#         str_not_checked = (
#             str_not_checked + str[: single_delimiter_location + len(delimiter)]
#         )
#         word_start_end_locations.append(single_word_location)
#         return locate_delimiter(
#             str[single_delimiter_location + len(delimiter) :],
#             delimiter,
#             str_not_checked,
#         )

#     for text in node_text_lst:
#         locate_delimiter(text, delimiter, "")
#         location_pairs = list(
#             zip(word_start_end_locations[::2], word_start_end_locations[1::2])
#         )
#         emphasized_phrases = []
#         for pair in location_pairs:
#             emphasized_phrases.append(text[pair[0] : pair[1]])
#         print(f"{emphasized_phrases}\n")

#         text_split = text.split(delimiter)
#         if "" in text_split:
#             text_split.remove("")

#         for text in text_split:
#             if text in emphasized_phrases:
#                 rtn_lst_nodes.append(TextNode(text, text_type))
#             else:
#                 text_type2 = TextType.TEXT
#                 rtn_lst_nodes.append(TextNode(text, text_type2))
#     return rtn_lst_nodes
