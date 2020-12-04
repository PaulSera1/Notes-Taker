//lookup table - transforms default Django DateField into HTML view
parseDate = (oldDate) => {
    const months = {
        '01': 'Jan.',
        '02': 'Feb.',
        '03': 'Mar.',
        '04': 'Apr.',
        '05': 'May.',
        '06': 'Jun.',
        '07': 'Jul.',
        '08': 'Aug.',
        '09': 'Sep.',
        '10': 'Oct.',
        '11': 'Nov.',
        '12': 'Dec.'
    }
    let data = oldDate.split('-');
    let year = data[0];
    let day = data[2];
    month = months[data[1]];
    return month + ' ' + day + ', ' + year;
}

$(document).ready(() => {
    //server domain
    const DOMAIN = 'http://localhost:8000';
    var btn = $("#mod"); //display notes
    var cl = $(".close"); //close single note

    btn.click(function() { //check toggle status of note display, display notes accordingly
        if(!$('.co').length) {
            if(!$('#dne').length)
                $('#notelist').append('<p id="dne" style="color: red">you have no notes!</p>');
            else return
        }
        else if($('.co').css('display') == 'block') {
            btn.html('Reveal Notes');
            $('.co').fadeOut(500);
            $('#dne').remove();
        }
        else {
            btn.html('Hide Notes');
            $('.co').css('display', 'block');
            $('#dne').remove();
        }
    });

    cl.click(function() { //close current note
        $(this).parent().parent().css('display', "none");
        $('.co').each(function() { //change display button value if all are closed
            if($(this).css('display') == 'block') return false;
            btn.html('Reveal Notes');
        });
    })

    $(document).on('click', '.note-opener', function() {
        const element = '#' + this.id.split('-')[1];
        if($(element).length) {
            if($(element).css('display') == 'block')
                $(element).fadeOut(500);
            else
                $(element).css('display', 'block');
        }
        else return false;   
    });

    $(document).on('click', '.delete-button', function() { //ajax call to delete note from database and delete HTML
        if(!confirm('Are you sure you want to delete this note? (this cannot be undone)'))
            return false;
        const noteId = this.id.split('-')[1];
        $.ajax({
            type: 'POST',
            url: DOMAIN + '/post/ajax/deletenote',
            data: {'note_id': noteId},
            success: function() {
                var openSelector = '#open-' + noteId;
                var noteSelector = '#' + noteId;
                $(openSelector).remove();
                $(noteSelector).remove();
            },
            error: function(response) {
                alert(response.JSON['responseJSON']['error']);
            }
        });
    })

    $('#noteform').submit(function(e) { //create new note HTML and record in database
        e.preventDefault();
        var serializedData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: DOMAIN + '/post/ajax/note',
            data: serializedData,
            success: function(response) {
                $('#noteform').trigger('reset');
                var instance = JSON.parse(response['instance']);
                var fields = instance[0]['fields'];
                const id = instance[0]['pk'];
                var date = fields.date_created;
                $('#notelist').append(
                    `<div id="${id}" class="co" style="display: block">
                        <div class="head">
                            <span class="close" onclick="$(this).parent().parent().css('display', 'none')">&times;</span>
                            <h2>${fields.title}</h2>
                            <p>by ${fields.author}</p>
                        </div>
                        <div class="body">
                            <p>${fields.body}</p>
                        </div>
                        <div class="footer">
                            <h3>${parseDate(date)}</h3>
                            <button class="delete-button" id="delete-${id}">Delete Permanently?</button>
                        </div>
                    </div>`
                );
                $('#notebar').append(
                    `<button class="note-opener" id="open-${id}">${fields.title}</button>`
                );
                $('#dne').remove();
            },
            error: function(response) {
                alert(response.JSON['responseJSON']['error']);
            }
        });
    });
});