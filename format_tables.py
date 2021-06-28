import pandas as pd
import pickle

do = False
operator = 'Eran Nir'
# PROJECT_FILE = 'C:\\Users\\erann\\Desktop\\Eran Nir\\My Projects\\top_sort_courses'
COURSE_ID_STR = 'מס\' קורס'
TOTAL_STR = 'סה"כ'
LIBA = ['ליבה)', 'במסלול)']
NOTACOURSE = ['שם הקורס', '3 קורסי מסלול', 'פרויקט גמר שלב ב\'', 'פרויקט גמר שלב א\'', '2 מעבדות מתקדמות']
PROBLEMATIC = ['*', ' ']


class Course:
    def __init__(self, course_id, name, lec_hours, rec_hours, tot_hours, weight, kdam):
        self.id = course_id
        self.name = name
        self.lec_hours = lec_hours
        self.rec_hours = rec_hours
        self.tot_hours = tot_hours
        self.weight = weight
        self.kdam = kdam

    def remove_rouge_number(self):
        if self.name[-1] in PROBLEMATIC:
            self.name = self.name[:-1]
        try:
            last_word = int(self.name[-1])
            self.name = self.name[:-1]
        except ValueError as e:
            pass
        return self.name


class CourseTable:
    def __init__(self, table):
        self.table = table


class DegreeCoursesTables:
    def __init__(self, website_address):
        self.website_address = website_address
        self.tables = self.get_courses_tables()
        self.courses_list = self.get_courses_list()

    def get_courses_tables(self):
        tables = []
        tables_list = []
        table_mn = pd.read_html(self.website_address)
        list_of_rows_to_remove = []
        for table_index in range(len(table_mn)):
            if table_mn[table_index].shape in [(1, 1), (1, 0), (0, 1)]:
                list_of_rows_to_remove.append(table_index)
        for index in sorted(list_of_rows_to_remove, reverse=True):
            del table_mn[index]
        for table in table_mn:
            i = 0
            while table[0][i] != COURSE_ID_STR:
                i += 1
            table = table.iloc[i:]
            table = table.reset_index(drop=True)
            new_header = table.iloc[0]  # grab the first row for the header
            table = table[1:]  # take the data less the header row
            table.columns = new_header  # set the header row as the df header
            if table.iloc[-1, 1] == TOTAL_STR:
                table = table[:-1]
            tables.append(table)
        for i in range(len(tables) - 1):
            if tables[i].equals(tables[i + 1]):
                continue
            else:
                tables_list.append(CourseTable(tables[i]))
        return tables_list

    def get_courses_list(self):
        course_list = []
        for table in self.tables:
            for index in range(table.table.shape[0]):
                course = table.table.iloc[index].values
                id = course[0]
                name = course[1]  # .split(")")[0]
                lec_hours = course[2]
                rec_hours = course[3]
                tot_hours = course[5]
                weight = course[6]
                kdam = course[7]
                course_list.append(Course(id, name, lec_hours, rec_hours, tot_hours, weight, kdam))
        return course_list

    def fix_courses_names(self):
        course_list = []
        for course in self.courses_list:
            course.name = course.remove_rouge_number()
            if course.name.split()[-1] in LIBA:
                course.name = course.name.split()[:-2]
                course.name = " ".join(course.name)
            course.name = course.remove_rouge_number()
            if course.name not in NOTACOURSE:
                course_list.append(course)
        self.courses_list = course_list
        return self.courses_list

    def dump_list_to_pkl(self, file_name):
        open_file = open(file_name, "wb")
        pickle.dump(self.fix_courses_names(), open_file)
        open_file.close()


if __name__ == '__main__' or operator == 'Eran Nir':
    # do = input("RUN THE PROGRAM AGAIN?     True / False")
    if do:
        hashmal_courses_tables = DegreeCoursesTables('https://engineering.tau.ac.il/yedion/9')
        tables = hashmal_courses_tables.get_courses_tables()
        # courses_list = hashmal_courses_tables.get_courses_list()
        courses_list = hashmal_courses_tables.fix_courses_names()
        hashmal_courses_tables.dump_list_to_pkl('courses_list.pkl')





