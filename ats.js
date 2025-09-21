const fileInput = document.getElementById("resume");
const uploadText = document.getElementById("upload-text");

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    uploadText.textContent = fileInput.files[0].name;
  } else {
    uploadText.textContent = "Click to choose your resume file";
  }
});

document.getElementById("ats-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  let formData = new FormData();
  formData.append("resume", fileInput.files[0]);
  formData.append("job_desc", document.getElementById("job-desc").value);

  let resultDiv = document.getElementById("ats-result");
  resultDiv.style.display = "block";
  resultDiv.innerHTML = "<p>Calculating score...</p>";

  try {
    let res = await fetch("http://127.0.0.1:8000/ats-check", {
      method: "POST",
      body: formData
    });

    let data = await res.json();

    if (data.error) {
      resultDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
    } else {
      let keywords = data.keywords ? data.keywords.join(", ") : "N/A";
      resultDiv.innerHTML = `
        <h2>ATS Score: ${data.score}%</h2>
        <p><strong>Matched Resume Keywords:</strong> ${keywords}</p>
      `;
    }
  } catch (err) {
    resultDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
  }
});
