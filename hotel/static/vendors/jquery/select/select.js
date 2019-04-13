$(() => {
    $('.select').select2({
        allowClear: true,
        placeholder: 'Choose An Option',
        minimumResultsForSearch: -1
    });
    $('.photo__search-visitors').select2({
        allowClear: true,
        placeholder: 'Выберите количество гостей',
        minimumResultsForSearch: -1
    });
});