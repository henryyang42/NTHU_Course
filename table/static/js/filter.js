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

  $('#twocolbtn').on("click", function(event) {
    event.preventDefault();
    $('#main .container > div').toggleClass('col-lg-12 col-lg-6');
    $('#main .form-group label').toggleClass('col-lg-1 col-lg-2');
    $('#main .form-group div').toggleClass('col-lg-11 col-lg-10');
    $('#main .container').toggleClass("lg-container");
  });

  $("#search-filter").on("submit", function(event) {
    event.preventDefault();
    var url = '/search/?' + $(this).serialize() +
      '&page=' + 1 +
      '&size=' + scope.page_size +
      '&sort=' + scope.predicate +
      '&reverse=' + scope.reverse;
    $.get(url, function(result) {
      if (result == 'TMD') {
        toastr.warning('搜尋結果過多，請加強搜尋條件。');
        return;
      }
      scope.fetch = result;
      scope.currentPage = 1;
      scope.$apply();
      if (result.total == 0) {
        toastr.warning('查無結果！請嘗試其他關鍵字。');
        return;
      }
      $('#result-table').addClass(animation)
        .one(animationend, function(e) {
          $(this).removeClass(animation);
        });
    });
  });
})
