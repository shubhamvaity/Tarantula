if (annyang && anim != 1) {
  // Add our commands to annyang
  annyang.addCommands({
    ':term': function(term) { //alert('Searching for '+term);
    $("input[name=term]").val($("input[name=term]").val() + ' ' +term); }
  });

  // Tell KITT to use annyang
  SpeechKITT.annyang();

  // Define a stylesheet for KITT to use
  SpeechKITT.setStylesheet('/static/css/SpeechKITT.css');

  // Render KITT's interface
  SpeechKITT.vroom();

}

