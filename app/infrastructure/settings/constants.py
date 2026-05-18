

class Limits:
    class Department:
        class Name:
            min_length = 1
            max_length = 200

    class Employee:
        class FullName:
            min_length = 1
            max_length = 200

        class Position:
            min_length = 1
            max_length = 200

    class QueryParams:
        class GetDepartment:
            min_depth = 0
            max_depth = 5
            default_include_employees = True
