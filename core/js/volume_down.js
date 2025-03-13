var volumeSlider = document.querySelector(".volume-slider");

if (volumeSlider) {
    var currentSliderValue = volumeSlider.value;
    var newSliderValue = Math.max(parseInt(currentSliderValue) - 5, 0);

    volumeSlider.value = newSliderValue;

    var event = new Event("change");
    volumeSlider.dispatchEvent(event);
}
