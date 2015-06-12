$(function() {

  // remove facebook disgusting hash on login redirect url
  if (window.location.hash && window.location.hash == '#_=_')
    window.location.hash = '';

  var scope = angular.element('[ng-controller=CourseCtrl]').scope();
  var animation = 'animated bounceInLeft',
    animationend = 'webkitAnimationEnd mozAnimationEnd ' +
                   'MSAnimationEnd oanimationend animationend';
  var course_code_option = function() {
    $('#id_ge').val('');
    $('#id_gec').val('');
    $('#id_dept_required').val('');
    code = $('#id_code').val();
    // 4 digit code for dept-required-option
    code_4 = code;
    while (code_4.length < 4)
      code_4 += ' ';
    $('#ge-option').hide();
    $('#gec-option').hide();
    $('#dept-required-option').hide();
    if (code == 'GE' || code == 'GEC') {
      id = '#' + code.toLowerCase() + '-option';
      $(id).show();
    } else if ($('#id_dept_required  option[value^="' + code_4 + '"]').length) {
      $('#dept-required-option').show();
      $('#id_dept_required  option').hide();
      $('#id_dept_required  option[value^="' + code_4 + '"]').show();
      $('#id_dept_required  option[value=""]').show();
    }
  };
  $('#id_code').change(course_code_option);
  course_code_option();

  var CLASS_NAME_MAP = {
    '0': 'B',
    '1': 'BA',
    '2': 'BB',
    '3': 'BC',
    '5': 'M',
    '6': 'M',
    '7': 'M',
    '8': 'D',
    '9': 'D'
  };

  var DEPT_MAP = {
    '000': 'ST',
    '001': 'SLS',
    '002': 'ILS',
    '010': 'IPNS',
    '011': 'ESS',
    '012': 'BMES',
    '013': 'NES',
    '020': 'SCI',
    '021': 'MATH',
    '022': 'PHYS',
    '023': 'CHEM',
    '024': 'STAT',
    '025': 'ASTR',
    '030': 'IPE',
    '031': 'MS',
    '032': 'CHE',
    '033': 'PME',
    '034': 'IEEM',
    '035': 'NEMS',
    '036': 'IEM',
    '037': 'OET',
    '038': 'BME',
    '041': 'CL',
    '042': 'FL',
    '043': 'HIS',
    '044': 'LING',
    '045': 'SOC',
    '046': 'ANTH',
    '047': 'PHIL',
    '048': 'HSS',
    '049': 'TL',
    '141': 'GPTS',
    '142': 'IACS',
    '060': 'EECS',
    '061': 'EE',
    '062': 'CS',
    '063': 'ENE',
    '064': 'COM',
    '065': 'ISA',
    '066': 'IPT',
    '067': 'RDIC',
    '068': 'RDDM',
    '069': 'RDPE',
    '161': 'UPPP',
    '162': 'SNHC',
    '070': 'UPMT',
    '071': 'QF',
    '072': 'ECON',
    '073': 'TM',
    '074': 'LST',
    '075': 'EMBA',
    '076': 'MBA',
    '077': 'IMBA',
    '078': 'ISS',
    '080': 'LSIP',
    '081': 'LS',
    '082': 'DMS',
    '083': 'LSIN'
  };

  $('input[name=q]').keyup(function() {
    var input_str = $(this).val();
    var SENIOR = 101;
    if (isNaN(input_str) === false) {
      if (input_str.length < 8)
        return;
      if (input_str.length == 8) {
        input_str = '0' + input_str;
      }
      var year = input_str.substr(0, 3);
      if (parseInt(year, 10) < SENIOR) {
        year = SENIOR;
      }
      dept = input_str.substr(3, 3);
      class_name = input_str.substr(6, 1);
      if (DEPT_MAP[dept] !== undefined &&
        CLASS_NAME_MAP[class_name] !== undefined) {
        dept = DEPT_MAP[dept];
        class_name = CLASS_NAME_MAP[class_name];

        while (dept.length < 4)
          dept = dept + ' ';
        $('#dept-required-option').show();
        $('#id_dept_required  option').hide();
        $('#id_dept_required  option[value^="' + dept + '"]').show();
        $('#id_dept_required  option[value=""]').show();
        $('#id_dept_required  option:selected').removeAttr('selected');
        $('#id_code').val(dept.trim());
        $('#id_dept_required').val(dept + year + class_name);
      }
    }
  });

  $('#twocolbtn').on('click', function(event) {
    event.preventDefault();
    $('#main .container > div').toggleClass('col-lg-12 col-lg-6');
    $('#main .form-group label').toggleClass('col-lg-1 col-lg-2');
    $('#main .form-group div').toggleClass('col-lg-11 col-lg-10');
    $('#main .container').toggleClass('lg-container');
  });

  $('#reset-filter').on('click', function(event) {
    $('#ge-option').hide();
    $('#gec-option').hide();
    $('#dept-required-option').hide();
  });

  $('#search-filter').on('submit', function(event) {
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
});
