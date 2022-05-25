$(document).ready(function(){

    $("z").mouseover(function(){
        $.ajax({
            url: $('form').attr('action'),
            type: 'get',
            data: {
                button_text: $(this).attr('value')
            },
            success: function(button_text){
                alert('Congrats!' + button_text)
                console.log(button_text)
            }
        });
    });



    /*$('#id_like').mouseover(function(){
        //let attr_name = $('html body div.container.mt-5 div.row div.col-7.offset-md-3 h1').text()
        let form_attr_action = $('form').attr('action')
        //alert(attr_name)
        alert(form_attr_action)
    });*/
});
