$(document).ready(function(){
    // Получаем значение csrf_token //
    var csrf = $('input[name="csrfmiddlewaretoken]').val();

    $('#is_like').click(function(){
        $('#is_like').attr('class', 'btn btn-light'));

        $.ajax({
        // Получаем url из атрибута data-url тега button //
            url: $('#is_like').attr('data-url'),
            type: 'post',
            data: {
            // Получаем email другого участника из атрибута id тега h1//
                other_client_email: $('h1').attr('id'),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                console.log($('#is_like').attr('class')));

            }
        });
    });
});
