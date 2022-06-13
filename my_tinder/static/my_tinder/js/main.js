$(document).ready(function(){
    // Получаем значение csrf_token //
    var csrf = $('input[name=csrfmiddlewaretoken]').val();
    var btn = $('button:contains("равится")');
    var like_btn = $('button:contains("Нравится")')
    var unlike_btn = $('button:contains("Не нравится")')


    function sendAjax(method='post', btnType){
          $.ajax({
        // Получаем url из атрибута data-url тега button //
            url: $('button:contains("равится")').attr('data-url'),
            type: method,
            data: {
            // Получаем email другого участника из атрибута id тега h1//
                other_client_email: $('h1').attr('id'),
                csrfmiddlewaretoken: csrf,
                btnType: btnType
            },
            success: function(response) {
                console.log($(response.request));}
        });
    }
        /*$('button').click(function(){
            if $('button:')
            if (button.text() ==='Нравится'){
                $(button).attr('class', 'btn btn-primary')
                $('button').text('Не нравится').attr('class', 'btn btn-light')
                }
            else if (button.text('Не нравится')){
                $(this).attr('class', 'btn btn-primary')
                $('button').text('Нравится').attr('class', 'btn btn-light')

             }
            }*/


        /*$(btn).click(function(){
            if (btn.text() === 'Нравится'){
                $(btn).attr('class', 'btn btn-primary');
                $('button:contains("Не нравится")'.attr('class', 'btn btn-light'));
                }*/

        $(unlike_btn).click(function(){
            $(unlike_btn).attr('class', 'btn btn-success');
            $(like_btn).attr('class', 'btn btn-light');
            sendAjax(unlike_btn)})


        $(like_btn).click(function(){
            $(unlike_btn).attr('class', 'btn btn-light');
            $(like_btn).attr('class', 'btn btn-success');
            sendAjax(like_btn)



    });
});
