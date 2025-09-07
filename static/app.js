// // --- DOM Elements ---
const welcomeSection = document.getElementById('welcome-section');
const resumeInputSection = document.getElementById('resume-input-section');
const jobDetailsSection = document.getElementById('job-details-section');
const coverLetterSection = document.getElementById('cover-letter-section');

const uploadResumeCard = document.getElementById('upload-resume-card');
const fillFormCard = document.getElementById('fill-form-card');

const uploadResumeSubSection = document.getElementById('upload-resume-sub-section');
const manualFormSubSection = document.getElementById('manual-form-sub-section');

const resumeFile = document.getElementById('resume-file');
const uploadResumeBtn = document.getElementById('upload-resume-btn');
const manualResumeForm = document.getElementById('manual-resume-form');
const jobDetailsForm = document.getElementById('job-details-form');
const coverLetterOutput = document.getElementById('cover-letter-output');
const startOverBtn = document.getElementById('start-over-btn');

let resumeData = {}; // To store either uploaded file or form data

// --- Helper Function to Show Sections ---
function showSection(sectionToShow) {
const sections = [welcomeSection, resumeInputSection, jobDetailsSection, coverLetterSection];
sections.forEach(section => {
    section.classList.remove('active');
});
sectionToShow.classList.add('active');
}

// --- Event Listeners ---

// Welcome section choices
uploadResumeCard.addEventListener('click', () => {
uploadResumeSubSection.classList.remove('hidden');
manualFormSubSection.classList.add('hidden');
showSection(resumeInputSection);
});

fillFormCard.addEventListener('click', () => {
manualFormSubSection.classList.remove('hidden');
uploadResumeSubSection.classList.add('hidden');
showSection(resumeInputSection);
});

// Handle resume file upload (placeholder for actual upload logic)
uploadResumeBtn.addEventListener('click', () => {
const file = resumeFile.files[0];
if (file) {
    console.log('Resume file selected:', file.name);
    // In a real application, you would send this file to your FastAPI backend
    // using FormData and fetch API.
    // Example:
    // const formData = new FormData();
    // formData.append('resume', file);
    // fetch('/upload-resume', { method: 'POST', body: formData })
    // .then(response => response.json())
    // .then(data => {
    //     console.log('Resume upload response:', data);
    //     resumeData.type = 'file';
    //     resumeData.filename = file.name;
    //     showSection(jobDetailsSection);
    // })
    // .catch(error => console.error('Error uploading resume:', error));

    resumeData = { type: 'pdf', resume: file };
    showSection(jobDetailsSection);
} else {
    alert('Please select a PDF resume file.');
}
});

// Handle manual form submission
manualResumeForm.addEventListener('submit', (event) => {
event.preventDefault(); // Prevent default form submission
const formData = new FormData(manualResumeForm);
resumeData = {
    type: 'manual',
    profile: {
        name: formData.get('name'),
        experience: formData.get('experience'),
        skills: formData.get('skills'),
        projects: formData.get('projects')
    }
};
console.log('Manual resume data:', resumeData);
showSection(jobDetailsSection);
});

// Handle job details submission and cover letter generation
jobDetailsForm.addEventListener('submit', async (event) => {
event.preventDefault(); // Prevent default form submission

const jobTitle = document.getElementById('job-title').value;
const jobDescription = document.getElementById('job-description').value;
const tone = document.getElementById("tone")

console.log('Job Title:', jobTitle);
console.log('Job Description:', jobDescription);
console.log('Tone:', tone);

// Show the cover letter section and a loading message
showSection(coverLetterSection);
coverLetterOutput.textContent = 'Generating your personalized cover letter... Please wait.';

// --- Simulate API Call to FastAPI Backend ---
// In a real application, you would send resumeData, jobTitle, and jobDescription
// to your FastAPI backend to generate the cover letter.
// Example using fetch API:

try {
    let route = "";
    let response = null;

    if (resumeData["type"] === "pdf") {
        route = "/cover-letter/resume";

        // ✅ Use FormData for multipart
        const formData = new FormData();
        formData.append("resume", resumeData["resume"]); // resumeData["resume"] should be a File object
        formData.append("job_title", jobTitle);
        formData.append("job_description", jobDescription);
        formData.append("tone", tone.value);

        response = await fetch(route, {
            method: "POST",
            body: formData, // no need to set Content-Type manually, browser sets it
        });
    } else {
        route = "/cover-letter/form";

        response = await fetch(route, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            
            body: JSON.stringify({
                profile: resumeData.profile,
                job_description: {
                    job_title: jobTitle,
                    job_requirements: jobDescription,
                },
                tone: tone.value,
            }),
        });
    }

    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    coverLetterOutput.textContent = data.cover_letter; // Assuming your backend returns { "cover_letter": "..." }
} catch (error) {
    console.error('Error generating cover letter:', error);
    coverLetterOutput.textContent = 'Failed to generate cover letter. Please try again. Error: ' + error.message;
}


// --- Placeholder for actual cover letter generation ---
// Simulate a delay for API call
setTimeout(() => {
    const simulatedCoverLetter = `
Dear [Hiring Manager Name],

I am writing to express my enthusiastic interest in the ${jobTitle} position, as advertised on [Platform where you saw the ad]. With my background in ${resumeData.experience || 'software development'} and a strong proficiency in ${resumeData.skills || 'various technologies'}, I am confident that my skills and experience align perfectly with the requirements outlined in your job description.

During my career, I have successfully ${resumeData.projects || 'led and contributed to various projects, developing robust solutions and optimizing existing systems'}. My expertise includes ${resumeData.skills || 'a wide range of programming languages and tools'}, which I believe will be highly beneficial in contributing to your team's objectives.

I am particularly drawn to this opportunity at [Company Name] because ${jobDescription.substring(0, 150)}... I am eager to leverage my abilities to [mention a specific goal related to the job description, e.g., 'develop innovative solutions' or 'drive product success'].

Thank you for considering my application. I have attached my resume for your review and welcome the opportunity to discuss how my qualifications can benefit your organization.

Sincerely,
${resumeData.name || 'Your Name'}
    `;
    // coverLetterOutput.textContent = simulatedCoverLetter;
}, 2000); // Simulate 2-second delay for generation
});

// Start over button
startOverBtn.addEventListener('click', () => {
// Reset forms
manualResumeForm.reset();
jobDetailsForm.reset();
resumeFile.value = ''; // Clear file input
coverLetterOutput.textContent = ''; // Clear cover letter output

// Hide sub-sections
uploadResumeSubSection.classList.add('hidden');
manualFormSubSection.classList.add('hidden');

// Show welcome section
showSection(welcomeSection);
});

// Initial state: show welcome section
showSection(welcomeSection);