$(document).ready(function() {
    const isWeekend = (date) => {
        const day = date.getDay();
        return day === 0 || day === 6;
    }

    const duration = () => {
        $('#date_to').removeAttr('readonly');
        $('#half_day').attr('disabled','')
        if ($('#date_to').val() && $('#date_from').val()) {
            const dateTo = new Date($('#date_to').val());
            const dateFrom = new Date($('#date_from').val());
            let duration = 0;
            let currentDate = dateFrom;
            while (currentDate <= dateTo) {
                if (!isWeekend(currentDate)) {
                    duration++;
                }
                currentDate.setDate(currentDate.getDate() + 1);
            }
            duration >= 0 ? $('#number_of_days').val(duration) : $('#number_of_days').val(0)
        }
        if($('#is_half_day').is(':checked')) {
            $('#date_to').val($('#date_from').val());
            $('#date_to').attr('readonly', '');
            $('#number_of_days').val(0.5);
            $('#half_day').removeAttr('disabled');
        }
    }

    duration();
    $('#is_half_day').on('change', function(){
        duration()
    });
    $('#date_from').on('change', function() {
        duration();
        if (this.value != '') {
            $('#date_to').attr('min', this.value);
        } else {
            $('#date_to').attr('min', '');
        }
    });
    $('#date_to').on('change', function() {
        duration();
        if (this.value != '') {
            $('#date_from').attr('max', this.value);
        } else {
            $('#date_from').attr('max', '');
        }
    });
});