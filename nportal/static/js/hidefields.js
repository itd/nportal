/**
 * Created by kbendl on 10/16/15.
   hidefields.js

   Show/Hides some fields on the reg form if a user has an nrel account
    based on a radio button click.
 */


$(document).ready(function(){

  $("input[name$='isnreluser']").click(function() {
    if($(this).val() === 'existing') {
      $("fieldset#existing-account").hide();
      $("fieldset#new-account").show();
    }
    if($(this).val() === 'new') {
      $("fieldset#existing-account").show();
      $("fieldset#new-account").hide();
    }
  });

});

//$(document).ready(function (){
//  validate();
//  $('#preferredUID', '#nrelUserID').change(validate);
//});
//
//function validate(){
//  if ($('#preferredUID').val().length   >   0   ||
//      $('#nrelUserID').val().length  >   0 ) {
//      $("input[type=submit]").prop("disabled", false);
//  }
//  else {
//      $("input[type=submit]").prop("disabled", true);
//  }
//}


