import os
import sys
import _ctypes


class Node:
    def __init__(self, value, next_node, prev_node):
        self.value = value
        self.next_node = next_node
        self.prev_node = prev_node

    def get_value(self):
        return self.value

    def get_next(self):
        return self.next_node

    def get_prev(self):
        return self.prev_node

    def set_next(self, node):
        self.next_node = node

    def set_prev(self, node):
        self.prev_node = node


class LinkedList:
    def __init__(self, list_type):
        self.head = None
        self.tail = None
        self.minimum = None
        self.list_type = list_type
        self.values_dict = dict()

    def get_tail(self):
        return self.tail

    def get_head(self):
        return self.head

    def get_values_dict(self):
        return self.values_dict

    def insert_sorted(self, value):
        pointer = self.head
        if pointer is None:
            # First value in the list
            new_node = Node(value, None, None)
            self.head = new_node
            self.tail = new_node
            return
        while pointer is not None:
            if pointer.get_value() == value:
                # already exist in the list
                return
            if pointer.get_value() > value:
                if pointer.get_next() is None:
                    # Insert to the end of the list
                    new_node = Node(value, None, pointer)
                    pointer.set_next(new_node)
                    self.tail = new_node
                    return
                else:
                    pointer = pointer.get_next()
            else:
                new_node = Node(value, pointer, pointer.get_prev())
                if pointer.get_prev() is None:
                    # Insert to the head of the list
                    pointer.set_prev(new_node)
                    self.head = new_node
                else:
                    # Insert into the list
                    pointer.get_prev().set_next(new_node)
                    pointer.set_prev(new_node)
                return

    def union_sorted(self, other_list):
        list3 = LinkedList(self.list_type)
        pointer = self.tail
        pointer_other_list = other_list.get_tail()
        while pointer is not None or pointer_other_list is not None:
            if pointer is not None and pointer_other_list is not None:
                if pointer.get_value() < pointer_other_list.get_value():
                    list3.insert_sorted(pointer.get_value())
                    pointer = pointer.get_prev()
                elif pointer.get_value() > pointer_other_list.get_value():
                    list3.insert_sorted(pointer_other_list.get_value())
                    pointer_other_list = pointer_other_list.get_prev()
                else:
                    pointer = pointer.get_prev()
            elif pointer is not None:
                list3.insert_sorted(pointer.get_value())
                pointer = pointer.get_prev()
            else:
                list3.insert_sorted(pointer_other_list.get_value())
                pointer_other_list = pointer_other_list.get_prev()
        return list3

    def get_minimum(self):
        if self.tail is not None:
            # sorted list
            return self.tail.get_value()
        return self.minimum

    def extract_minimum_sorted(self):
        if self.tail is None:
            return None
        min_value = self.tail.get_value()
        self.tail = self.tail.get_prev()
        if self.tail is None:
            # The list is now empty
            self.head = None
            self.minimum = None
        else:
            self.tail.set_next(None)
            self.minimum = self.tail.get_value()
        return min_value

    def insert_unsorted(self, *args):
        value = args[0]
        if len(args) == 2 and args[1] is not None:
            # get other list values dict
            other_values_dict = args[1].get_values_dict()
            if value in other_values_dict:
                print('Error: the value already exist in the other list.')
                return
        if value not in self.values_dict:
            new_node = Node(value, self.head, None)
            self.values_dict[value] = id(new_node)
            if self.head is not None:
                self.head.set_prev(new_node)
                if self.minimum > value:
                    self.minimum = value
            else:
                self.minimum = value
            self.head = new_node

    def extract_minimum_unsorted(self):
        if self.minimum is None:
            return None
        minimum_node = _ctypes.PyObj_FromPtr(self.values_dict[self.minimum])
        if minimum_node.get_prev() is not None:
            minimum_node.get_prev().set_next(minimum_node.get_next())
        else:
            self.head = minimum_node.get_next()
        if minimum_node.get_next() is not None:
            minimum_node.get_next().set_prev(minimum_node.get_prev())
        del self.values_dict[self.minimum]
        last_minimum = self.minimum
        # finds the new minimum in the list
        pointer = self.get_head()
        if pointer is None:
            min_value = None
        else:
            min_value = sys.maxsize
        while pointer is not None:
            if pointer.get_value() < min_value:
                min_value = pointer.get_value()
            pointer = pointer.get_next()
        self.minimum = min_value
        return last_minimum

    def union_unsorted(self, other_list):
        self.minimum = min(self.minimum, other_list.minimum)
        pointer = other_list.get_head()
        while pointer is not None:
            self.insert_unsorted(pointer.get_value())
            pointer = pointer.get_next()
        return self

    def __str__(self):
        string = ''
        pointer = self.head
        while pointer is not None:
            string += f'{pointer.get_value()} -> '
            pointer = pointer.get_next()
        return string + 'None'


def main():
    list_flag = True
    lists = [None, None]
    list_type = input('Please choose lists type: (enter the number)\n'
                      '1. Sorted lists\n'
                      '2. Unsorted lists\n'
                      '3. Disjointed and unsorted lists\n')
    while list_type != '1' and list_type != '2' and list_type != '3':
        print('Error: Improper selection.')
        list_type = input('Please try again: ')
    list_type = int(list_type)
    file_name = input('To load file enter the file name, otherwise press enter.\n')
    if file_name != '':
        fd = open(file_name, 'r')
    while True:
        if file_name != '':
            line = fd.readline()
            if line.isspace():
                # empty line in the file
                continue
            else:
                if line == '':
                    # end of file
                    fd.close()
                    return
                operation = line[:-1]
        else:
            operation = input('Enter one of the following operations: MakeHeap / Insert X / Union / Minimum /'
                              ' ExtractMin / Print / Exit\n')
        command = operation.split(' ')[0]
        if command == 'Print':
            print(f'List1: {lists[0]}\nList2: {lists[1]}')
            continue
        if operation == 'Exit':
            return
        insert_value = operation.split(' ')[-1] if operation.find(' ') != -1 else None
        operations = {'MakeHeap': lambda: make_heap(list_type),
                      'Insert': lambda current_list, other_list: insert(current_list, other_list, int(insert_value),
                                                                        list_type),
                      'Union': lambda current_list, other_list: union(current_list, other_list, list_type),
                      'Minimum': lambda current_list: minimum(current_list),
                      'ExtractMin': lambda current_list: extract_min(current_list, list_type)}

        if command not in operations.keys():
            print('Error: Improper selection.')
            continue
        if command == 'MakeHeap':
            list_flag = not list_flag
        if command in ['Minimum', 'ExtractMin']:
            lists[list_flag] = operations[operation.split(' ')[0]](lists[list_flag])
        elif command in ['Insert', 'Union']:
            lists[list_flag] = operations[operation.split(' ')[0]](lists[list_flag], lists[not list_flag])
        else:
            # MakeHeap command
            lists[list_flag] = operations[operation.split(' ')[0]]()
        if command == 'Union':
            lists[not list_flag] = None
        print(f'Current list: {lists[list_flag]}')


def make_heap(list_type):
    return LinkedList(list_type)


def insert(this_list, other_list, value, list_type):
    list_types_dict = {1: lambda: this_list.insert_sorted(value), 2: lambda: this_list.insert_unsorted(value),
                       3: lambda: this_list.insert_unsorted(value, other_list)}
    list_types_dict[list_type]()
    return this_list


def union(this_list, other_list, list_type):
    list_types_dict = {1: lambda: this_list.union_sorted(other_list), 2: lambda: this_list.union_unsorted(other_list),
                       3: lambda: this_list.union_unsorted(other_list)}
    return list_types_dict[list_type]()


def minimum(this_list):
    print(this_list.get_minimum())
    return this_list


def extract_min(this_list, list_type):
    list_types_dict = {1: lambda: this_list.extract_minimum_sorted(), 2: lambda: this_list.extract_minimum_unsorted(),
                       3: lambda: this_list.extract_minimum_unsorted()}
    print(list_types_dict[list_type]())
    return this_list


if __name__ == '__main__':
    main()
