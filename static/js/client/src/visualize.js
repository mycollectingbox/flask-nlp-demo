window.addEventListener("load", function(event) {
    // console.log("All resources finished loading!");
    
    // 1. Add functionality of Clear button
    var clearElement = document.getElementById("reset");

    clearElement.addEventListener("click", function(){
        if (document.getElementById("parse") != null) {
            document.getElementById("parse").innerHTML = "";
        }
        if (document.getElementById("detectField") != null) {
            document.getElementById("detectField").innerHTML = "";
        }
        if (document.getElementById("tagSeqField") != null) {
            document.getElementById("tagSeqField").innerHTML = "";
        }
    });

    var sliderElement = document.getElementById("imgsize");
    var imageElement = document.getElementById("theImgId");
    var sizeElement = document.getElementById("imageSizeText");
    if (sliderElement != null) {
        var slider = new Slider('#imgsize', {
            formatter: function(value) { return 'Current value: ' + value;}
        });

        slider.on("change", function(event) {
            imageElement.style.maxWidth = event.newValue.toString() + "%";
            sizeElement.innerHTML = event.newValue.toString() + "%";
        });
    }
});