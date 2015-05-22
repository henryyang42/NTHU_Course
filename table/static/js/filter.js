$(function() {
  var scope = angular.element('[ng-controller=CourseCtrl]').scope();
  var ge_option = function() {
    code = $('#id_code').val();
    $('#ge-option').hide();
    $('#gec-option').hide();
    if (code == 'GE' || code == 'GEC') {
      id = '#' + code.toLowerCase() + '-option';
      $(id).show();
    } else {
      $('#id_ge').val('');
      $('#id_gec').val('');
    }
  }
  $('#id_code').change(ge_option);
  ge_option();

  $("#search-filter").on("submit", function(event) {
    event.preventDefault();
    var url = '/search/?' + $(this).serialize();
    $.get(url, function(data) {
      scope.fetch = JSON.parse(data);
      scope.$apply();
    });
  });
})
