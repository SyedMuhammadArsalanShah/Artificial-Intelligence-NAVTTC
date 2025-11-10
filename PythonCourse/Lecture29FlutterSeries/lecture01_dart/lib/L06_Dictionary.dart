void main() {
  Map students_info = {
    "name": "Usman",
    "age": 18,
    "Subjects": ["URDU", "MATH", "ENG"],
    "education": {"BS":2025, "MS":2026,"PHD":2027},
  };


print(students_info["Subjects"][0]);
print(students_info["education"]["PHD"]);

}
