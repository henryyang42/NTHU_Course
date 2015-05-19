var moduleNTHUCourse = angular.module("ModuleNTHUCourse", ['ui.bootstrap']);

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
    var out = [], ids = [];
    for (var i in added_course)
      ids.push(added_course[i].id);

    for (var i in input) {
      if (ids.indexOf(input[i].id) < 0)
        out.push(input[i]);
    }
    return out;
  };
});

moduleNTHUCourse.controller("CourseCtrl", function($scope) {
  $scope.query = [];
  $scope.added_course = [];
  $scope.time_table = {};
  $scope.credit = 0;
  $scope.course_ct = 0;
  $scope.currentPage = 1;
  $scope.max_size = 5;

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
    for (i in time) {
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

  // Init data
  if (typeof(Storage) !== 'undefined') {
    // Code for localStorage
    var added_course = localStorage.getItem('added_course');
    if (added_course != null) {
      $scope.added_course = JSON.parse(added_course);
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

  $scope.pageChanged = function() {
    angular.element(document.querySelector('#courseSearch'))
        .NTHUCourseAutocomplete().fetch($scope.currentPage);
  };

  $scope.add = function(c) {
    timeTable(c, 'add');
    $scope.added_course.push(c);
    $scope.credit += c.credit;
    $scope.course_ct++;
    del_course($scope.query, c);
    // Increase hit
    $.get('/search/hit/'+c.id);
  }

  $scope.del = function(c) {
    timeTable(c, 'del');
    $scope.credit -= c.credit;
    $scope.course_ct--;
    del_course($scope.added_course, c);
  }

  $scope.free = function(c) {
    return timeTable(c, 'free');
  }

  $scope.ass = function(c) {
    console.log(c)
    return true;
  }

  var updateChange = function() {
    setTimeout(function() {
      $('.ajax-popup-link').magnificPopup({
        type: 'ajax'
      });
    }, 100);
    // Save data
    if (typeof(Storage) !== 'undefined') {
      // Code for localStorage
      localStorage.setItem('added_course', JSON.stringify($scope.added_course));
    } else {
      //Holy shit! No Web Storage support..
    }
  }
  $scope.$watch('query', updateChange, true);
  $scope.$watch('added_course', updateChange, true);
})
