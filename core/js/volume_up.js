var volumeSlider = document.querySelector(".volume-slider");

if (volumeSlider) {
    var currentSliderValue = volumeSlider.value;
    var newSliderValue = Math.min(parseInt(currentSliderValue) + 5, 100);

    volumeSlider.value = newSliderValue;

    var event = new Event("change");
    volumeSlider.dispatchEvent(event);
}
