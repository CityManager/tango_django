$(document).ready(function(){
    // jQuery code to be added in here.
    $("#about-btn").click(
        function(event){
            alert('You clicked the button using JQuery!');
            msg_str = $("#msg").html();
            msg_str = msg_str + "o";
            $("#msg").html(msg_str);
        }
    );

    $(".ouch").click(
        function(event){
            alert('You clicked me! ouch!');
        }
    );

    $("p").hover(
        function(){
            $(this).css('color', 'red');
        },
        function(){
            $(this).css('color', 'blue');
        }
    );

    $("#about-btn").addClass('btn btn-primary');

    $('#addPageModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var recipient = button.data('whatever'); // Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this);
        modal.find('.modal-title').text('New Page Link to ' + recipient)
        // modal.find('.modal-body input').val(recipient)
    });

});