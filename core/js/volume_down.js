var s = document.querySelector(".volume-slider");
if (s) {
    s.value = Math.max(+s.value - 5, 0);
    s.dispatchEvent(new Event("change"));
}
