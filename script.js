document.addEventListener("DOMContentLoaded", () => {
  const todoInput = document.getElementById("todoInput");
  const dueDate = document.getElementById("dueDate");
  const addBtn = document.getElementById("addBtn");
  const deleteAllBtn = document.getElementById("deleteAllBtn");
  const todoList = document.getElementById("todoList");

  let todos = JSON.parse(localStorage.getItem("todos")) || [];

  function renderTodos() {
    todoList.innerHTML = "";
    if (todos.length === 0) {
      todoList.innerHTML = `<tr><td colspan="4">No task found</td></tr>`;
      return;
    }

    todos.forEach((todo, index) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${todo.text}</td>
        <td>${todo.date}</td>
        <td>${todo.completed ? "Completed" : "Pending"}</td>
        <td>
          <button class="complete-btn" onclick="completeTodo(${index})">Done</button>
          <button class="delete-btn" onclick="deleteTodo(${index})">Delete</button>
        </td>
      `;
      todoList.appendChild(row);
    });
  }

  window.completeTodo = function(index) {
    todos[index].completed = true;
    saveAndRender();
  };

  window.deleteTodo = function(index) {
    todos.splice(index, 1);
    saveAndRender();
  };

  addBtn.addEventListener("click", () => {
    const text = todoInput.value.trim();
    const date = dueDate.value;

    if (text === "" || date === "") {
      alert("Isi task dan tanggalnya dulu ya!");
      return;
    }

    todos.push({ text, date, completed: false });
    saveAndRender();
    todoInput.value = "";
    dueDate.value = "";
  });

  deleteAllBtn.addEventListener("click", () => {
    if (confirm("Yakin ingin menghapus semua task?")) {
      todos = [];
      saveAndRender();
    }
  });

  function saveAndRender() {
    localStorage.setItem("todos", JSON.stringify(todos));
    renderTodos();
  }

  renderTodos();
});
