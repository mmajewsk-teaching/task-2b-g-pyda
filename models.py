class Student:
    def __init__(
            self,
            name: str,
            surname: str,
            id: int
    ):
        self.name = name
        self.surname = surname
        self.id = id
        self.attendance = {}
        self.grades = {}

    def get_attendance_score(self) -> float:
        classes = self.attendance.keys()
        n = 0
        result = 0.0
        for cl in classes:
            for at in self.attendance[cl]:
                result += at
                n += 1

        result /= n
        return result
    
    def get_average_score_in_class(self, cl: str) -> float:
        grades = self.grades[cl]
        mean = 0.0
        weight = 0.0
        for g in grades:
            mean += g["value"]*g["weight"]
            weight += g["weight"]

        mean /= weight
        return mean
    

    def get_average_score(self, class_rates: dict) -> float:
        mean = 0.0
        weight = 0.0
        classes = class_rates.keys()
        for cl in classes:
            mean += self.get_average_score_in_class(cl) * class_rates[cl]
            weight += class_rates[cl]

        mean /= weight
        return mean
    
    # would be implemented to read from a file, now a placeholder
    def load_attendance(self):
        self.attendance = {
            "bio" : [0, 1, 1, 1, 1, 0, 1],
            "math" : [0, 1, 0, 1, 1, 0, 1],
            "phys" : [0, 1, 1, 0, 0, 0, 1],
            "chem" : [0, 1, 1, 1, 1, 0, 1],
            "eng" : [0, 1, 0, 1, 1, 0, 1]
        }