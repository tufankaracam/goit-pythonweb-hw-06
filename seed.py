from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
from models import Group, Student, Teacher, Subject, Grade
from datetime import datetime
import random

engine = create_engine("postgresql://postgres:secret123@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

# create 3 groups
groups = [Group(name=f"Group {i}") for i in range(1, 4)]
session.add_all(groups)

# create 50 students
students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(50)]
session.add_all(students)

# create 5 teachers
teachers = [Teacher(name=fake.name()) for _ in range(5)]
session.add_all(teachers)

# create 8 subjects
subjects = [
    Subject(name=f"Subject {i}", teacher=random.choice(teachers)) for i in range(1, 9)
]
session.add_all(subjects)

# create 20 grades for every student
grades = []
for student in students:
    for subject in subjects:
        for _ in range(3):  # 3 not
            grade = Grade(
                student=student,
                subject=subject,
                grade=random.uniform(50, 100),
                date=datetime.now(),
            )
            grades.append(grade)

session.add_all(grades)
session.commit()
session.close()
