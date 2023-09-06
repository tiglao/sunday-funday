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


# Test the function
print(last_entry(None))  # Should print None

# Create sample linked list: Node("C") -> Node("A") -> Node("T")
node1 = Node(value="C", link=None)
node2 = Node(value="A", link=node1)
node3 = Node(value="T", link=node2)

# Should print the last node with value "T"
print(last_entry(node3).value)

# Create another sample linked list: Node(100) -> Node(2)
node4 = Node(value=100, link=None)
node5 = Node(value=2, link=node4)

# Should print the last node with value 2
print(last_entry(node5).value)
