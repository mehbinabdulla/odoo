 $(document).ready(function() {
    $("#student_id").on( "change", function() {
    if (this.value) {
        fetch(`/api/student/${this.value}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            var res = data.result
            $("#class_id").val(res.class_id.id)
            $("#class_name").val(res.class_id.name)
        })
        .catch(error => {
            console.log(error)
        });
    } else {
        $("#class_id").val()
        $("#class_name").val('Class')
    }
    });
});