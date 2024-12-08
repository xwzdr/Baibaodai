from sql import StudentRepository, GroupRepository
from pydantic1 import Student
from pydantic1 import Group

# # class StudentService:
# #     def __init__(self, student_repo: StudentRepository):
# #         self.student_repo = student_repo
# #
# #     def create_student(self, student: Student):
# #         return self.student_repo.create(student)
# #
# #     def get_student(self, student_id: int):
# #         return self.student_repo.get(student_id)
# #
# #     # 其他学生相关方法...
# #
# # class GroupService:
# #     def __init__(self, group_repo: GroupRepository):
# #         self.group_repo = group_repo
# #
# #     def create_group(self, group: Group):
# #         return self.group_repo.create(group)
# #
# #     def get_group(self, group_id: int):
# #         return self.group_repo.get(group_id)
# #
# #     # 其他班级相关方法...
#
# from sql import StudentRepository, GroupRepository
# from pydantic1 import Student
# from pydantic1 import Group
# class GroupService:
#     def __init__(self, group_repo: GroupRepository):
#         self.group_repo = group_repo
#
#     def create_group(self, group: Group):
#         return self.group_repo.create(group)
#
#     def get_group(self, group_id: int):
#         return self.group_repo.get(group_id)
#
#     def update_group(self, group_id: int, group: Group):
#         # 假设 Group 模型有一个更新方法
#         group.id = group_id
#         return self.group_repo.update(group)
#
#     def delete_group(self, group_id: int):
#         return self.group_repo.delete(group_id)
#
#     def list_groups(self):
#         return self.group_repo.list_all()
#
#     def search_groups(self, search_term: str):
#         # 假设 GroupRepository 有一个搜索方法
#         return self.group_repo.search(search_term)
#
#     def add_student_to_group(self, group_id: int, student: Student):
#         # 假设 Group 模型有一个添加学生的方法
#         group = self.get_group(group_id)
#         if group:
#             group.add_student(student)
#             return self.group_repo.update(group.id, group)
#         return None
#
#     def remove_student_from_group(self, group_id: int, student_id: int):
#         group = self.get_group(group_id)
#         if group:
#             group.remove_student(student_id)
#             return self.group_repo.update(group.id, group)
#         return None

class StudentService:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def create_student(self, student: Student):
        return self.student_repo.create(student)

    def get_student(self, student_id: int):
        return self.student_repo.get(student_id)

    def update_student(self, student_id: int, student: Student):
        return self.student_repo.update(student_id, student)

    def delete_student(self, student_id: int):
        self.student_repo.delete(student_id)

    def list_students(self):
        return self.student_repo.list_all()

    def add_student_to_group(self, student_id: int, group_id: int):
        student = self.get_student(student_id)
        group = self.student_repo.get_group(group_id)
        if student and group:
            group.students.add(student)
            return self.group_repo.update(group_id, group)
        return None

    def remove_student_from_group(self, student_id: int, group_id: int):
        group = self.get_group(group_id)
        if group:
            group.students.discard(student)
            return self.group_repo.update(group_id, group)
        return None

    def get_students_in_group(self, group_id: int):
        group = self.get_group(group_id)
        if group:
            return list(group.students)
        return []


class GroupService:
    def __init__(self, group_repo: GroupRepository):
        self.group_repo = group_repo

    def create_group(self, group: Group):
        return self.group_repo.create(group)

    def get_group(self, group_id: int):
        return self.group_repo.get(group_id)

    def update_group(self, group_id: int, group: Group):
        return self.group_repo.update(group_id, group)

    def delete_group(self, group_id: int):
        self.group_repo.delete(group_id)

    def list_groups(self):
        return self.group_repo.list_all()

    def add_student_to_group(self, student_id: int, group_id: int):
        return self.student_service.add_student_to_group(student_id, group_id)

    def remove_student_from_group(self, student_id: int, group_id: int):
        return self.student_service.remove_student_from_group(student_id, group_id)

    def get_students_in_group(self, group_id: int):
        return self.student_service.get_students_in_group(group_id)