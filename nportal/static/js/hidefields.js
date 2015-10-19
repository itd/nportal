/**
 * Created by kbendl on 10/16/15.
   hidefields.js

   Show/Hides some fields on the reg form if a user has an nrel account
    based on a radio button click.
 */

$(document).ready(function(){
    $("input[name$='isnreluser']").click(function() {
      if($(this).val()=='0') {
        $("fieldset#existing-account").hide();
        $("fieldset#new-account").show();
      }
      if($(this).val()=='1') {
        $("fieldset#existing-account").show();
        $("fieldset#new-account").hide();
      }
    });
});