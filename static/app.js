const countUps = document.querySelectorAll(".count-up");
const formatNumber = new Intl.NumberFormat("en-US");
const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
).matches;

function setCount(element) {
    element.textContent = formatNumber.format(
        Number(element.dataset.target)
    );
}

function countUp(element) {
    const target = Number(element.dataset.target);
    const duration = 1600;
    let startedAt;

    function update(timestamp) {
        if (startedAt === undefined) {
            startedAt = timestamp;
        }

        const progress = Math.min(
            (timestamp - startedAt) / duration,
            1
        );

        element.textContent = formatNumber.format(
            Math.round(target * (1 - Math.pow(1 - progress, 3)))
        );

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

if (reduceMotion || !("IntersectionObserver" in window)) {
    countUps.forEach(setCount);
} else {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                countUp(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    countUps.forEach((element) => {
        observer.observe(element);
    });
}