// =========================================
// EduGenie AI
// Version 2.0
// =========================================

// ---------- DOM ----------

const input = document.getElementById("inputText");
const counter = document.getElementById("charCount");

// ---------- Character Counter ----------

input.addEventListener("input", () => {

    counter.textContent =
        `${input.value.length} Characters`;

});

// ---------- Thinking Messages ----------

const thinkingMessages = [

    "Reading your request...",

    "Searching educational knowledge...",

    "Connecting concepts...",

    "Building response...",

    "Almost finished...",

    "Checking accuracy..."

];

// ---------- Button Lock ----------

function disableButtons(state = true){

    document.querySelectorAll(".module button")
    .forEach(btn=>{

        btn.disabled = state;

        if(state){

            btn.classList.add("disabled");

        }

        else{

            btn.classList.remove("disabled");

        }

    });

}

// ---------- Toast ----------

function showToast(message){

    const toast = document.createElement("div");

    toast.className = "toast";

    toast.innerHTML = message;

    document.body.appendChild(toast);

    requestAnimationFrame(()=>{

        toast.classList.add("show");

    });

    setTimeout(()=>{

        toast.classList.remove("show");

        setTimeout(()=>{

            toast.remove();

        },400);

    },2200);

}

// ---------- Loading ----------

function loading(boxId){

    const msg =
        thinkingMessages[
            Math.floor(
                Math.random()*thinkingMessages.length
            )
        ];

    document.getElementById(boxId).innerHTML =

`

<div class="loading">

<div class="brain">

🧠

</div>

<div class="loadingText">

${msg}

</div>

<div class="loader">

<div></div>

<div></div>

<div></div>

</div>

</div>

`;

}
// =========================================
// NETWORK REQUEST
// =========================================

let lastGenerationTime = 0;

async function postData(url, fieldName){

    const value = input.value.trim();

    if(value===""){

        showToast("Please enter a topic or question.");

        throw new Error("Input cannot be empty.");

    }

    disableButtons(true);

    const start = performance.now();

    try{

        const form = new FormData();

        form.append(fieldName,value);

        const response = await fetch(url,{

            method:"POST",

            body:form

        });

        if(!response.ok){

            throw new Error("Server returned an error.");

        }

        const data = await response.json();

        const end = performance.now();

        lastGenerationTime =
            ((end-start)/1000).toFixed(2);

        return data;

    }

    finally{

        disableButtons(false);

    }

}



// =========================================
// COPY
// =========================================

function copyText(text){

    navigator.clipboard.writeText(text);

    showToast("Copied successfully.");

}



// =========================================
// STATISTICS
// =========================================

function responseStats(text){

    const words =
        text.trim().split(/\s+/).length;

    const chars =
        text.length;

    return `

<div class="stats">

<span>📄 ${words} words</span>

<span>🔤 ${chars} characters</span>

<span>⚡ ${lastGenerationTime}s</span>

</div>

`;

}



// =========================================
// RESPONSE CARD
// =========================================

function responseCard(title,text){

    return `

<div class="ai-card fadeIn">

<div class="cardHeader">

<h3>${title}</h3>

<button

class="copyBtn"

onclick="copyText(\`${text.replace(/`/g,"\\`")}\`)">

📋 Copy

</button>

</div>

<div class="markdown">

${marked.parse(text)}

</div>

${responseStats(text)}

</div>

`;

}



// =========================================
// ERROR CARD
// =========================================

function errorCard(message){

    return `

<div class="ai-card errorCard fadeIn">

<h3>

❌ Something went wrong

</h3>

<p>

${message}

</p>

</div>

`;

}



// =========================================
// SCROLL
// =========================================

function scrollToBox(id){

    document

        .getElementById(id)

        .scrollIntoView({

            behavior:"smooth",

            block:"center"

        });

}
// =========================================
// GENERIC MODULE RENDERER
// =========================================

async function runModule({

    url,

    field,

    box,

    title,

    responseKey

}){

    loading(box);

    scrollToBox(box);

    try{

        const data = await postData(url, field);

        if(!data[responseKey]){

            throw new Error("No response received.");

        }

     renderResponse(
    box,
    title,
    data[responseKey]
);

    }

    catch(err){

        renderError(
    box,
    err.message
);

    }

}



// =========================================
// QUESTION ANSWERING
// =========================================

function askQuestion(){

    runModule({

        url:"/qna",

        field:"question",

        box:"qnaBox",

        title:"❓ Question Answering",

        responseKey:"answer"

    });

}



// =========================================
// EXPLANATION
// =========================================

function explain(){

    runModule({

        url:"/explanation",

        field:"topic",

        box:"explainBox",

        title:"🧠 Explanation",

        responseKey:"explanation"

    });

}



// =========================================
// SUMMARY
// =========================================

function summarize(){

    runModule({

        url:"/summary",

        field:"text",

        box:"summaryBox",

        title:"📄 Summary",

        responseKey:"summary"

    });

}



// =========================================
// LEARNING PATH
// =========================================

function learningPath(){

    runModule({

        url:"/learning-path",

        field:"topic",

        box:"pathBox",

        title:"🧭 Learning Roadmap",

        responseKey:"learning_path"

    });

}
// =========================================
// QUIZ CARD
// =========================================

function quizCard(question, index){

    return `

<div class="quiz-card fadeIn">

<div class="quiz-header">

<h3>

📝 Question ${index + 1}

</h3>

</div>

<div class="quiz-question">

${question.question}

</div>

<div class="quiz-options">

<button class="optionBtn">

<b>A.</b> ${question.options.A}

</button>

<button class="optionBtn">

<b>B.</b> ${question.options.B}

</button>

<button class="optionBtn">

<b>C.</b> ${question.options.C}

</button>

<button class="optionBtn">

<b>D.</b> ${question.options.D}

</button>

</div>

<button

class="showAnswerBtn"

onclick="toggleAnswer(this)">

👁 Show Answer

</button>

<div class="answerBox">

<div class="correctAnswer">

✅ Correct Answer

<b>

${question.correct_answer}

</b>

</div>

<div class="explanation">

💡 ${question.explanation}

</div>

</div>

</div>

`;

}



// =========================================
// SHOW / HIDE ANSWER
// =========================================

function toggleAnswer(button){

    const answer =

        button.nextElementSibling;

    if(answer.style.display==="block"){

        answer.style.display="none";

        button.innerHTML="👁 Show Answer";

    }

    else{

        answer.style.display="block";

        button.innerHTML="🙈 Hide Answer";

    }

}



// =========================================
// QUIZ GENERATOR
// =========================================

async function generateQuiz(){

    loading("quizBox");

    scrollToBox("quizBox");

    try{

        const data = await postData(

            "/quiz",

            "text"

        );

        if(!data.success){

            throw new Error(data.error);

        }

        let html =

`

<div class="ai-card fadeIn">

<div class="cardHeader">

<h2>

🧩 Generated Quiz

</h2>

<button

class="copyBtn"

onclick="copyText(document.getElementById('quizBox').innerText)">

📋 Copy

</button>

</div>

`;

        data.quiz.forEach((question,index)=>{

            html += quizCard(

                question,

                index

            );

        });

        html += `

</div>

`;

    document.getElementById("quizBox").innerHTML = html;

finalizeRender();

    }

    catch(err){

      renderError(
    "quizBox",
    err.message
);

    }

}
// =========================================
// RESPONSE ANIMATIONS
// =========================================

function animateCards(){

    document.querySelectorAll(".ai-card").forEach(card=>{

        card.animate(

            [

                {

                    opacity:0,

                    transform:"translateY(20px) scale(.98)"

                },

                {

                    opacity:1,

                    transform:"translateY(0) scale(1)"

                }

            ],

            {

                duration:450,

                easing:"ease-out",

                fill:"forwards"

            }

        );

    });

}



// =========================================
// BEAUTIFY CODE BLOCKS
// =========================================

function styleCodeBlocks(){

    document.querySelectorAll("pre").forEach(pre=>{

        pre.classList.add("codeBlock");

    });

    document.querySelectorAll("code").forEach(code=>{

        code.classList.add("inlineCode");

    });

}



// =========================================
// AFTER EVERY RESPONSE
// =========================================

function finalizeRender(){

    styleCodeBlocks();

    animateCards();

}



// =========================================
// LOADING BAR
// =========================================

function startProgress(boxId){

    const box = document.getElementById(boxId);

    const bar=document.createElement("div");

    bar.className="progressBar";

    bar.innerHTML="<span></span>";

    box.prepend(bar);

}



// =========================================
// AUTO RESIZE TEXTAREA
// =========================================

input.addEventListener("input",()=>{

    input.style.height="auto";

    input.style.height=input.scrollHeight+"px";

});



// =========================================
// KEYBOARD SHORTCUTS
// =========================================

input.addEventListener("keydown",(event)=>{

    if(event.ctrlKey && event.key==="Enter"){

        askQuestion();

    }

    if(event.altKey && event.key==="1"){

        askQuestion();

    }

    if(event.altKey && event.key==="2"){

        explain();

    }

    if(event.altKey && event.key==="3"){

        summarize();

    }

    if(event.altKey && event.key==="4"){

        generateQuiz();

    }

    if(event.altKey && event.key==="5"){

        learningPath();

    }

});



// =========================================
// FOCUS INPUT
// =========================================

window.addEventListener("load",()=>{

    input.focus();

});



// =========================================
// EduGenie AI
// FINAL INITIALIZATION
// =========================================

// ---------- Session Statistics ----------

const session = {

    requests: 0,

    totalWords: 0,

    started: new Date()

};

function updateSession(text){

    session.requests++;

    session.totalWords += text.split(/\s+/).length;

}



// ---------- Status Indicator ----------

function setStatus(status){

    let badge = document.getElementById("statusBadge");

    if(!badge) return;

    badge.innerHTML = status;

}



// ---------- Wrapper for Responses ----------

function renderResponse(boxId,title,text){

    updateSession(text);

    document.getElementById(boxId).innerHTML =

        responseCard(title,text);

    finalizeRender();

}



// ---------- Wrapper for Errors ----------

function renderError(boxId,error){

    document.getElementById(boxId).innerHTML =

        errorCard(error);

    finalizeRender();

}



// ---------- Random Placeholder ----------

const placeholders=[

"Explain Artificial Intelligence.",

"What is Cloud Computing?",

"Summarize this chapter.",

"Generate quiz from this passage.",

"Create a learning roadmap for Python.",

"Explain Binary Search with example.",

"What is Machine Learning?",

"Difference between Stack and Queue."

];

window.addEventListener("load",()=>{

    input.placeholder =

        placeholders[

            Math.floor(

                Math.random()*placeholders.length

            )

        ];

});



// ---------- Ripple Effect ----------

document.querySelectorAll(".module button")

.forEach(button=>{

    button.addEventListener("click",function(e){

        const circle=document.createElement("span");

        circle.className="ripple";

        circle.style.left=e.offsetX+"px";

        circle.style.top=e.offsetY+"px";

        this.appendChild(circle);

        setTimeout(()=>{

            circle.remove();

        },600);

    });

});



// ---------- Welcome Toast ----------

window.addEventListener("load",()=>{

    setTimeout(()=>{

        showToast("🎓 EduGenie AI Ready");

    },600);

});



// ---------- Auto Save Input ----------

input.value=

localStorage.getItem("edugenie_input") || "";

input.dispatchEvent(new Event("input"));

input.addEventListener("input",()=>{

    localStorage.setItem(

        "edugenie_input",

        input.value

    );

});



// ---------- Keyboard Escape ----------

document.addEventListener("keydown",(event)=>{

    if(event.key==="Escape"){

        input.value="";

        input.dispatchEvent(new Event("input"));

        input.focus();

        showToast("Input cleared.");

    }

});



// ---------- Footer Info ----------

window.addEventListener("load",()=>{

    const footer=document.querySelector("footer");

    if(footer){

        footer.innerHTML +=

        `

        <br>

        <small>

        Session Started :

        ${session.started.toLocaleTimeString()}

        </small>

        `;

    }

});



// ---------- Startup Animation ----------

window.addEventListener("load",()=>{

    document.querySelectorAll(".module")

    .forEach((card,index)=>{

        card.animate(

            [

                {

                    opacity:0,

                    transform:"translateY(30px)"

                },

                {

                    opacity:1,

                    transform:"translateY(0)"

                }

            ],

            {

                duration:600,

                delay:index*120,

                fill:"forwards",

                easing:"ease"

            }

        );

    });

});



// ---------- Console Signature ----------

console.log(

"%cEduGenie AI Loaded",

"color:#6C63FF;font-size:18px;font-weight:bold"

);

console.log(

"Powered by Google Gemini"

);
// ======================================
// COPY ALL RESPONSES
// ======================================

function copyAll() {

    let text = "";

    text += document.getElementById("qnaBox").innerText + "\n\n";
    text += document.getElementById("explainBox").innerText + "\n\n";
    text += document.getElementById("summaryBox").innerText + "\n\n";
    text += document.getElementById("quizBox").innerText + "\n\n";
    text += document.getElementById("pathBox").innerText;

    navigator.clipboard.writeText(text);

    showToast("📋 All responses copied!");
}
// =========================================
// COPY ALL OUTPUTS
// =========================================

function copyEntirePage(){

    let text = "";

    document.querySelectorAll(".outputBox").forEach(box => {

        text += box.innerText + "\n\n";

    });

    navigator.clipboard.writeText(text);

    showToast("📋 Copied All Responses");

}



// =========================================
// CLEAR ALL OUTPUTS
// =========================================

function clearOutputs(){

    document.querySelectorAll(".outputBox").forEach(box => {

        box.innerHTML = `
            <div class="placeholder">
                Waiting for response...
            </div>
        `;

    });

    showToast("🗑 Cleared");

}



// =========================================
// SCROLL TOP
// =========================================

function scrollTopSmooth(){

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

}
