from typing import List, Dict, Tuple, Any
from numpy import mean
import json

gradesType = Dict[str, List[float]]
SchoolType = Dict[str, List[str] | str]
StudentType = Dict[str, gradesType]


def validateKeys(
        dataSet: Dict[str, Any],
        keysList: List[str]
        ) -> bool:
    datasetKeys = dataSet.keys()
    for key in keysList:
        if key not in datasetKeys:
            return False
    return True


def addStudent(
        schools: List[SchoolType],
        students: List[StudentType],
        studentName: str,
        grades: gradesType | None = None
        ) -> bool:
    if studentName in [student["full name"] for student in students]:
        return False
    newStudent = {
        "full name": studentName,
        "grades": {}
    }
    if grades is not None and isinstance(grades, Dict):
        for grade in grades.keys():
            if not isinstance(grades[grade], List):
                return False
            if not any([grade in s["courses"] for s in schools]):
                return False
        newStudent["grades"] = grades
    students.append(newStudent)

    return True


def readData(
        path: str,
        ) -> Tuple[List[SchoolType], List[StudentType] | str]:
    with open(path, "r") as sourceFile:
        data = json.load(sourceFile)

    valid = validateKeys(data, ["students", "schools"])
    if valid and isinstance(data["schools"], List):
        validSchools = filter(
            lambda school: validateKeys(school, ["name", "courses"]),
            data["schools"])
        valid = valid and len(list(validSchools)) == len(data["schools"])
    if valid and isinstance(data["students"], List):
        validStudents = filter(
            lambda student: validateKeys(student, ["full name", "grades"]),
            data["students"])
        valid = valid and len(list(validStudents)) == len(data["students"])
        for student in data["students"]:
            if valid and isinstance(student["grades"], Dict):
                existingCourses = filter(
                    lambda x: any([x in s["courses"] for s in data["schools"]]),
                    keysGrades := student["grades"].keys()
                )
                valid = valid and len(list(existingCourses)) == len(keysGrades)

    if not valid:
        raise ValueError("Inproper json structure")
    return data["schools"], data["students"]


def saveData(
        path: str,
        schools: List[SchoolType],
        students: List[StudentType]
        ) -> bool:
    data = {
        "schools": schools,
        "students": students
    }

    try:
        with open(path, "w") as saveFile:
            json.dump(data, saveFile, indent=4)
    except Exception:
        return False
    return True


def averageStudentsInCourse(
        students: List[StudentType],
        course: str
        ) -> Dict[str, float]:
    averages = {}
    for student in students:
        if course in student["grades"].keys():
            averages[student["full name"]] = mean(student["grades"][course])
    return averages


def averageCoursesInStudent(
        students: List[StudentType],
        studentName: str
        ) -> Dict[str, float]:
    averages = {}
    student = list(filter(
        lambda s: s["full name"] == studentName,
        students
    ))[0]
    for course in student["grades"].keys():
        averages[course] = mean(student["grades"][course])
    return averages


def averageStudentsInSchool(
        schools: List[SchoolType],
        students: List[StudentType],
        schoolName: str
        ) -> Dict[str, float]:
    school = list(filter(
        lambda s: s["name"] == schoolName,
        schools
    ))[0]
    studentsInSchool = list(filter(
        lambda s: any([c in school["courses"] for c in s["grades"].keys()]),
        students
    ))
    averages = {}
    for student in studentsInSchool:
        averages[student["full name"]] = \
            mean(list(averageCoursesInStudent(students, student["full name"])
                      .values()))
    return averages


def averageCoursesInSchool(
        schools: List[SchoolType],
        students: List[StudentType],
        schoolName: str
        ) -> Dict[str, float]:
    school = list(filter(
        lambda s: s["name"] == schoolName,
        schools
    ))[0]
    averages = {}
    for course in school["courses"]:
        averages[course] = \
            mean(list(averageStudentsInCourse(students, course).values()))
    return averages


if __name__ == "__main__":
    try:
        schools, students = readData("./database.json")

        print("#----- Averages of Mathematics students")
        print(*averageStudentsInCourse(students, "Mathematics").items(),
              sep="\n")
        
        print("\n\n#----- Averages of Emma Davis courses")
        print(*averageCoursesInStudent(students, "Emma Davis")
              .items(), sep="\n")
        
        print("\n\n#----- Averages of Language School courses")
        print(*averageCoursesInSchool(schools, students, "Language School")
              .items(), sep="\n")
        
        print("\n\n#----- Averages of High School students")
        print(*averageStudentsInSchool(schools, students, "High School")
              .items(), sep="\n")
        
        print("\n\n#----- Unsuccessfull addition of student")
        print(addStudent(schools, students, "John Smith"))

        print("\n\n#----- Successfull addition of student")
        print(addStudent(schools, students, "Grzegorz Brzęczyszczykiewicz",
                         {"French": [5], "Biology": [4, 3.5]}))
        
        print("\n\n#----- Successfull save of new database state")
        print(saveData("./new_database.json", schools, students))

    except Exception as e:
        print(f"[ERR] {e}")
