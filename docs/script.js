async function analyzeResume() {
    const file = document.getElementById("resume").files[0];
    const jobDescription =
        document.getElementById("jobDescription").value;

    const result = document.getElementById("result");

    if (!file) {
        alert("Please select a PDF resume.");
        return;
    }

    if (!jobDescription.trim()) {
        alert("Please enter a job description.");
        return;
    }

    const formData = new FormData();

    formData.append("file", file);
    formData.append("job_description", jobDescription);

    result.innerHTML = `
        <div class="feedback">
            <p>⏳ Analyzing your resume...</p>
        </div>
    `;

    try {
        const response = await fetch(
            "https://ai-resume-screener-yz9s.onrender.com/upload-resume",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Something went wrong"
            );
        }

        result.innerHTML = `
            <h2>📊 Resume Analysis Dashboard</h2>

            <div class="score-card">

                <div class="score">
                    ${data.match_percentage}%
                </div>

                <p>Overall Job Match</p>

                <div class="progress-container">

                    <div
                        class="progress-bar"
                        style="width: ${data.match_percentage}%"
                    >
                        ${data.match_percentage}%
                    </div>

                </div>

            </div>


            <h3>🤖 AI Analysis</h3>

            <div class="feedback ai-analysis">

                <p>${data.ai_analysis}</p>

            </div>


            <h3>📄 Resume Summary</h3>

            <div class="feedback">

                <p>${data.summary}</p>

            </div>


            <h3>💻 Skills Analysis</h3>

            <div class="feedback">

                <strong>Matched Skills</strong>

                <div class="skills matched">

                    ${
                        data.matched_skills.length > 0
                            ? data.matched_skills
                                .map(
                                    skill =>
                                        `<span>✓ ${skill}</span>`
                                )
                                .join("")
                            : "<span>None</span>"
                    }

                </div>


                <strong>Missing Skills</strong>

                <div class="skills missing">

                    ${
                        data.missing_skills.length > 0
                            ? data.missing_skills
                                .map(
                                    skill =>
                                        `<span>✗ ${skill}</span>`
                                )
                                .join("")
                            : "<span>None</span>"
                    }

                </div>

            </div>


            <h3>💼 Experience</h3>

            <div class="feedback">

                ${
                    data.experience.length > 0
                        ? data.experience
                            .map(
                                item =>
                                    `<p>💼 ${item}</p>`
                            )
                            .join("")
                        : "<p>No experience information detected.</p>"
                }

            </div>


            <h3>🎓 Education</h3>

            <div class="feedback">

                ${
                    data.education.length > 0
                        ? data.education
                            .map(
                                item =>
                                    `<p>🎓 ${item}</p>`
                            )
                            .join("")
                        : "<p>No education information detected.</p>"
                }

            </div>


            <h3>💪 Strengths</h3>

            <div class="feedback strengths-box">

                ${
                    data.strengths.length > 0
                        ? data.strengths
                            .map(
                                item =>
                                    `<p>✓ ${item}</p>`
                            )
                            .join("")
                        : "<p>No specific strengths detected.</p>"
                }

            </div>


            <h3>💡 Resume Feedback</h3>

            <div class="feedback">

                ${
                    data.feedback.length > 0
                        ? data.feedback
                            .map(
                                item =>
                                    `<p>• ${item}</p>`
                            )
                            .join("")
                        : "<p>No additional feedback.</p>"
                }

            </div>
        `;

    } catch (error) {

        console.error("Error:", error);

        result.innerHTML = `
            <div class="feedback">

                <p>
                    ❌ ${error.message}
                </p>

            </div>
        `;
    }
}
