import pandas as pd


def add_locations(locations, obj_tuple_list):
    for obj_tuple in obj_tuple_list:
        locations[obj_tuple[0]] = obj_tuple[1]
    return locations

def show_deck_OT2(locations):
    locations["12"] = "12"
    layout_dict = {
            "1":('Row_4','Col_1'),
            "2":('Row_4','Col_2'),
            "3":('Row_4','Col_3'),
            "4":('Row_3','Col_1'),
            "5":('Row_3','Col_2'),
            "6":('Row_3','Col_3'),
            "7":('Row_2','Col_1'),
            "8":('Row_2','Col_2'),
            "9":('Row_2','Col_3'),
            "10":('Row_1','Col_1'),
            "11":('Row_1','Col_2'),
            "12":('Row_1','Col_3')
            }
    layout_table = pd.DataFrame(index=['Row_1','Row_2','Row_3','Row_4'], columns=['Col_1','Col_2','Col_3']).fillna("---")
    for obj in locations:
        if str(locations[obj]):
            object_to_place = str(locations[obj])
        else:
            object_to_place = str(obj)
        layout_table.loc[layout_dict[obj][0], layout_dict[obj][1]] = object_to_place
    print("\n Please arrange the items in the following configuration: \n")
    print(layout_table,"\n")
    input("Press enter to continue")


