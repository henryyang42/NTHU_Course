// Our class will live in the NTHUCourse global namespace.
if (window.NTHUCourse == undefined) window.NTHUCourse = {};

// Fix #25: Prevent accidental inclusion of autocomplete_light/static.html
if (window.NTHUCourse.Autocomplete != undefined)
  console.log('WARNING ! You are loading autocomplete.js **again**.');

NTHUCourse.getInternetExplorerVersion = function()
  // Returns the version of Internet Explorer or a -1
  // (indicating the use of another browser).
  {
    var rv = -1; // Return value assumes failure.
    if (navigator.appName == 'Microsoft Internet Explorer') {
      var ua = navigator.userAgent;
      var re = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
      if (re.exec(ua) != null)
        rv = parseFloat(RegExp.$1);
    }
    return rv;
  }

$.fn.NTHUCourseRegistry = function(key, value) {
  var ie = NTHUCourse.getInternetExplorerVersion();

  if (ie == -1 || ie > 8) {
    // If not on IE8 and friends, that's all we need to do.
    return value === undefined ? this.data(key) : this.data(key, value);
  }

  if ($.fn.NTHUCourseRegistry.data == undefined) {
    $.fn.NTHUCourseRegistry.data = {};
  }

  if ($.fn.NTHUCourseRegistry.guid == undefined) {
    $.fn.NTHUCourseRegistry.guid = function() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(
        /[xy]/g,
        function(c) {
          var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
          return v.toString(16);
        }
      );
    }
  }

  var attributeName = 'data-NTHUCourse-' + key + '-registry-id';
  var id = this.attr(attributeName);

  if (id == undefined) {
    id = $.fn.NTHUCourseRegistry.guid();
    this.attr(attributeName, id);
  }

  if (value != undefined) {
    $.fn.NTHUCourseRegistry.data[id] = value;
  }

  return $.fn.NTHUCourseRegistry.data[id];
}

/*
The autocomplete class constructor:

- takes a takes a text input element as argument,
- sets attributes and methods for this instance.

The reason you want to learn about all this script is that you will then be
able to override any variable or function in it on a case-per-case basis.
However, overriding is the job of the jQuery plugin so the procedure is
described there.
*/

var scope;

NTHUCourse.Autocomplete = function(input) {
  /*
  The text input element that should have an autocomplete.
  */
  this.input = input;

  // The value of the input. It is kept as an attribute for optimisation
  // purposes.
  this.value = '';

  /*
  The server should have a URL that takes the input value, and responds
  with the list of choices as HTML. In most cases, an absolute URL is
  better.
   */
  this.url = false;

  /*
  Although this script will make sure that it doesn't have multiple ajax
  requests at the time, it also supports debouncing.

  Set a number of milliseconds here, it is the number of milliseconds that it
  will wait before querying the server. The higher it is, the less it will
  spam the server but the more the user will wait.
  */
  this.xhrWait = 200;

  /*
  The value of the input is passed to the server via a GET variable. This
  is the name of the variable.
   */
  this.queryVariable = 'q';

  /*
  This dict will also be passed to the server as GET variables.

  If this autocomplete depends on another user defined value, then the
  other user defined value should be set in this dict.

  Consider a country select and a city autocomplete. The city autocomplete
  should only fetch city choices that are in the selected country. To
  achieve this, update the data with the value of the country select:

      $('select[name=country]').change(function() {
          $('city[name=country]').NTHUCourseAutocomplete().data = {
              country: $(this).val(),
          }
      });
   */
  this.data = {};

  /*
  To avoid several requests to be pending at the same time, the current
  request is aborted before a new one is sent. This attribute will hold the
  current XMLHttpRequest.
   */
  this.xhr = false;

  /*
  fetch() keeps a copy of the data sent to the server in this attribute. This
  avoids double fetching the same autocomplete.
   */
  this.lastData = {};

  this.next_page = 1;
}

/*
Rather than directly setting up the autocomplete (DOM events etc ...) in
the constructor, setup is done in this method. This allows to:

- instanciate an Autocomplete,
- override attribute/methods of the instance,
- and *then* setup the instance.
 */
NTHUCourse.Autocomplete.prototype.initialize = function() {
  this.input
    .on('blur.autocomplete', $.proxy(this.inputBlur, this))
    .on('click.autocomplete', $.proxy(this.inputClick, this))
    .on('keypress.autocomplete', $.proxy(this.inputKeypress, this))
    .on('keyup.autocomplete', $.proxy(this.inputKeyup, this))
    .on('keydown.autocomplete', $.proxy(this.inputKeydown, this))

  this.data[this.queryVariable] = '';
}

// Unbind callbacks on input.
NTHUCourse.Autocomplete.prototype.destroy = function(input) {
  input
    .unbind('blur.autocomplete')
    .unbind('click.autocomplete')
    .unbind('keypress.autocomplete')
    .unbind('keyup.autocomplete')
    .unbind('keydown.autocomplete')
}

// Return the value to pass to this.queryVariable.
NTHUCourse.Autocomplete.prototype.getQuery = function() {
  // Return the input's value by default.
  return this.input.val();
}

NTHUCourse.Autocomplete.prototype.inputKeyup = function(e) {
  if (!this.input.is(':visible'))
  // Don't handle keypresses on hidden inputs (ie. with limited choices)
    return;

  switch (e.keyCode) {
    case 40: // down arrow
    case 38: // up arrow
    case 16: // shift
    case 17: // ctrl
    case 18: // alt
      break

    case 9: // tab
    case 13: // enter
      if (!this.box.is(':visible')) return

      var choice = this.box.find('.' + this.hilightClass);

      if (!choice.length) {
        // Don't get in the way, let the browser submit form or focus
        // on next element.
        return;
      }

      e.preventDefault();
      e.stopPropagation();
      break

    default:
      this.refresh()
  }
}

NTHUCourse.Autocomplete.prototype.inputKeydown = function(e) {
  // Don't handle keypresses on hidden inputs (ie. with limited choices)
  if (!this.input.is(':visible')) return;

  // Avoid double call to move().
  this.suppressKeyPressRepeat = ~$.inArray(e.keyCode, [40, 38, 9, 13, 27])

}

// This function is in charge of keyboard usage.
NTHUCourse.Autocomplete.prototype.inputKeypress = function(e) {
  // Don't handle keypresses on hidden inputs (ie. with limited choices)
  if (!this.input.is(':visible')) return;

  // Return if it already handled by inputKeydown.
  if (this.suppressKeyPressRepeat) return;

}

// This function is in charge of angularjs model change.
NTHUCourse.Autocomplete.prototype.refreshScope = function(e) {
  this.next_page = e.next;
  scope.query = e.courses;
  scope.total_result = e.total;
  scope.$apply();
}

// Proxy fetch(), with some sanity checks.
NTHUCourse.Autocomplete.prototype.refresh = function() {
  // Set the new current value.
  this.value = this.getQuery();
  this.next_page = 1;

  if (this.value.length == 0) {
    this.refreshScope([]);
  }
  else if (this.value.length > 1) {
    this.fetch();
  }
}

// Manage requests to this.url.
NTHUCourse.Autocomplete.prototype.fetch = function() {
  // Add the current value to the data dict.
  this.data[this.queryVariable] = this.value;
  this.data['next_page'] = this.next_page;

  this.lastData = {};
  for (var key in this.data) {
    this.lastData[key] = this.data[key];
  }

  console.log(this.data);
  // Abort any current request.
  if (this.xhr) this.xhr.abort();

  // Abort any request that we planned to make.
  if (this.timeoutId) clearTimeout(this.timeoutId);

  // Make an asynchronous GET request to this.url in this.xhrWait ms
  this.timeoutId = setTimeout($.proxy(this.makeXhr, this), this.xhrWait);
}

// Wrapped ajax call to use with setTimeout in fetch().
NTHUCourse.Autocomplete.prototype.makeXhr = function() {
  this.input.addClass('xhr-pending');

  this.xhr = $.ajax(this.url, {
    type: "GET",
    data: this.data,
    complete: $.proxy(this.fetchComplete, this)
  });
}

// Callback for the ajax response.
NTHUCourse.Autocomplete.prototype.fetchComplete = function(jqXHR, textStatus) {
  this.input.removeClass('xhr-pending');

  if (this.xhr == jqXHR) this.xhr = false;
  if (textStatus == 'abort') return;

  this.refreshScope(JSON.parse(jqXHR.responseText));

}

$.fn.NTHUCourseAutocomplete = function(overrides) {
  if (this.length < 1) {
    // avoid crashing when called on a non existing element
    return;
  }

  var overrides = overrides ? overrides : {};
  var autocomplete = this.NTHUCourseRegistry('autocomplete');

  if (overrides == 'destroy') {
    if (autocomplete) {
      autocomplete.destroy(this);
      this.removeData('autocomplete');
    }
    return
  }

  // Disable the browser's autocomplete features on that input.
  this.attr('autocomplete', 'off');

  // If no Autocomplete instance is defined for this id, make one.
  if (autocomplete == undefined) {
    // Instanciate Autocomplete.
    var autocomplete = new NTHUCourse.Autocomplete(this);

    // Extend the instance with data-autocomplete-* overrides
    for (var key in this.data()) {
      if (!key) continue;
      if (key.substr(0, 12) != 'autocomplete' || key == 'autocomplete')
        continue;
      var newKey = key.replace('autocomplete', '');
      var newKey = newKey.charAt(0).toLowerCase() + newKey.slice(1);
      autocomplete[newKey] = this.data(key);
    }

    // Extend the instance with overrides.
    autocomplete = $.extend(autocomplete, overrides);

    if (!autocomplete.url) {
      alert('Autocomplete needs a url !');
      return;
    }

    this.NTHUCourseRegistry('autocomplete', autocomplete);

    // All set, call initialize().
    autocomplete.initialize();
  }

  // Return the Autocomplete instance for this id from the registry.
  return autocomplete;
};

$(function() {
  scope = angular.element('[ng-controller=CourseCtrl]').scope();
  $('#courseSearch').NTHUCourseAutocomplete({
    url: '/search'
  });

  $('#moreCourses').click(function() {
    // $('#courseSearch').NTHUCourseAutocomplete().next_page += 1;
    $('#courseSearch').NTHUCourseAutocomplete().fetch();
  });
})
