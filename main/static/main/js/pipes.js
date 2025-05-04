document.addEventListener("DOMContentLoaded", function () {
  const pipesImage = document.getElementById("pipesImage");
  const humidityTableBody = document.querySelector("#humidityTable tbody");

  async function fetchData() {
    fetch("/api/data")
      .then((response) => response.json())
      .then((data) => {
        console.log("Данные с сервера:", data.pipes);

        const humidityTableBody = document.querySelector(
          "#humidityTable tbody"
        );
        humidityTableBody.innerHTML = ""; // очищаем перед добавлением новых строк

        data.pipes.forEach((pipe) => {
          const newRow = document.createElement("tr");
          const now = new Date();
          newRow.innerHTML = `
            <td>Труба ${pipe.number}</td>
            <td>${pipe.humidity}%</td>
            <td>${now.toLocaleTimeString()}</td>
          `;
          humidityTableBody.appendChild(newRow);

          const statusElem = document.getElementById(`status${pipe.number}`);
          if (statusElem) statusElem.textContent = pipe.status;
        });
      })
      .catch((error) => {
        console.error("Ошибка при получении данных:", error);
      });
  }

  // Запрашивать каждые 3 секунды
  setInterval(fetchData, 3000);
  fetchData();
});

function simulateSignal() {
  const statuses = ["Ожидание", "Активирован", "Ошибка"];

  // Генерация случайных состояний для каждого сервопривода
  for (let i = 1; i <= 6; i++) {
    const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
    document.getElementById(`status${i}`).textContent = randomStatus;

    // Обновление состояния кнопок и цветов
    const servo = document.getElementById(`servo${i}`);
    if (randomStatus === "Активирован") {
      servo.classList.add("active");
      servo.classList.remove("inactive");
    } else if (randomStatus === "Ошибка") {
      servo.classList.add("inactive");
      servo.classList.remove("active");
    } else {
      servo.classList.remove("active", "inactive");
    }
  }
}
