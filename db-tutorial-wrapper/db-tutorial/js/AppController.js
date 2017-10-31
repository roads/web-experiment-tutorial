/* AppController.js
*
* Author: BD Roads
*
* Controller for website tutorial
*
*/

var AppController = function(cfg) {

    // Global variables
    var trialStartTimeMs;
    var trialEndTimeMs;
    var experimentState = {
        completedScreenCounter : 0
    }
    var letterSequence = Generate_Letter_Sequence(cfg.nTrial);

    Start_New_Trial(experimentState);

    function Generate_Letter_Sequence(nTrial) {
        // Generate a random sequence of A's and B's to show during the
        // experiment.
        var letterSequence = [];
        for (var iTrial=0; iTrial<nTrial; iTrial++) {
            if (Math.random() < .5) {
                letterSequence.push('A');
            } else {
                letterSequence.push('B');
            }
        }
        Console_Debug(cfg.debugOn, 'Generated letter sequence for trials.')
        return letterSequence;
    }

    function Start_New_Trial(experimentState) {
        trialStartTimeMs = new Date().getTime();
        if (experimentState.completedScreenCounter >= cfg.nTrial) {
            // The experimet is done, conclude the experiment.
            $(".trial-content").slideUp();
            $(".end-content").slideDown();
            Console_Debug(cfg.debugOn, 'All trials completed.')

            // BEGIN NEW CODE
            // Update the assignment status.
            var status = 'completed';
            Post_Assignment_Update(status);
            // END NEW CODE
        } else {
            // The experiment is not done, display next stimulus.
            $('#trial-content__stimulus').text(letterSequence[experimentState.completedScreenCounter])
            Console_Debug(cfg.debugOn, 'Started new trial.')
        }
    }

    function Grade_Response(submittedResponse) {
        var isCorrect = 0;
        if (submittedResponse === letterSequence[experimentState.completedScreenCounter]) {
            // Correct response
            Flash_Background_Correct();
            isCorrect = 1;
        } else {
            // Incorrect response
            Flash_Background_Incorrect();
        }
        return isCorrect;
    }

    function Flash_Background_Correct() {
        // Note: jquery-ui necessary to animate colors.
        $('body').stop().animate({backgroundColor:'#006622'}, 10);
        $('body').animate({backgroundColor:'#333333'}, 1000);
    }

    function Flash_Background_Incorrect() {
        // Note: jquery-ui necessary to animate colors.
        $('body').stop().animate({backgroundColor:'#800000'}, 10);
        $('body').animate({backgroundColor:'#333333'}, 1000);
    }

    // BEGIN NEW CODE
    function Post_Trial(trialCount, queryLetter, submittedLetter) {
        if (cfg.doRecord) {
            var dataToPost = {
                website: cfg.website,
                assignmentId: cfg.dbAssignmentId,
                trialCount: trialCount,
                queryLetter: queryLetter,
                submittedLetter: submittedLetter,
                startTimeMs: String(trialStartTimeMs),
                endTimeMs: String(trialEndTimeMs)
            };

            $.post("php/post-trial.php", dataToPost, function( data ) {
                Console_Debug(cfg.debugOn, data);
            }).fail( function () {
                Console_Debug(cfg.debugOn, "Failed to create display and/or triplet entries in database.");
            });
        } // end if
    }
    // END NEW CODE

    // BEGIN NEW CODE
    function Post_Assignment_Update(status) {
        if (cfg.doRecord) {
            var dataToPost = {
                website: cfg.website,
                assignmentId: cfg.dbAssignmentId,
                endHit: String(new Date().getTime()),
                status: status
            };

            $.post("php/update-assignment.php", dataToPost, function( data ) {
                Console_Debug(cfg.debugOn, data);
            }).fail( function () {
                Console_Debug(cfg.debugOn, "Failed to update assignment entry in database.");
            });
        } // end if
    }
    // END NEW CODE

    $(".trial-content__submit-button").click( function() {
        // Grab the submission data.
        trialEndTimeMs = new Date().getTime();
        var submittedResponse = $(this).data("submit-button");
        var queryLetter = letterSequence[experimentState.completedScreenCounter];
        Console_Debug(cfg.debugOn, 'Response submitted.')

        // Evaluate the participant's response.
        var isCorrect = Grade_Response(submittedResponse)

        // BEGIN NEW CODE
        // Post the completed trial.
        Post_Trial(experimentState.completedScreenCounter, queryLetter, submittedResponse);
        // END NEW CODE

        // Start the next trial.
        experimentState.completedScreenCounter += 1;
        $("#trial-content__progress-counter").text(experimentState.completedScreenCounter)
        Start_New_Trial(experimentState);
    });

    $("#next-button").click( function() {
        // Hide instructions and show the first trial.
        $(".begin-content").slideUp();
        $(".trial-content").slideDown();
    });

}
