function analyzeResume() {

const fileInput = document.getElementById("resumeFile");
const result = document.getElementById("result");
const progressBar = document.getElementById("progressBar");

if (fileInput.files.length === 0) {
    result.innerHTML = "❌ Please upload a resume first.";
    result.style.color = "red";
    return;
}

const fileName = fileInput.files[0].name;

document.getElementById("previewName").innerHTML =
    "📄 Selected File: " + fileName;

document.getElementById("previewNameCard").innerHTML =
    fileName;

const formData = new FormData();
formData.append("resume", fileInput.files[0]);

fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    body: formData
})
.then(response => response.json())
.then(data => {

    console.log(data);

    const score = data.ats_score;

    // Domain
    document.getElementById("domain").innerHTML =
        data.domain;

    // Missing Skills
    document.getElementById("missingSkills").innerHTML =
        data.missing_skills.join(", ");

    // ATS Score
    document.getElementById("circleScore").innerHTML =
        score + "%";

    // Resume Strength
    document.getElementById("strengthText").innerHTML =
        data.strength;

    // Skills
    document.getElementById("skillsList").innerHTML =
        data.skills.join(", ");

    // Recommendations
    document.getElementById("recommendations").innerHTML =
        data.recommendations.join("<br>");

    // Progress Bar
    document.querySelector(".progress-container").style.display = "block";

    progressBar.style.width = score + "%";

    if (score >= 90) {
        progressBar.style.background = "limegreen";
    }
    else if (score >= 75) {
        progressBar.style.background = "gold";
    }
    else {
        progressBar.style.background = "red";
    }

    result.innerHTML = `
    ✅ Resume Uploaded Successfully! <br><br>
    📄 File Name: ${data.filename} <br>
    ⭐ ATS Score: ${score}/100 <br>
    🎯 Domain: ${data.domain}
    `;

    result.style.color = "lightgreen";

})
.catch(error => {

    console.log(error);

    result.innerHTML =
        "❌ Backend Error. Check Flask Server.";

    result.style.color = "red";
});

}

function toggleTheme() {
document.body.classList.toggle("dark-mode");
}

const fileInput = document.getElementById("resumeFile");

if (fileInput) {
fileInput.addEventListener("change", function () {

    document.getElementById("previewName").innerHTML =
        "📄 Resume Ready";

    document.getElementById("previewNameCard").innerHTML =
        this.files[0].name;
});

}
function downloadReport() {
    window.open("http://127.0.0.1:5000/download-report", "_blank");
}