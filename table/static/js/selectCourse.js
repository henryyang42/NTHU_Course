var moduleNTHUCourse = angular.module('ModuleNTHUCourse', ['ui.bootstrap']);
var semester = '10410';

moduleNTHUCourse.filter('courseInThatTime', function() {
  return function(input, time) {
    var out = [];
    for (var i in input) {
      if (input[i].time.indexOf(time) >= 0)
        out.push(input[i]);
    }
    return out;
  };
});

moduleNTHUCourse.filter('showQuery', function() {
  return function(input, added_course) {
    var ids = [];
    for (var i in added_course)
      ids.push(added_course[i].id);

    for (var i in input) {
      input[i].added = ids.indexOf(input[i].id) >= 0;
    }
    return input;
  };
});

moduleNTHUCourse.controller("CourseCtrl", function($scope, $filter) {
  $scope.fetch = {};
  $scope.query = [];
  $scope.currentPage = 0;
  $scope.max_size = 5;
  $scope.total_result = 0;
  $scope.alerts = 1;
  $scope.page_size = 10;
  $scope.pageSizeModel = '10';
  $scope.predicate = 'no';
  $scope.reverse = false;

  function init() {
    $scope.added_course = [];
    $scope.time_table = {};
    $scope.credit = 0;
    $scope.course_ct = 0;
    $scope.addAll_clicked = false;
  }

  function del_course(arr, c) {
    for (var i in arr) {
      // Remove course from array
      if (c.no == arr[i].no) {
        arr.splice(i, 1);
      }
    }
  }

  function timeTable(c, type) {
    var time = c.time.match(/.{1,2}/g);
    var table = $scope.time_table;
    for (var i in time) {
      if (type == 'add') {
        if (!table[time[i]])
          table[time[i]] = 0;
        table[time[i]]++;
      } else if (type == 'del') {
        table[time[i]]--;
        if (!table[time[i]])
          delete table[time[i]];
      } else if (type == 'free') {
        if (table[time[i]])
          return false;
      }
    }
    return true;
  }

  function load_localStorage() {
    if (typeof(Storage) !== 'undefined') {
      // Code for localStorage
      try {
        var added_course = localStorage.getItem('added_course');
        if (added_course != null) {
          added_course = JSON.parse(added_course);
          for (var i in added_course) {
            c = added_course[i];
            if (c.no.indexOf(semester) >= 0) {
              $scope.added_course.push(c);
            }
          }
        }
      } catch (e) {
        localStorage.setItem('added_course', JSON.stringify($scope.added_course));
      }
    } else {
      //Holy shit! No Web Storage support..
    }
  
    for (var i in $scope.added_course) {
      var c = $scope.added_course[i];
      $scope.credit += c.credit;
      $scope.course_ct++;
      timeTable(c, 'add');
    }
  }

  // Init data
  init();
  toastr.options.timeOut = 1500;

  $.get('/search/status/', function(remote_data) {
    if (remote_data.total > 0) {
      var local_data = JSON.parse(localStorage.getItem('added_course'));
      // merge remote data into local
      $.extend(local_data, remote_data.courses);
      localStorage.setItem('added_course', JSON.stringify(local_data));
    }
    load_localStorage();
    $scope.$apply();
  });

  $scope.closeAlert = function() {
    $scope.alerts = 0;
  };

  var search = function(page, size, sortby) {
    var url = '/search/?' + $('#search-filter').serialize() +
      '&page=' + page +
      '&size=' + size +
      '&sort=' + sortby +
      '&reverse=' + $scope.reverse;
    $.get(url, function(data) {
      $scope.fetch = data;
      $scope.$apply();
    });
  };

  $scope.scrollTo = function(element) {
    $('html, body').animate({
      scrollTop: $(element).offset().top
    }, 500);
  };

  $scope.order = function(predicate) {
    search($scope.currentPage, $scope.page_size, predicate);
  };

  $scope.pageChanged = function(page) {
    search(page, $scope.page_size, $scope.predicate);
    $scope.scrollTo('#result-table');
  };

  $scope.setPageSize = function(size) {
    $scope.page_size = size;
    search($scope.currentPage, size, $scope.predicate);
  };

  $scope.add = function(c) {
    if (c.added)
      return;
    timeTable(c, 'add');
    $scope.added_course.push(c);
    $scope.credit += c.credit;
    $scope.course_ct++;
    toastr.success(c.chi_title + ' 已成功加入您的課表。');
    $.get('/search/course/' + c.id + '/', {'type': 'PUT'});
  };

  $scope.add_all = function(courses) {
    for (var i in courses) {
      $scope.add(courses[i]);
    }
    toastr.info('您真貪心。');
  };

  $scope.del = function(c) {
    timeTable(c, 'del');
    $scope.credit -= c.credit;
    $scope.course_ct--;
    del_course($scope.added_course, c);
    toastr.warning(c.chi_title + ' 已從您的課表移除。');
    $.get('/search/course/' + c.id + '/', {'type': 'DELETE'});
  };

  $scope.del_all = function() {
    for (var i in $scope.added_course) {
      var c = $scope.added_course[i];
      $.get('/search/course/' + c.id + '/', {'type': 'DELETE'});
    }
    init();
    toastr.info('已完全清空您的課表。');
  };

  $scope.free = function(c) {
    if (c.added)
      return true;
    return timeTable(c, 'free');
  };

  var updateChange = function() {
    setTimeout(function() {
      $('.ajax-popup-link').magnificPopup({
        type: 'ajax',
        closeOnContentClick: false
      });
      $('[data-toggle="tooltip"]').tooltip();
      $(document).tooltip({
        track: true
      });
      $('#id_q').attr('title', '中英文課程名稱或簡稱(普物) / 老師名稱' +
                      '/ 課程時間(M1M2) / 學號查詢必選修 / 留空查詢該類課程');
      $('#id_q').tooltip({
        track: false,
        position: {
          my: 'left bottom',
          at: 'left top-5'
        }
      });
    }, 100);
    // Save data
    if (typeof(Storage) !== 'undefined') {
      // Code for localStorage
      localStorage.setItem('added_course', JSON.stringify($scope.added_course));
    } else {
      //Holy shit! No Web Storage support..
    }
  };

  var updateFetch = function() {
    $scope.query = $scope.fetch.courses;
    $scope.total_result = $scope.fetch.total;
  };

  $scope.$watch('query', updateChange, true);
  $scope.$watch('added_course', updateChange, true);
  $scope.$watch('fetch', updateFetch, true);

});
