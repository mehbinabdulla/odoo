 $(document).ready(function() {
    $("#department_name").val('Department')
    $("#class_id").on( "change", function() {
    if (this.value) {
        fetch(`/api/class/${this.value}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            var res = data.result
            $("#department_id").val(res.department_id.id)
            $("#department_name").val(res.department_id.name)
        })
        .catch(error => {
            console.log(error)
        });
    } else {
        $("#department_id").val()
        $("#department_name").val('Department')
    }
    });
    $("#class_id").trigger('change')

});