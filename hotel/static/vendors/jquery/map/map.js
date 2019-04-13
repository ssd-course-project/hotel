ymaps.ready(init);
    function init(){
        var myMap = new ymaps.Map("map", {
            center: [52.366870, 4.898620],
            zoom: 14,
            controls: [],
        }, {
            suppressMapOpenBlock: true,
            balloonPanelMaxMapArea: Infinity,
            balloonCloseButton: false
        });
        var customBalloonContentLayout = ymaps.templateLayoutFactory.createClass([
            '<div class="map-balloon">' +
            '<div class="map-balloon__container">' +
            '<div class="map-balloon__title"> Наш адрес </div>' +
            '<div class="map-balloon__address">Амстел 17,<br>Амстердам, Нидерланды</div>' +
            '</div>' +
            '</div>'
        ].join(''));
        myMap.geoObjects
        .add(new ymaps.Placemark([52.366870, 4.898620], {}, {
            balloonContentLayout: customBalloonContentLayout,
            preset: 'islands#redIcon'
        }))
    }