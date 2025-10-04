var s = document.querySelector(".volume-slider");
if (s) {
    s.value = Math.min(+s.value + 5, 100);
    s.dispatchEvent(new Event("change"));
}
