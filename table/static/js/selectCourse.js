var moduleNTHUCourse = angular.module("ModuleNTHUCourse", ['ui.bootstrap']);
var semester = '10320'
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

moduleNTHUCourse.controller("CourseCtrl", function($scope) {
    function init() {
        $scope.added_course = [];
        $scope.time_table = {};
        $scope.credit = 0;
        $scope.course_ct = 0;
        toastr.options.timeOut = 1500;
    }

    $scope.fetch = {};
    $scope.query = [];
    $scope.currentPage = 0;
    $scope.max_size = 5;
    $scope.total_result = 0;
    $scope.alerts = 1;
    $scope.page_size = 10;
    $scope.pageSizeModel = '10';

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

    // Init data
    init();
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

    $scope.closeAlert = function() {
        $scope.alerts = 0;
    };

    var search = function(page, size) {
        var url = '/search/?' + $('#search-filter').serialize() + '&page=' + page + '&size=' + size;
        $.get(url, function(data) {
            $scope.fetch = JSON.parse(data);
            $scope.$apply();
        });
    }

    $scope.pageChanged = function(page) {
        search(page, $scope.page_size);
    }

    $scope.setPageSize = function(size) {
        $scope.page_size = size;
        search('', size);
    }

    $scope.add = function(c) {
        if (c.added)
            return;
        timeTable(c, 'add');
        $scope.added_course.push(c);
        $scope.credit += c.credit;
        $scope.course_ct++;
        toastr.success(c.chi_title + ' 已成功加入您的課表。');
    }

    $scope.add_all = function(courses) {
        for (var i in courses) {
            $scope.add(courses[i]);
        }
        toastr.info('您真貪心。');
        delete $scope.fetch.type;
    }

    $scope.del = function(c) {
        timeTable(c, 'del');
        $scope.credit -= c.credit;
        $scope.course_ct--;
        del_course($scope.added_course, c);
        toastr.warning(c.chi_title + ' 已從您的課表移除。');
    }

    $scope.del_all = function() {
        init();
        toastr.info('已完全清空您的課表。');
    }

    $scope.free = function(c) {
        if (c.added)
            return true;
        return timeTable(c, 'free');
    }

    var updateChange = function() {
        setTimeout(function() {
            $('.ajax-popup-link').magnificPopup({
                type: 'ajax',
                closeOnContentClick: false
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

    var updateFetch = function() {
        $scope.query = $scope.fetch.courses;
        $scope.currentPage = $scope.fetch.page;
        $scope.total_result = $scope.fetch.total;
    }

    $scope.$watch('query', updateChange, true);
    $scope.$watch('added_course', updateChange, true);
    $scope.$watch('fetch', updateFetch, true);

})
