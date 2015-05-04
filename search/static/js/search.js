$(function() {
  $('#courseSearch').yourlabsAutocomplete({
    url: '/search'
  }).input.bind('selectChoice', function(e, choice, autocomplete) {
    // When a choice is selected, open it.
    window.location.href = choice.attr('href');
  });
})
