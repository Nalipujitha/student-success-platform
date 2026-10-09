
const API_URL = "http://127.0.0.1:5000/api";

const totalStudents = document.getElementById("totalStudents");
const averageScore = document.getElementById("averageScore");
const needsAttention = document.getElementById("needsAttention");
const onTrack = document.getElementById("onTrack");
const supportChart = document.getElementById("supportChart");
const supportTotal = document.getElementById("supportTotal");
const onTrackInsight = document.getElementById("onTrackInsight");
const studentTable = document.getElementById("studentTable");
const searchInput = document.getElementById("searchInput");
const tableMessage = document.getElementById("tableMessage");

let allStudents = [];

async function loadDashboard() {
    try {
        const response = await fetch(`${API_URL}/dashboard`);

        if (!response.ok) {
            throw new Error("Could not load dashboard statistics.");
        }

        const data = await response.json();

        totalStudents.textContent = data.total_students;
        averageScore.textContent = Number(data.average_success_score).toFixed(2);
        needsAttention.textContent = data.needs_attention;
        onTrack.textContent = data.on_track;

        supportTotal.textContent = data.needs_support;
        onTrackInsight.textContent = data.on_track;

        renderSupportChart(data);
    } catch (error) {
        supportChart.textContent =
            "Unable to load statistics. Check that the Flask server is running.";
        console.error(error);
    }
}

function renderSupportChart(data) {
    const categories = [
        {
            label: "Needs Attention",
            count: data.needs_attention,
            cssClass: "attention"
        },
        {
            label: "On Track",
            count: data.on_track,
            cssClass: "ontrack"
        },
        {
            label: "Needs Support",
            count: data.needs_support,
            cssClass: "support"
        }
    ];

    supportChart.replaceChildren();

    categories.forEach(category => {
        const row = document.createElement("div");
        row.className = "chart-row";

        const label = document.createElement("span");
        label.textContent = category.label;

        const track = document.createElement("div");
        track.className = "bar-track";

        const bar = document.createElement("div");
        bar.className = `bar ${category.cssClass}`;

        const percentage = data.total_students
            ? (category.count / data.total_students) * 100
            : 0;

        bar.style.width = `${percentage}%`;
        track.appendChild(bar);

        const count = document.createElement("span");
        count.className = "chart-count";
        count.textContent = category.count;

        row.append(label, track, count);
        supportChart.appendChild(row);
    });
}

async function loadStudents() {
    try {
        const response = await fetch(`${API_URL}/students`);

        if (!response.ok) {
            throw new Error("Could not load student records.");
        }

        allStudents = await response.json();
        renderStudents(allStudents);
    } catch (error) {
        studentTable.replaceChildren();

        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 5;
        cell.textContent =
            "Unable to load students. Check the Flask server.";

        row.appendChild(cell);
        studentTable.appendChild(row);

        console.error(error);
    }
}

function renderStudents(students) {
    studentTable.replaceChildren();

    if (students.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 5;
        cell.textContent = "No matching students found.";

        row.appendChild(cell);
        studentTable.appendChild(row);
        tableMessage.textContent = "";
        return;
    }

    students.forEach(student => {
        const row = document.createElement("tr");

        const values = [
            student.student_id,
            Number(student.cgpa).toFixed(2),
            `${Number(student.attendance).toFixed(1)}%`,
            Number(student.success_score).toFixed(2)
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        const statusCell = document.createElement("td");
        const badge = document.createElement("span");

        badge.className = "status";

        if (student.support_status === "Needs Support") {
            badge.classList.add("needs-support");
        } else if (student.support_status === "Needs Attention") {
            badge.classList.add("needs-attention");
        } else {
            badge.classList.add("on-track");
        }

        badge.textContent = student.support_status;
        statusCell.appendChild(badge);
        row.appendChild(statusCell);

        studentTable.appendChild(row);
    });

    tableMessage.textContent =
        `Showing ${students.length} of ${allStudents.length} students`;
}

searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim().toLowerCase();

    const filteredStudents = allStudents.filter(student =>
        student.student_id.toLowerCase().includes(query)
    );

    renderStudents(filteredStudents);
});

loadDashboard();
loadStudents();


const recommendationButton = document.getElementById(
    "getRecommendationsBtn"
);

recommendationButton.addEventListener("click", async () => {
    const studentId = document
        .getElementById("recommendationStudentId")
        .value.trim();

    const resultBox = document.getElementById(
        "recommendationsResult"
    );

    if (!studentId) {
        resultBox.textContent = "Please enter a student ID.";
        return;
    }

    resultBox.textContent = "Loading recommendations...";

    try {
        const response = await fetch(
            `${API_URL}/students/${encodeURIComponent(studentId)}/recommendations`
        );

        const data = await response.json();

        if (!response.ok) {
            resultBox.textContent =
                data.error || "Could not find this student.";
            return;
        }

        resultBox.replaceChildren();

        const heading = document.createElement("h3");
        heading.textContent = `Recommendations for ${data.student_id}`;
        resultBox.appendChild(heading);

        if (!data.recommendations || data.recommendations.length === 0) {
            const message = document.createElement("p");
            message.textContent = "No recommendations available.";
            resultBox.appendChild(message);
            return;
        }

        data.recommendations.forEach((recommendation) => {
            const card = document.createElement("article");
            card.className = "recommendation-card";

            const area = document.createElement("h4");
            area.textContent = recommendation.area;

            const priority = document.createElement("p");
            priority.textContent = `Priority: ${recommendation.priority}`;

            const message = document.createElement("p");
            message.textContent = recommendation.message;

            card.append(area, priority, message);
            resultBox.appendChild(card);
        });
    } catch (error) {
        resultBox.textContent =
            "Unable to connect to the backend. Check that Flask is running.";
        console.error("Recommendation error:", error);
    }
});
