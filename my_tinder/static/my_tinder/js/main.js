$(document).ready(function(){
    // Получаем значение csrf_token //
    var csrf = $('input[name=csrfmiddlewaretoken]').val();
    /* var btn = $('button:contains("равится")');
    var like_btn = $('button:contains("Нравится")')
    var unlike_btn = $('button:contains("Не нравится")')*/

        $('button:contains("Нравится")').click(function(){
          $.ajax({
        // Получаем url из атрибута data-url тега button //
            url: $('button:contains("Нравится")').attr('data-url'),
            type: 'post',
            data: {
            // Получаем email другого участника из атрибута id тега h1 //
                other_client_email: $('h1').attr('id'),
                csrfmiddlewaretoken: csrf,
                button: $('button:contains("Нравится")').text()
            },
            success: function(response) {
                console.log($(response.request));}
        });



    });
});
