## 使用方法

用 stream() 函数传入列表，然后像java的Stream类一样操作。


## 示例
```python
if __name__ == '__main__':
    # （1）list
    print()
    my_list = [1, 2, 3, 4, 5, 6]
    print(my_list)

    my_list_1 = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, my_list)))
    print(my_list_1)

    my_list_2 = stream(my_list).filter(lambda x: x % 2 == 0).map(lambda x: x ** 2).collect()
    print(my_list_2)


    # （2）dict
    print()
    my_dict = {1: 1, 2: 2, 3: 3, "4": "4", "5": "5", "6": "6"}
    print(my_dict)

    def my_map(item):
        item["value"] = int(item["value"]) * int(item["value"])
        return item
    my_dict_2_1 = stream(my_dict).filter(lambda i: int(i["value"]) % 2 == 0).map(my_map).collect()
    print(my_dict_2_1)
    my_dict_2_2 = stream(my_dict).filter(lambda i: int(i["value"]) % 2 == 0).map(my_map).collect(is_to_dict = False)
    print(my_dict_2_2)

