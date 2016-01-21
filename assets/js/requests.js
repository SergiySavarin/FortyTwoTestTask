var COUNT = 0;
var START = 0;
var END = 0;

setInterval(function() {
    $.ajax({
        url: REQUESTS_URL,
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            if (START == 0) {
                START = data.count;
            }
            if (END == 0) {
                END = data.count;
            }
            if (data.count > START) {
                END = data.count;
            }
            COUNT = END - START;
            $('title').text(COUNT);
            if (COUNT > 0) {
                $('#result').html('');
                for (index in data.request) {
                    var text = data.request[index];
                    $('#result').append('<p>' + text);
                }
            }
        }
    });
}, 1000);

function mOver() {
    START = 0;
    END = 0;
    $('title').text(0);
    $('p').css('color', '#551A8B');
};

document.addEventListener('visibilitychange', function(){
    START = 0;
    END = 0;
    document.title = 0;
    $('p').css('color', '#551A8B');
});

$(document).ready(function(){
    $('#priority-selector select').val($.cookie('current_priority'))
    $('#priority-selector select').change(function(event){
        var priority = $(this).val();
        if (priority) {
            $.cookie(
                'current_priority', priority,
                {'path': '/requests/', 'expires': 365}
            );
        } else {
            $.removeCookie('current_priority', {'path': '/requests/'});
        }
        $.ajax({
            url: REQUESTS_URL,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#result').html('');
                for (index in data.request) {
                    var text = data.request[index];
                    $('#result').append('<p>' + text);
                }
            }
        });
        return true;
    });
});