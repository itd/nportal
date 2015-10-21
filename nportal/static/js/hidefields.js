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

/*
  $("fieldset#existing-account").hide();
  $("fieldset#new-account").hide();
  var sel = $('input[name$="isnreluser"]').val();
  if (sel === 'existing') {
    $("fieldset#existing-account").show();
    $("fieldset#new-account").hide();
  } else if  (sel === 'new') {
    $("fieldset#existing-account").hide();
    $("fieldset#new-account").show();
  } else {
    $("fieldset#new-account").hide();
    $("fieldset#existing-account").hide();
  }*/

// end document ready
});
