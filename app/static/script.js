function addStudent() {
    const container = document.getElementById('student-list');
    const newField = document.createElement('div');
    newField.innerHTML = `
      <input type="text" name="name[]" placeholder="Name">
      <input type="text" name="roll[]" placeholder="Roll No">
    `;
    container.appendChild(newField);
  }
function showToday() {
  document.getElementById("today-form").style.display = "block";
  document.getElementById("date-form").style.display = "none";
}

function showDate() {
  document.getElementById("today-form").style.display = "none";
  document.getElementById("date-form").style.display = "block";
}