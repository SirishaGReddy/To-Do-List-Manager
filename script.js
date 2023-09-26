class Task {
    constructor(description, dueDate) {
        this.description = description;
        this.dueDate = dueDate;
        this.completed = false;
    }
}

let tasks = [];
let taskHistory = [];
let historyIndex = -1;

const taskList = document.getElementById('taskList');
const taskInput = document.getElementById('taskInput');
const dueDate = document.getElementById('dueDate');
const undoButton = document.querySelector('.undo');
const redoButton = document.querySelector('.redo');

function addTask() {
    const description = taskInput.value.trim();
    const date = dueDate.value;
    if (description === '') return;

    const task = new Task(description, date);
    tasks.push(task);
    addToHistory();

    renderTasks();
    taskInput.value = '';
    dueDate.value = '';
    updateUndoRedoButtons();
}

function toggleCompleted(index) {
    tasks[index].completed = !tasks[index].completed;
    addToHistory();
    renderTasks();
}

function deleteTask(index) {
    tasks.splice(index, 1);
    addToHistory();
    renderTasks();
}

function filterTasks(filter) {
    let filteredTasks;
    if (filter === 'completed') {
        filteredTasks = tasks.filter(task => task.completed);
    } else if (filter === 'pending') {
        filteredTasks = tasks.filter(task => !task.completed);
    } else {
        filteredTasks = tasks;
    }
    renderTasks(filteredTasks);
}

function renderTasks(filteredTasks = tasks) {
    taskList.innerHTML = '';
    filteredTasks.forEach((task, index) => {
        const li = document.createElement('li');
        li.className = task.completed ? 'completed' : '';
        li.innerHTML = `
            ${task.description}${task.dueDate ? ` - Due: ${task.dueDate}` : ''}
            <div>
                <button onclick="toggleCompleted(${index})">${task.completed ? 'Undo' : 'Complete'}</button>
                <button onclick="deleteTask(${index})">Delete</button>
            </div>
        `;
        taskList.appendChild(li);
    });
}

function addToHistory() {
    taskHistory = taskHistory.slice(0, historyIndex + 1);
    taskHistory.push(JSON.parse(JSON.stringify(tasks)));
    historyIndex++;
    updateUndoRedoButtons();
}

function undo() {
    if (historyIndex > 0) {
        historyIndex--;
        tasks = JSON.parse(JSON.stringify(taskHistory[historyIndex]));
        renderTasks();
        updateUndoRedoButtons();
    }
}

function redo() {
    if (historyIndex < taskHistory.length - 1) {
        historyIndex++;
        tasks = JSON.parse(JSON.stringify(taskHistory[historyIndex]));
        renderTasks();
        updateUndoRedoButtons();
    }
}

function updateUndoRedoButtons() {
    undoButton.disabled = historyIndex === 0;
    redoButton.disabled = historyIndex === taskHistory.length - 1;
}

renderTasks();
