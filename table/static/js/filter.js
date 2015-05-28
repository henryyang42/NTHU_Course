$(function() {
  var scope = angular.element('[ng-controller=CourseCtrl]').scope();
  var animation = 'animated bounceInLeft',
      animationend = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
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
      var result = JSON.parse(data);
      scope.fetch = result;
      scope.$apply();
      if (result.total == 0) {
        toastr.info('查無結果！請嘗試其他關鍵字。');
      }
      $('#result-table').addClass(animation)
        .one(animationend, function(e) {
          $(this).removeClass(animation);
        });
    });
  });
})
