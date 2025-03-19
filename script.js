// Image Upload Preview
document.getElementById("imageUpload").addEventListener("change", function(event) {
    let preview = document.getElementById("imagePreview");
    preview.innerHTML = "";
    Array.from(event.target.files).forEach(file => {
        let img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.classList.add("preview-img");
        preview.appendChild(img);
    });
});

// Music Upload Preview
document.getElementById("musicUpload").addEventListener("change", function(event) {
    let musicPreview = document.getElementById("musicPreview");
    musicPreview.innerHTML = "";
    let file = event.target.files[0];
    if (file) {
        let audio = document.createElement("audio");
        audio.controls = true;
        audio.src = URL.createObjectURL(file);
        musicPreview.appendChild(audio);
    }
});

// Create Video
document.getElementById("createVideoBtn").addEventListener("click", function() {
    let videoPreview = document.getElementById("videoPreview");
    let format = document.getElementById("videoFormat").value;
    let quality = document.getElementById("videoQuality").value;
    let duration = document.getElementById("videoDuration").value;
    let message = document.getElementById("customMessage").value;

    videoPreview.innerHTML = "<p>Your video is being generated... 🎥</p>";

    setTimeout(() => {
        let videoWidth = format === "landscape" ? "500px" : "300px";
        let videoHeight = format === "landscape" ? "300px" : "500px";

        videoPreview.innerHTML = `
            <video width='${videoWidth}' height='${videoHeight}' controls style="border: 3px solid #007BFF; border-radius: 8px;">
                <source src='demo.mp4' type='video/mp4'>
            </video>
            <p style="color: #0056b3;">${message} (Duration: ${duration}s)</p>
        `;

        document.getElementById("downloadBtn").style.display = "block";
    }, 3000);
});
