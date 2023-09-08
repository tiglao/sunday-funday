# 11

# find the last node

from pydantic import BaseModel
from typing import Any, Union


class Node(BaseModel):
    value: Any
    link: "Node" | None


def last_entry(linked_list: Node = None) -> Node:
    while linked_list is not None:
        if linked_list.link is None:
            return linked_list
        linked_list = linked_list.link
    return None


node1 = Node(value="C", link=None)
node2 = Node(value="A", link=node1)
node3 = Node(value="T", link=node2)

node4 = Node(value=100, link=None)
node5 = Node(value=2, link=node4)
