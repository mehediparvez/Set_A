class Employee:
    def __init__(self, name, emp_id, salary):
        self.name = name
        self.emp_id = emp_id
        self.salary = salary

    def display(self):
        print(f"  Name   : {self.name}")
        print(f"  ID     : {self.emp_id}")
        print(f"  Salary : {self.salary}")


class Programmer(Employee):
    def __init__(self, name, emp_id, salary, language):
        super().__init__(name, emp_id, salary)
        self.language = language

    def display(self):
        print("[ Programmer ]")
        super().display()
        print(f"  Language : {self.language}")


class Manager(Employee):
    def __init__(self, name, emp_id, salary, department):
        super().__init__(name, emp_id, salary)
        self.department = department

    def display(self):
        print("[ Manager ]")
        super().display()
        print(f"  Department : {self.department}")


def main():
    employees = []

    while True:
        print("\n========== Employee Menu ==========")
        print("1. Add Programmer")
        print("2. Add Manager")
        print("3. Display All Employees")
        print("4. Exit")
        print("===================================")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            name = input("Enter name       : ").strip()
            emp_id = input("Enter ID         : ").strip()
            salary = input("Enter salary     : ").strip()
            language = input("Enter language   : ").strip()
            employees.append(Programmer(name, emp_id, salary, language))
            print("Programmer added successfully.")

        elif choice == '2':
            name = input("Enter name       : ").strip()
            emp_id = input("Enter ID         : ").strip()
            salary = input("Enter salary     : ").strip()
            department = input("Enter department : ").strip()
            employees.append(Manager(name, emp_id, salary, department))
            print("Manager added successfully.")

        elif choice == '3':
            if not employees:
                print("No employees to display.")
            else:
                print(f"\n--- Total Employees: {len(employees)} ---")
                for emp in employees:
                    emp.display()
                    print()

        elif choice == '4':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
