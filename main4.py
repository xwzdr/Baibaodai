class Student:
    def __init__(self, group_number, average_score):
        self.group_number = group_number
        self.average_score = average_score

    def show_info(self):
        print(f"Студент группы {self.group_number}, средний балл: {self.average_score}")

    def calculate_stipend(self):
        if self.average_score >= 5:
            return 6000 if self.group_number == "аспирант" else 8000
        else:
            return 4000 if self.group_number == "студент" else 6000


class Postgraduate:
    def __init__(self, group_number, average_score, thesis_title):
        self.group_number = group_number
        self.average_score = average_score
        self.thesis_title = thesis_title

    def show_info(self):
        print(f"Аспирант группы {self.group_number}, средний балл: {self.average_score}, научная работа: {self.thesis_title}")

    def calculate_stipend(self):
        if self.average_score >= 5:
            return 8000
        else:
            return 6000


# 示例使用
student1 = Student("group1", 5.5)
student2 = Student("group2", 4.8)

postgrad1 = Postgraduate("group1", 5.0, "Thesis Title")

# 显示信息
student1.show_info()
student2.show_info()
postgrad1.show_info()

# 计算助学金
print(f"Студент {student1.group_number} получает стипендию {student1.calculate_stipend()}р.")
print(f"Студент {student2.group_number} получает стипендию {student2.calculate_stipend()}р.")
print(f"Аспирант {postgrad1.group_number} получает стипендию {postgrad1.calculate_stipend()}р.")