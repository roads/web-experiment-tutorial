/* AppController.js
*
* Author: BD Roads
*
* Controller for database tutorial
*
*/

var AppController = function(cfg) {

    // Global variables
    var startTimeMs;
    var endTimeMs;
    var experimentState = {};

    // Experiment state does not exist yet, initialize
    var experimentState = {
        completedScreenCounter : 0
    }
    Start_New_Trial(experimentState);

    function Start_New_Trial(experimentState) {
        startTimeMs = new Date().getTime();
        if (experimentState.completedScreenCounter >= cfg.nScreen) {
            // Experimet done
            //Disable button
            $('#grid__submit-button').removeClass('custom-button_enabled');
            $('#grid__submit-button').addClass('custom-button_disabled');
            $('#grid__submit-button').addClass('unselectable')
            // Update status
            Post_Assignment_Update();
        }
    }

    function Post_Trial(trialCount) {
        if (cfg.doRecord) {
            var dataToPost = {
                website: cfg.website,
                assignmentId: cfg.dbAssignmentId,
                trialCount: trialCount,
                startTimeMs: String(startTimeMs),
                endTimeMs: String(endTimeMs)
            };

            $.post("php/post-trial.php", dataToPost, function( data ) {
                Console_Debug(cfg.debugOn, data);
            }).fail( function () {
                Console_Debug(cfg.debugOn, "Failed to create display and/or triplet entries in database.");
            });
        } // end if
    }

    function Post_Assignment_Update() {
        if (cfg.doRecord) {
            status = 'completed'
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

    $("#grid__submit-button").click( function() {
        if ($("#grid__submit-button").hasClass("custom-button_enabled")) {
            // Post completed trial
            endTimeMs = new Date().getTime();
            experimentState.completedScreenCounter += 1;
            $("#grid__progress-counter").text(experimentState.completedScreenCounter)
            Post_Trial(experimentState.completedScreenCounter);
            // Start next trial
            Start_New_Trial(experimentState);
        }
    });

}
