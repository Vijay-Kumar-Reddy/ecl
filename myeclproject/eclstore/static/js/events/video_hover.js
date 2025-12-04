document.addEventListener("DOMContentLoaded", () => {
    const videos = document.querySelectorAll(".event-video");

    videos.forEach(video => {

        video.addEventListener("mouseenter", () => {
            video.muted = true;
            video.play().catch(() => {});
        });

        video.addEventListener("mouseleave", () => {
            video.pause();
            video.currentTime = 0;
        });

        video.addEventListener("click", () => {
            video.setAttribute("controls", "true");

            if (video.requestFullscreen) video.requestFullscreen();
            else if (video.webkitRequestFullscreen) video.webkitRequestFullscreen();

            video.play();
        });

        video.addEventListener("fullscreenchange", () => {
            if (!document.fullscreenElement) {
                video.removeAttribute("controls");
            }
        });
    });
});
