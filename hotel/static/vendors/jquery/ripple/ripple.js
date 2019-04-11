$(() => {
    var elements = document.querySelectorAll('.enable-ripple');

    Array.prototype.forEach.call(elements, function (button) {
        button.addEventListener('click', ripple)
    });

    function ripple (event) {
        var element = event.currentTarget;

        var rippleElement = document.querySelector('span.ripple-effect');
            if(!rippleElement) {
                rippleElement = document.createElement('span');
            }
        element.appendChild(rippleElement);

        var max = Math.max(element.offsetWidth, element.offsetHeight);
        rippleElement.style.width = rippleElement.style.height = max + 'px';

        var rect = element.getBoundingClientRect();
        rippleElement.style.left = event.clientX - rect.left - max / 2 + 'px';
        rippleElement.style.top = event.clientY - rect.top - max / 2 + 'px';

        rippleElement.classList.add('ripple-effect');
    }
});