from datetime import datetime

class Task:
    def __init__(self, description, due_date=None):
        self.description = description
        self.completed = False
        self.due_date = due_date

    def mark_completed(self):
        self.completed = True

    def unmark_completed(self):
        self.completed = False

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        due_date_str = f", Due: {self.due_date}" if self.due_date else ""
        return f"{self.description} - {status}{due_date_str}"
class TaskBuilder:
    def __init__(self, description):
        self.description = description
        self.due_date = None

    def set_due_date(self, due_date):
        self.due_date = due_date
        return self

    def build(self):
        return Task(self.description, self.due_date)

class TaskMemento:
    def __init__(self, tasks):
        self.tasks = tasks.copy()

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.history = []
        self.redo_history = []

    def add_task(self, task):
        self.tasks.append(task)
        self.save_to_history()
        self.redo_history = []  # Clear redo history

    def mark_completed(self, description):
        for task in self.tasks:
            if task.description == description:
                task.mark_completed()
                self.save_to_history()
                self.redo_history = []  # Clear redo history
                return
        print("Task not found.")

    def unmark_completed(self, description):
        for task in self.tasks:
            if task.description == description:
                task.unmark_completed()
                self.save_to_history()
                self.redo_history = []  # Clear redo history
                return
        print("Task not found.")

    def delete_task(self, description):
        self.tasks = [task for task in self.tasks if task.description != description]
        self.save_to_history()
        self.redo_history = []  # Clear redo history

    def save_to_history(self):
        self.history.append(TaskMemento(self.tasks))

    def undo(self):
        if len(self.history) > 1:
            undone_task = self.history.pop()
            self.redo_history.append(undone_task)
            self.tasks = self.history[-1].tasks.copy()

    def redo(self):
        if self.redo_history:
            redone_task = self.redo_history.pop()
            self.history.append(redone_task)
            self.tasks = redone_task.tasks.copy()

    def view_tasks(self, filter_type="all"):
        if filter_type == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_type == "pending":
            filtered_tasks = [task for task in self.tasks if not task.completed]
        else:
            filtered_tasks = self.tasks

        for task in filtered_tasks:
            print(task)

def parse_due_date(input_string):
    try:
        return datetime.strptime(input_string, "%Y-%m-%d")
    except ValueError:
        return None

def main():
    task_manager = TaskManager()
    print("\nOptions:")
    print("1. Add Task (e.g., 'Buy groceries, Due: 2023-09-20')")
    print("2. Mark Completed (e.g., 'Mark Completed: Buy groceries')")
    print("3. Unmark Completed (e.g., 'Unmark Completed: Buy groceries')")
    print("4. Delete Task (e.g., 'Delete Task: Buy groceries')")
    print("5. Undo")
    print("6. Redo")
    print("7. View Tasks (e.g., 'Show all', 'Show completed', 'Show pending')")
    print("8. Exit")

    while True:


        choice = input("-->")

        if choice.startswith("Add Task:"):
            input_parts = choice.split(':')
            description = input_parts[1].strip()
            main = description.split(',')

            due_date = None
            due_date_str = input_parts[2]
            due_date = parse_due_date(due_date_str)
            print(due_date , due_date_str)
            task_builder = TaskBuilder(main[0])
            if due_date:
                task_builder.set_due_date(due_date)
            task = task_builder.build()
            task_manager.add_task(task)
            print(f"Task '{main[0]}' added.")

        elif choice.startswith("Mark Completed:"):
            description = choice.split(":")[1].strip()
            task_manager.mark_completed(description)

        elif choice.startswith("Unmark Completed:"):
            description = choice.split(":")[1].strip()
            task_manager.unmark_completed(description)

        elif choice.startswith("Delete Task:"):
            description = choice.split(":")[1].strip()
            task_manager.delete_task(description)

        elif choice == "Undo":
            task_manager.undo()

        elif choice == "Redo":
            task_manager.redo()

        elif choice.startswith("Show"):
            filter_type = choice.split(" ")[-1].strip().lower()
            task_manager.view_tasks(filter_type)

        elif choice == "Exit":
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
