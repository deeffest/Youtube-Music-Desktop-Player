var s = document.querySelector(".volume-slider");
s && (
    s.value = Math.min(+s.value + 5, 100),
    s.dispatchEvent(new Event("change"))
);
