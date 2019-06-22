#! python3


# Finds all the areas
def area_options(original_list):
    list_ = [i[1] for i in original_list]
    list_ = list(dict.fromkeys(list_))
    list_.sort()

    return list_


# Finds all the sub areas in the selected area
def sub_area_options(original_list):
    list_ = [i[2] for i in original_list]
    list_ = list(dict.fromkeys(list_))
    list_.sort()

    return list_


# Finds all the grades in an area
def grade_options(original_list):
    list_ = [i[-1] for i in original_list]
    list_ = list(dict.fromkeys(list_))
    list_.sort()

    return list_
