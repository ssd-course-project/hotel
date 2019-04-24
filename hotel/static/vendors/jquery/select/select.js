$(() => {
    $('.select').select2({
        allowClear: true,
        placeholder: 'Choose An Option',
        minimumResultsForSearch: -1
    });
    $('.visitors').select2({
        allowClear: true,
        placeholder: 'Выберите количество гостей',
        minimumResultsForSearch: -1
    });
});