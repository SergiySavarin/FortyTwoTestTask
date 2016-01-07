$(document).ready(function() {

    function block_form() {
        $("#form_loading").show();
        $('textarea').attr('disabled', 'disabled');
        $('input').attr('disabled', 'disabled');
    }

    function unblock_form() {
        $('#form_loading').hide();
        $('textarea').removeAttr('disabled');
        $('input').removeAttr('disabled');
        $('.errorlist').remove();
    }
    // Make form ajax
    $('#editContact').ajaxForm({
        beforeSubmit: function(form, options) {
            block_form();
        },
        success: function() {
            unblock_form();
            $("#form_success").show();
            setTimeout(function() {
                $("#form_success").hide();
            }, 3000);
        },
        error:  function(resp) {
            unblock_form();
            $("#form_error").show();
            // render errors ander form fields
            var errors = JSON.parse(resp.responseText);
            for (error in errors) {
                var id = '#' + error;
                $(id).parent('div').append(errors[error]).css('color', 'red');
            }
            setTimeout(function() {
                $("#form_error").hide();
            }, 3000);
        }
    });

    $('#data_saved').hide();
    $('#birthday').datetimepicker({
        'format': 'MM/DD/YYYY',
    });

    function readURL(input) {

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#blah').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#photo").change(function(){
        readURL(this);
    });
});