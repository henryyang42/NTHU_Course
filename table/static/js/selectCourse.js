var moduleNTHUCourse = angular.module("ModuleNTHUCourse", []);

moduleNTHUCourse.controller("CourseCtrl", function($scope) {
  $scope.query = [];
  $scope.added_course = [];
  $scope.time_table = {};
  $scope.credit = 0;
  $scope.course_ct = 0;

  function del_course(arr, c) {
    for (var i in arr) {
      // Remove course from array
      if (c.no == arr[i].no) {
        arr.splice(i, 1);
      }
    }
  }

  function p(c, type) {
    time = c.time.match(/.{1,2}/g);
    for (i in time) {
      if (type == 'add')
        $scope.time_table[time[i]] = 1;
      else if (type == 'del')
        delete $scope.time_table[time[i]];
      else if (type == 'free') {
        if ($scope.time_table[time[i]])
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
    p(c, 'add');
  }

  $scope.add = function(c) {
    var course = jQuery.extend(true, {}, c);
    $scope.added_course.push(course);
    $scope.credit += c.credit;
    $scope.course_ct++;
    del_course($scope.query, c);
  }

  $scope.del = function(c) {
    p(c, 'del');
    $scope.credit -= c.credit;
    $scope.course_ct--;
    del_course($scope.added_course, c);
  }

  $scope.free = function(c) {
    return p(c, 'free');
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
