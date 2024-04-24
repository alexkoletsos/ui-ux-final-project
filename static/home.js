function next_question() {

    if (!$('input[name="response"]:checked').length) {
        alert('Please select a response.');
        return;
    }
    
    var selectedResponse = $('input[name="response"]:checked').val();

    console.log('Selected response:', selectedResponse);

    var currentId = window.location.pathname.split('/').pop();
        
    $.ajax({
        url: '/store_response',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ question_id: currentId, response: selectedResponse }),
        success: function(data) {

            console.log('Updated quiz_ans:', data.quiz_ans);

            var nextId = parseInt(currentId) + 1;
            var nextPageUrl = '/quiz/' + nextId;
            window.location.href = nextPageUrl;
        
        },
        error: function(xhr, status, error) {
            console.error('Error storing response: ' + error);
        }
    });
}

function makeClickable(element) {
    element.style.cursor = "pointer";
}


function submit_q(answers) {

    var currentId = window.location.pathname.split('/').pop();

    $.ajax({
        url: '/submit_quiz', // Replace with the actual endpoint to save quiz answers
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ question_id: currentId, response: answers }),
        success: function(response) {
            // Handle success response from the server
            console.log('Quiz answers saved successfully:', response);
            // Redirect the user to the next page or perform any other action
            window.location.href = '/quiz_results';
        },
        error: function(xhr, status, error) {
            console.error('Error saving quiz answers:', error);
        }
    });
}

function submit_quiz() {

    $(".err").remove();

    var one = $("#1").val();
    var two = $("#2").val();
    var three = $("#3").val();


    if (one.trim() == "" && two.trim() == "" && three.trim() == ""){
        $("#1").after("<div class='err'>*Field empty!</div>");
        $("#2").after("<div class='err'>*Field empty!</div>");
        $("#3").after("<div class='err'>*Field empty!</div>");

        $("#1").focus();

    } else if(two.trim() == "" && three.trim() == ""){

        $("#2").after("<div class='err'>*Field empty!</div>");
        $("#3").after("<div class='err'>*Field empty!</div>");

        $("#2").focus();

    } else if (one.trim() == "") {

        $("#1").after("<div class='err'>*Field empty!</div>");

        $("#1").focus();

    } else if (two.trim() == "") {

        $("#2").after("<div class='err'>*Field empty!</div>");

        $("#2").focus();

    } else if (three.trim() == "") {

        $("#3").after("<div class='err'>*Field empty!</div>");

        $("#3").focus();

    } else {

        var confirmation = confirm("Are you sure you want to submit the quiz?");
        if (confirmation) {

            var lastq_ans = {
                "1": one,
                "2": two,
                "3": three
            };
            submit_q(lastq_ans);

        }

    }

}

$(document).ready(function() {
    $('#next-question').click(function() {
        next_question();
    });
    $('#submit-quiz').click(function() {
        submit_quiz();
    });
});