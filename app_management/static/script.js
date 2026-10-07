function getCookie(name) {
    const item = document.cookie
        .split("; ")
        .find((cookie) => cookie.startsWith(name + "="));
    return item ? decodeURIComponent(item.split("=")[1]) : "";
}

document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = getCookie("csrftoken");
    const addAppForm = document.getElementById("add-app-form");
    const formStatus = document.getElementById("form-status");

    if (addAppForm) {
        addAppForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const response = await fetch("/api/apps/", {
                method: "POST",
                body: new FormData(addAppForm),
                credentials: "same-origin",
                headers: {"X-CSRFToken": csrfToken},
            });
            if (formStatus) {
                formStatus.textContent = response.ok
                    ? "App added successfully."
                    : "Unable to add the app.";
            }
            if (response.ok) addAppForm.reset();
        });
    }

    const dropArea = document.getElementById("drop-area");
    const screenshot = document.getElementById("screenshot");
    const uploadButton = document.getElementById("upload-task");
    const uploadStatus = document.getElementById("upload-status");

    document.querySelectorAll("[data-start-task]").forEach((button) => {
        button.addEventListener("click", () => {
            if (!dropArea) return;
            dropArea.dataset.appId = button.dataset.startTask;
            dropArea.hidden = false;
            screenshot?.focus();
        });
    });

    if (uploadButton && dropArea && screenshot) {
        uploadButton.addEventListener("click", async () => {
            const file = screenshot.files[0];
            if (!file) {
                uploadStatus.textContent = "Choose an image first.";
                return;
            }
            const formData = new FormData();
            formData.append("app", dropArea.dataset.appId);
            formData.append("screenshot", file);
            const response = await fetch("/api/tasks/", {
                method: "POST",
                body: formData,
                credentials: "same-origin",
                headers: {"X-CSRFToken": csrfToken},
            });
            uploadStatus.textContent = response.ok
                ? "Screenshot uploaded successfully."
                : "Unable to upload the screenshot.";
            if (response.ok) screenshot.value = "";
        });
    }
});
