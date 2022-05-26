$(document).ready(function(){
    // Получаем значение csrf_token //
    var csrf = $('input[name="csrfmiddlewaretoken').val();

    $(".btn").click(function(){
        $.ajax({
        // Получаем url из атрибута data-url тега button //
            url: $('button').attr('data-url'),
            type: 'post',
            data: {
            // Получаем emaail другого участника из атрибута id тега h1//
                other_client_email: $('h1').attr('id'),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                $(".btn").attr('class')
            }
        });
    });
});
