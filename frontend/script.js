document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const restoreBtn = document.getElementById("restoreBtn");
    const loader = document.getElementById("loader");

    if (!fileInput.files.length) {
        alert("Please upload an image first!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        // Disable button & show loader
        restoreBtn.disabled = true;
        loader.classList.remove("hidden");

        const response = await fetch("/restore", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Image restoration failed");
        }

        // Blob response for image
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);

        document.getElementById("restoredImage").src = imageUrl;
    } catch (err) {
        alert("Error: " + err.message);
        console.error(err);
    } finally {
        // Enable button & hide loader
        restoreBtn.disabled = false;
        loader.classList.add("hidden");
    }
});
