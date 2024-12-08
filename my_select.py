from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade

engine = create_engine("postgresql://postgres:secret123@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()


def select_1_top_5_students(session):
    return (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )


def select_2_top_student_in_subject(session, subject_id):
    return (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )


def select_3_group_avg_in_subject(session, group_id, subject_id):
    return (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar()
    )


def select_4_overall_average(session):
    return session.query(func.avg(Grade.grade).label("average_grade")).scalar()


def select_5_courses_by_teacher(session, teacher_id):
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()


def select_6_students_in_group(session, group_id):
    return session.query(Student.name).filter(Student.group_id == group_id).all()


def select_7_grades_in_group_for_subject(session, group_id, subject_id):
    return (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )


def select_8_teacher_avg_grade(session, teacher_id):
    return (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )


def select_9_courses_by_student(session, student_id):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )


def select_10_courses_by_student_and_teacher(session, student_id, teacher_id):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )


def test_select_queries():
    print("1. En yüksek ortalamaya sahip 5 öğrenci:")
    print(select_1_top_5_students(session))

    print("\n2. Belirli bir dersten en yüksek ortalamaya sahip öğrenci:")
    print(select_2_top_student_in_subject(session, subject_id=1))

    print("\n3. Belirli bir gruptaki dersin ortalama notu:")
    print(select_3_group_avg_in_subject(session, group_id=1, subject_id=2))

    print("\n4. Genel ortalama (tüm notlar üzerinden):")
    print(select_4_overall_average(session))

    print("\n5. Belirli bir öğretmenin verdiği dersler:")
    print(select_5_courses_by_teacher(session, teacher_id=1))

    print("\n6. Belirli bir grubun öğrencileri:")
    print(select_6_students_in_group(session, group_id=1))

    print("\n7. Belirli bir grubun belirli bir ders için aldığı notlar:")
    print(select_7_grades_in_group_for_subject(session, group_id=1, subject_id=2))

    print("\n8. Belirli bir öğretmenin verdiği derslerdeki not ortalaması:")
    print(select_8_teacher_avg_grade(session, teacher_id=1))

    print("\n9. Belirli bir öğrencinin aldığı dersler:")
    print(select_9_courses_by_student(session, student_id=1))

    print("\n10. Belirli bir öğrencinin belirli bir öğretmenden aldığı dersler:")
    print(select_10_courses_by_student_and_teacher(session, student_id=1, teacher_id=1))


if __name__ == "__main__":
    test_select_queries()
