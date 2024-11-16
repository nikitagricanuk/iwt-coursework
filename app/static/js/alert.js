// Automatically fade alerts after 3 seconds
document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove("show"); // Remove Bootstrap's "show" class
            alert.classList.add("fade");   // Add Bootstrap's "fade" class for transition
            setTimeout(() => alert.remove(), 150); // Remove from DOM after animation
        }, 3000); // 3-second delay
    });
});