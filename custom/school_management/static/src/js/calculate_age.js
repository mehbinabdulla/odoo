$(document).ready(function() {
  $('#dob').on('change', function() {
    var dob = new Date(this.value);
    var today = new Date();
    var age = Math.floor((today - dob) / (365.25 * 24 * 60 * 60 * 1000));
    $('#age').val(age);
  });
});