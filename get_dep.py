import pickle

from format_tables import do, courses_list_file_name

if do:
    from format_tables import courses_list


def load_courses_list(file_name):
    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list


def course_dependencies(course, course_list):
    if course.kdam == "nan":
        print(course.name)
        return
    else:
        for c in course_list:
            if type(course.kdam) is float:
                continue
            for o in course.kdam.split(";"):
                if sublist(c.name.split(), o.split()):
                    if type(course.kdam) is str:
                        print(c.name)
                        course_dependencies(c, course_list)
                    else:
                        for i in course.kdam.split(';'):
                            print(i.name)
                            course_dependencies(i, course_list)


def sublist(subset_list, main_list):
    common_list = [element for element in subset_list if element in main_list]
    return common_list == subset_list


def run_program(courses_list):
    course_name = input("Choose Course:\nTo exit enter 999\n")
    while course_name != str(999):
        for course in courses_list:
            if sublist(course_name.split(), course.name.split()):
                print("Showing dependencies courses for ", course.name, ":")
                course_dependencies(course, courses_list)
                print('-----------------------------------------------------------')
        print('**********************************************************\n')
        course_name = input("Choose Course:\nTo exit enter 999\n")


if __name__ == '__main__':
    if not do:
        courses_list = load_courses_list(courses_list_file_name)
    else:
        courses_list = courses_list
    run_program(courses_list)
