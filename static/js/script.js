document.addEventListener('DOMContentLoaded', function() {
    const scrollerContent = document.querySelector('.scroller-content');
    const itemCount = document.querySelectorAll('.scroller-item').length;

    // Adjust the animation duration based on the number of items
    const baseSpeed = 180; // Base speed for 200 items
    const speed = (itemCount / 200) * baseSpeed; // Adjust speed based on item count

    scrollerContent.style.animationDuration = `${speed}s`; // Apply new speed
});
