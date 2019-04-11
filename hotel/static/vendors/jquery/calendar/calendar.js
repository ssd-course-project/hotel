$(document).ready(function() {

    $.extend($.datepicker, {
        // Reference the orignal function so we can override it and call it later
        _inlineDatepicker2: $.datepicker._inlineDatepicker,
        // Override the _inlineDatepicker method
        _inlineDatepicker: function (target, inst) {
            // Call the original
            this._inlineDatepicker2(target, inst);
            var beforeShow = $.datepicker._get(inst, 'beforeShow');
            if (beforeShow) {
                beforeShow.apply(target, [target, inst]);
            }
        }
    });

    $('.datepicker').datepicker({
        dateFormat: 'dd.mm.yy',
        firstDay: 1,
        showOtherMonths: true,
        selectOtherMonths: true,
        showButtonPanel: true,
        dayNamesMin: [ "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" ],
        beforeShow: function(){
            setTimeout(function(){
                var d = new Date();
                var day = d.getDate();
                $('.datepicker-day').text(day);
            }, 10);
        },
        onSelect: function(dateText, inst) {
            $(this).parent().children('.datepicker-day').html(inst.currentDay);
        },
    });

    $.datepicker._gotoToday = function(id) {
        var target = $(id);
        var inst = this._getInst(target[0]);
        if (this._get(inst, 'gotoCurrent') && inst.currentDay) {
            inst.selectedDay = inst.currentDay;
            inst.drawMonth = inst.selectedMonth = inst.currentMonth;
            inst.drawYear = inst.selectedYear = inst.currentYear;
        }
        else {
            var date = new Date();
            inst.selectedDay = date.getDate();
            inst.drawMonth = inst.selectedMonth = date.getMonth();
            inst.drawYear = inst.selectedYear = date.getFullYear();
            // the below two lines are new
            this._setDateDatepicker(target, date);
            this._selectDate(id, this._getDateDatepicker(target));
        }
        this._notifyChange(inst);
        this._adjustDate(target);
    }
});