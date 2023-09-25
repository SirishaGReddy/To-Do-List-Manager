class Manager:
    def __init__(self):
        self.task_list = {}        # Dictionary to store tasks as {task_description: [due_date, status]}
        self.completed_tasks = []  # List to store completed tasks
        self.undo_stack = []       # Stack to store the state of the task list for undo/redo

    def add_task(self, date, task):
        self.task_list[task] = [date, 0]  # 0 represents task not completed
        self.undo_stack.append(dict(self.task_list))  # Save the state for undo/redo

    def task_done(self, task):
        if task in self.task_list:
            self.task_list[task][1] = 1  # 1 represents task completed
            self.completed_tasks.append(task)
            self.undo_stack.append(dict(self.task_list))

    def show_pending(self):
        formatted_tasks = []
        for task, info in self.task_list.items():
            status = "Completed" if info[1] == 1 else "Pending"
            formatted_task = f"Task: {task}, Due Date: {info[0]}, Status: {status}"
            if info[1] == 0:
                formatted_tasks.append(formatted_task)
        return formatted_tasks

    def show_completed(self):
        formatted_tasks = []
        for task, info in self.task_list.items():
            status = "Completed" if info[1] == 1 else "Pending"
            formatted_task = f"Task: {task}, Due Date: {info[0]}, Status: {status}"
            if info[1] == 1:
                formatted_tasks.append(formatted_task)
        return formatted_tasks

    def delete_task(self, task):
        if task in self.task_list:
            del self.task_list[task]
            self.undo_stack.append(dict(self.task_list))

    def undo(self):
        if len(self.undo_stack) > 1:
            self.undo_stack.pop()
            self.task_list = dict(self.undo_stack[-1])

    def redo(self):
        pass  # Implement redo functionality

    def show_all(self):
        formatted_tasks = []
        for task, info in self.task_list.items():
            status = "Completed" if info[1] == 1 else "Pending"
            formatted_task = f"Task: {task}, Due Date: {info[0]}, Status: {status}"
            formatted_tasks.append(formatted_task)
        return formatted_tasks


if __name__ == '__main__':
    m = Manager()
    print('Enter the commands here:\n')

    while True:
        command = str(input('$$>')).strip()
        func = None
        date = None
        task = None
        left = command.find(':')
        right = command.find(',')

        if command == 'Show All':
            formatted_tasks = m.show_all()
            for formatted_task in formatted_tasks:
                print(formatted_task)

        if command == 'Undo':
            m.undo()


        if command == 'Show completed':
            formatted_tasks = m.show_completed()
            for formatted_task in formatted_tasks:
                print(formatted_task)

        if command == 'Show pending':
            formatted_tasks = m.show_pending()
            for formatted_task in formatted_tasks:
                print(formatted_task)


        if left != -1 and right != -1:
            func = command[:left]
            date  = command[right+1:]
            task = command[left + 1:right]
        else:
            func = command[:left]
            task = command[left+1:]

        if func == 'Add Task':
            m.add_task(date.split(':')[1], task)

        if func == 'Mark Completed':
            m.task_done(task)

        if func == 'Delete':
            print(task)
            m.delete_task(task)
            print('Successfully removed')


