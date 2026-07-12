async function postData(url, fieldName) {
    const input = document.getElementById("inputText").value;

    const form = new FormData();
    form.append(fieldName, input);

    return fetch(url, {
        method: "POST",
        body: form
    }).then(r => r.json());
}

// helper animation wrapper
function render(boxId, html) {
    const box = document.getElementById(boxId);

    box.innerHTML = `<div class="loading">processing...</div>`;

    setTimeout(() => {
        box.innerHTML = html;
    }, 300);
}

// ---------------- QNA ----------------
async function askQuestion() {
    const data = await postData("/qna", "question");

    render("qnaBox", `
        <div class="card pop">
            <h3>Answer</h3>
            <p>${data.answer}</p>
        </div>
    `);
}

// ---------------- EXPLAIN ----------------
async function explain() {
    const data = await postData("/explanation", "topic");

    render("explainBox", `
        <div class="card pop">
            <h3>Explanation</h3>
            <p>${data.explanation}</p>
        </div>
    `);
}

// ---------------- SUMMARY ----------------
async function summarize() {
    const data = await postData("/summary", "text");

    render("summaryBox", `
        <div class="card pop">
            <h3>Summary</h3>
            <p>${data.summary}</p>
        </div>
    `);
}

// ---------------- PATH ----------------
async function learningPath() {
    const data = await postData("/learning-path", "topic");

    render("pathBox", `
        <div class="card pop">
            <h3>Learning Path</h3>
            <p>${data.learning_path}</p>
        </div>
    `);
}

// ---------------- QUIZ ----------------
async function generateQuiz() {
    const data = await postData("/quiz", "text");

    if (!data.success) {
        render("quizBox", `<div class="card error">${data.error}</div>`);
        return;
    }

    let html = `<div class="card pop"><h3>Quiz</h3>`;

    data.quiz.forEach((q, i) => {
        html += `
            <div class="quiz-block">
                <h4>Q${i + 1}. ${q.question}</h4>

                <div class="options">
                    <div>A ${q.options.A}</div>
                    <div>B ${q.options.B}</div>
                    <div>C ${q.options.C}</div>
                    <div>D ${q.options.D}</div>
                </div>

                <div class="answer">✔ ${q.correct_answer}</div>
            </div>
        `;
    });

    html += `</div>`;

    render("quizBox", html);
}