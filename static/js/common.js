/*!
 * Bootstrap v3.3.7 (http://getbootstrap.com)
 * Copyright 2011-2017 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 */

/*!
 * Generated using the Bootstrap Customizer (http://getbootstrap.com/customize/?id=77a092ae0bc2b25abd8a68c707be7e6a)
 * Config saved to config.json and https://gist.github.com/77a092ae0bc2b25abd8a68c707be7e6a
 */
if (typeof jQuery === 'undefined') {
  throw new Error('Bootstrap\'s JavaScript requires jQuery')
}
+function ($) {
  'use strict';
  var version = $.fn.jquery.split(' ')[0].split('.')
  if ((version[0] < 2 && version[1] < 9) || (version[0] == 1 && version[1] == 9 && version[2] < 1) || (version[0] > 3)) {
    throw new Error('Bootstrap\'s JavaScript requires jQuery version 1.9.1 or higher, but lower than version 4')
  }
}(jQuery);

/* ========================================================================
 * Bootstrap: alert.js v3.3.7
 * http://getbootstrap.com/javascript/#alerts
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // ALERT CLASS DEFINITION
  // ======================

  var dismiss = '[data-dismiss="alert"]'
  var Alert   = function (el) {
    $(el).on('click', dismiss, this.close)
  }

  Alert.VERSION = '3.3.7'

  Alert.TRANSITION_DURATION = 150

  Alert.prototype.close = function (e) {
    var $this    = $(this)
    var selector = $this.attr('data-target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
    }

    var $parent = $(selector === '#' ? [] : selector)

    if (e) e.preventDefault()

    if (!$parent.length) {
      $parent = $this.closest('.alert')
    }

    $parent.trigger(e = $.Event('close.bs.alert'))

    if (e.isDefaultPrevented()) return

    $parent.removeClass('in')

    function removeElement() {
      // detach from parent, fire event then clean up data
      $parent.detach().trigger('closed.bs.alert').remove()
    }

    $.support.transition && $parent.hasClass('fade') ?
      $parent
        .one('bsTransitionEnd', removeElement)
        .emulateTransitionEnd(Alert.TRANSITION_DURATION) :
      removeElement()
  }


  // ALERT PLUGIN DEFINITION
  // =======================

  function Plugin(option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.alert')

      if (!data) $this.data('bs.alert', (data = new Alert(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  var old = $.fn.alert

  $.fn.alert             = Plugin
  $.fn.alert.Constructor = Alert


  // ALERT NO CONFLICT
  // =================

  $.fn.alert.noConflict = function () {
    $.fn.alert = old
    return this
  }


  // ALERT DATA-API
  // ==============

  $(document).on('click.bs.alert.data-api', dismiss, Alert.prototype.close)

}(jQuery);

/* ========================================================================
 * Bootstrap: button.js v3.3.7
 * http://getbootstrap.com/javascript/#buttons
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // BUTTON PUBLIC CLASS DEFINITION
  // ==============================

  var Button = function (element, options) {
    this.$element  = $(element)
    this.options   = $.extend({}, Button.DEFAULTS, options)
    this.isLoading = false
  }

  Button.VERSION  = '3.3.7'

  Button.DEFAULTS = {
    loadingText: 'loading...'
  }

  Button.prototype.setState = function (state) {
    var d    = 'disabled'
    var $el  = this.$element
    var val  = $el.is('input') ? 'val' : 'html'
    var data = $el.data()

    state += 'Text'

    if (data.resetText == null) $el.data('resetText', $el[val]())

    // push to event loop to allow forms to submit
    setTimeout($.proxy(function () {
      $el[val](data[state] == null ? this.options[state] : data[state])

      if (state == 'loadingText') {
        this.isLoading = true
        $el.addClass(d).attr(d, d).prop(d, true)
      } else if (this.isLoading) {
        this.isLoading = false
        $el.removeClass(d).removeAttr(d).prop(d, false)
      }
    }, this), 0)
  }

  Button.prototype.toggle = function () {
    var changed = true
    var $parent = this.$element.closest('[data-toggle="buttons"]')

    if ($parent.length) {
      var $input = this.$element.find('input')
      if ($input.prop('type') == 'radio') {
        if ($input.prop('checked')) changed = false
        $parent.find('.active').removeClass('active')
        this.$element.addClass('active')
      } else if ($input.prop('type') == 'checkbox') {
        if (($input.prop('checked')) !== this.$element.hasClass('active')) changed = false
        this.$element.toggleClass('active')
      }
      $input.prop('checked', this.$element.hasClass('active'))
      if (changed) $input.trigger('change')
    } else {
      this.$element.attr('aria-pressed', !this.$element.hasClass('active'))
      this.$element.toggleClass('active')
    }
  }


  // BUTTON PLUGIN DEFINITION
  // ========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.button')
      var options = typeof option == 'object' && option

      if (!data) $this.data('bs.button', (data = new Button(this, options)))

      if (option == 'toggle') data.toggle()
      else if (option) data.setState(option)
    })
  }

  var old = $.fn.button

  $.fn.button             = Plugin
  $.fn.button.Constructor = Button


  // BUTTON NO CONFLICT
  // ==================

  $.fn.button.noConflict = function () {
    $.fn.button = old
    return this
  }


  // BUTTON DATA-API
  // ===============

  $(document)
    .on('click.bs.button.data-api', '[data-toggle^="button"]', function (e) {
      var $btn = $(e.target).closest('.btn')
      Plugin.call($btn, 'toggle')
      if (!($(e.target).is('input[type="radio"], input[type="checkbox"]'))) {
        // Prevent double click on radios, and the double selections (so cancellation) on checkboxes
        e.preventDefault()
        // The target component still receive the focus
        if ($btn.is('input,button')) $btn.trigger('focus')
        else $btn.find('input:visible,button:visible').first().trigger('focus')
      }
    })
    .on('focus.bs.button.data-api blur.bs.button.data-api', '[data-toggle^="button"]', function (e) {
      $(e.target).closest('.btn').toggleClass('focus', /^focus(in)?$/.test(e.type))
    })

}(jQuery);

/* ========================================================================
 * Bootstrap: dropdown.js v3.3.7
 * http://getbootstrap.com/javascript/#dropdowns
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // DROPDOWN CLASS DEFINITION
  // =========================

  var backdrop = '.dropdown-backdrop'
  var toggle   = '[data-toggle="dropdown"]'
  var Dropdown = function (element) {
    $(element).on('click.bs.dropdown', this.toggle)
  }

  Dropdown.VERSION = '3.3.7'

  function getParent($this) {
    var selector = $this.attr('data-target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && /#[A-Za-z]/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
    }

    var $parent = selector && $(selector)

    return $parent && $parent.length ? $parent : $this.parent()
  }

  function clearMenus(e) {
    if (e && e.which === 3) return
    $(backdrop).remove()
    $(toggle).each(function () {
      var $this         = $(this)
      var $parent       = getParent($this)
      var relatedTarget = { relatedTarget: this }

      if (!$parent.hasClass('open')) return

      if (e && e.type == 'click' && /input|textarea/i.test(e.target.tagName) && $.contains($parent[0], e.target)) return

      $parent.trigger(e = $.Event('hide.bs.dropdown', relatedTarget))

      if (e.isDefaultPrevented()) return

      $this.attr('aria-expanded', 'false')
      $parent.removeClass('open').trigger($.Event('hidden.bs.dropdown', relatedTarget))
    })
  }

  Dropdown.prototype.toggle = function (e) {
    var $this = $(this)

    if ($this.is('.disabled, :disabled')) return

    var $parent  = getParent($this)
    var isActive = $parent.hasClass('open')

    clearMenus()

    if (!isActive) {
      if ('ontouchstart' in document.documentElement && !$parent.closest('.navbar-nav').length) {
        // if mobile we use a backdrop because click events don't delegate
        $(document.createElement('div'))
          .addClass('dropdown-backdrop')
          .insertAfter($(this))
          .on('click', clearMenus)
      }

      var relatedTarget = { relatedTarget: this }
      $parent.trigger(e = $.Event('show.bs.dropdown', relatedTarget))

      if (e.isDefaultPrevented()) return

      $this
        .trigger('focus')
        .attr('aria-expanded', 'true')

      $parent
        .toggleClass('open')
        .trigger($.Event('shown.bs.dropdown', relatedTarget))
    }

    return false
  }

  Dropdown.prototype.keydown = function (e) {
    if (!/(38|40|27|32)/.test(e.which) || /input|textarea/i.test(e.target.tagName)) return

    var $this = $(this)

    e.preventDefault()
    e.stopPropagation()

    if ($this.is('.disabled, :disabled')) return

    var $parent  = getParent($this)
    var isActive = $parent.hasClass('open')

    if (!isActive && e.which != 27 || isActive && e.which == 27) {
      if (e.which == 27) $parent.find(toggle).trigger('focus')
      return $this.trigger('click')
    }

    var desc = ' li:not(.disabled):visible a'
    var $items = $parent.find('.dropdown-menu' + desc)

    if (!$items.length) return

    var index = $items.index(e.target)

    if (e.which == 38 && index > 0)                 index--         // up
    if (e.which == 40 && index < $items.length - 1) index++         // down
    if (!~index)                                    index = 0

    $items.eq(index).trigger('focus')
  }


  // DROPDOWN PLUGIN DEFINITION
  // ==========================

  function Plugin(option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.dropdown')

      if (!data) $this.data('bs.dropdown', (data = new Dropdown(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  var old = $.fn.dropdown

  $.fn.dropdown             = Plugin
  $.fn.dropdown.Constructor = Dropdown


  // DROPDOWN NO CONFLICT
  // ====================

  $.fn.dropdown.noConflict = function () {
    $.fn.dropdown = old
    return this
  }


  // APPLY TO STANDARD DROPDOWN ELEMENTS
  // ===================================

  $(document)
    .on('click.bs.dropdown.data-api', clearMenus)
    .on('click.bs.dropdown.data-api', '.dropdown form', function (e) { e.stopPropagation() })
    .on('click.bs.dropdown.data-api', toggle, Dropdown.prototype.toggle)
    .on('keydown.bs.dropdown.data-api', toggle, Dropdown.prototype.keydown)
    .on('keydown.bs.dropdown.data-api', '.dropdown-menu', Dropdown.prototype.keydown)

}(jQuery);

/* ========================================================================
 * Bootstrap: modal.js v3.3.7
 * http://getbootstrap.com/javascript/#modals
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // MODAL CLASS DEFINITION
  // ======================

  var Modal = function (element, options) {
    this.options             = options
    this.$body               = $(document.body)
    this.$element            = $(element)
    this.$dialog             = this.$element.find('.modal-dialog')
    this.$backdrop           = null
    this.isShown             = null
    this.originalBodyPad     = null
    this.scrollbarWidth      = 0
    this.ignoreBackdropClick = false

    if (this.options.remote) {
      this.$element
        .find('.modal-content')
        .load(this.options.remote, $.proxy(function () {
          this.$element.trigger('loaded.bs.modal')
        }, this))
    }
  }

  Modal.VERSION  = '3.3.7'

  Modal.TRANSITION_DURATION = 300
  Modal.BACKDROP_TRANSITION_DURATION = 150

  Modal.DEFAULTS = {
    backdrop: true,
    keyboard: true,
    show: true
  }

  Modal.prototype.toggle = function (_relatedTarget) {
    return this.isShown ? this.hide() : this.show(_relatedTarget)
  }

  Modal.prototype.show = function (_relatedTarget) {
    var that = this
    var e    = $.Event('show.bs.modal', { relatedTarget: _relatedTarget })

    this.$element.trigger(e)

    if (this.isShown || e.isDefaultPrevented()) return

    this.isShown = true

    this.checkScrollbar()
    this.setScrollbar()
    this.$body.addClass('modal-open')

    this.escape()
    this.resize()

    this.$element.on('click.dismiss.bs.modal', '[data-dismiss="modal"]', $.proxy(this.hide, this))

    this.$dialog.on('mousedown.dismiss.bs.modal', function () {
      that.$element.one('mouseup.dismiss.bs.modal', function (e) {
        if ($(e.target).is(that.$element)) that.ignoreBackdropClick = true
      })
    })

    this.backdrop(function () {
      var transition = $.support.transition && that.$element.hasClass('fade')

      if (!that.$element.parent().length) {
        that.$element.appendTo(that.$body) // don't move modals dom position
      }

      that.$element
        .show()
        .scrollTop(0)

      that.adjustDialog()

      if (transition) {
        that.$element[0].offsetWidth // force reflow
      }

      that.$element.addClass('in')

      that.enforceFocus()

      var e = $.Event('shown.bs.modal', { relatedTarget: _relatedTarget })

      transition ?
        that.$dialog // wait for modal to slide in
          .one('bsTransitionEnd', function () {
            that.$element.trigger('focus').trigger(e)
          })
          .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
        that.$element.trigger('focus').trigger(e)
    })
  }

  Modal.prototype.hide = function (e) {
    if (e) e.preventDefault()

    e = $.Event('hide.bs.modal')

    this.$element.trigger(e)

    if (!this.isShown || e.isDefaultPrevented()) return

    this.isShown = false

    this.escape()
    this.resize()

    $(document).off('focusin.bs.modal')

    this.$element
      .removeClass('in')
      .off('click.dismiss.bs.modal')
      .off('mouseup.dismiss.bs.modal')

    this.$dialog.off('mousedown.dismiss.bs.modal')

    $.support.transition && this.$element.hasClass('fade') ?
      this.$element
        .one('bsTransitionEnd', $.proxy(this.hideModal, this))
        .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
      this.hideModal()
  }

  Modal.prototype.enforceFocus = function () {
    $(document)
      .off('focusin.bs.modal') // guard against infinite focus loop
      .on('focusin.bs.modal', $.proxy(function (e) {
        if (document !== e.target &&
            this.$element[0] !== e.target &&
            !this.$element.has(e.target).length) {
          this.$element.trigger('focus')
        }
      }, this))
  }

  Modal.prototype.escape = function () {
    if (this.isShown && this.options.keyboard) {
      this.$element.on('keydown.dismiss.bs.modal', $.proxy(function (e) {
        e.which == 27 && this.hide()
      }, this))
    } else if (!this.isShown) {
      this.$element.off('keydown.dismiss.bs.modal')
    }
  }

  Modal.prototype.resize = function () {
    if (this.isShown) {
      $(window).on('resize.bs.modal', $.proxy(this.handleUpdate, this))
    } else {
      $(window).off('resize.bs.modal')
    }
  }

  Modal.prototype.hideModal = function () {
    var that = this
    this.$element.hide()
    this.backdrop(function () {
      that.$body.removeClass('modal-open')
      that.resetAdjustments()
      that.resetScrollbar()
      that.$element.trigger('hidden.bs.modal')
    })
  }

  Modal.prototype.removeBackdrop = function () {
    this.$backdrop && this.$backdrop.remove()
    this.$backdrop = null
  }

  Modal.prototype.backdrop = function (callback) {
    var that = this
    var animate = this.$element.hasClass('fade') ? 'fade' : ''

    if (this.isShown && this.options.backdrop) {
      var doAnimate = $.support.transition && animate

      this.$backdrop = $(document.createElement('div'))
        .addClass('modal-backdrop ' + animate)
        .appendTo(this.$body)

      this.$element.on('click.dismiss.bs.modal', $.proxy(function (e) {
        if (this.ignoreBackdropClick) {
          this.ignoreBackdropClick = false
          return
        }
        if (e.target !== e.currentTarget) return
        this.options.backdrop == 'static'
          ? this.$element[0].focus()
          : this.hide()
      }, this))

      if (doAnimate) this.$backdrop[0].offsetWidth // force reflow

      this.$backdrop.addClass('in')

      if (!callback) return

      doAnimate ?
        this.$backdrop
          .one('bsTransitionEnd', callback)
          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
        callback()

    } else if (!this.isShown && this.$backdrop) {
      this.$backdrop.removeClass('in')

      var callbackRemove = function () {
        that.removeBackdrop()
        callback && callback()
      }
      $.support.transition && this.$element.hasClass('fade') ?
        this.$backdrop
          .one('bsTransitionEnd', callbackRemove)
          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
        callbackRemove()

    } else if (callback) {
      callback()
    }
  }

  // these following methods are used to handle overflowing modals

  Modal.prototype.handleUpdate = function () {
    this.adjustDialog()
  }

  Modal.prototype.adjustDialog = function () {
    var modalIsOverflowing = this.$element[0].scrollHeight > document.documentElement.clientHeight

    this.$element.css({
      paddingLeft:  !this.bodyIsOverflowing && modalIsOverflowing ? this.scrollbarWidth : '',
      paddingRight: this.bodyIsOverflowing && !modalIsOverflowing ? this.scrollbarWidth : ''
    })
  }

  Modal.prototype.resetAdjustments = function () {
    this.$element.css({
      paddingLeft: '',
      paddingRight: ''
    })
  }

  Modal.prototype.checkScrollbar = function () {
    var fullWindowWidth = window.innerWidth
    if (!fullWindowWidth) { // workaround for missing window.innerWidth in IE8
      var documentElementRect = document.documentElement.getBoundingClientRect()
      fullWindowWidth = documentElementRect.right - Math.abs(documentElementRect.left)
    }
    this.bodyIsOverflowing = document.body.clientWidth < fullWindowWidth
    this.scrollbarWidth = this.measureScrollbar()
  }

  Modal.prototype.setScrollbar = function () {
    var bodyPad = parseInt((this.$body.css('padding-right') || 0), 10)
    this.originalBodyPad = document.body.style.paddingRight || ''
    if (this.bodyIsOverflowing) this.$body.css('padding-right', bodyPad + this.scrollbarWidth)
  }

  Modal.prototype.resetScrollbar = function () {
    this.$body.css('padding-right', this.originalBodyPad)
  }

  Modal.prototype.measureScrollbar = function () { // thx walsh
    var scrollDiv = document.createElement('div')
    scrollDiv.className = 'modal-scrollbar-measure'
    this.$body.append(scrollDiv)
    var scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth
    this.$body[0].removeChild(scrollDiv)
    return scrollbarWidth
  }


  // MODAL PLUGIN DEFINITION
  // =======================

  function Plugin(option, _relatedTarget) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.modal')
      var options = $.extend({}, Modal.DEFAULTS, $this.data(), typeof option == 'object' && option)

      if (!data) $this.data('bs.modal', (data = new Modal(this, options)))
      if (typeof option == 'string') data[option](_relatedTarget)
      else if (options.show) data.show(_relatedTarget)
    })
  }

  var old = $.fn.modal

  $.fn.modal             = Plugin
  $.fn.modal.Constructor = Modal


  // MODAL NO CONFLICT
  // =================

  $.fn.modal.noConflict = function () {
    $.fn.modal = old
    return this
  }


  // MODAL DATA-API
  // ==============

  $(document).on('click.bs.modal.data-api', '[data-toggle="modal"]', function (e) {
    var $this   = $(this)
    var href    = $this.attr('href')
    var $target = $($this.attr('data-target') || (href && href.replace(/.*(?=#[^\s]+$)/, ''))) // strip for ie7
    var option  = $target.data('bs.modal') ? 'toggle' : $.extend({ remote: !/#/.test(href) && href }, $target.data(), $this.data())

    if ($this.is('a')) e.preventDefault()

    $target.one('show.bs.modal', function (showEvent) {
      if (showEvent.isDefaultPrevented()) return // only register focus restorer if modal will actually get shown
      $target.one('hidden.bs.modal', function () {
        $this.is(':visible') && $this.trigger('focus')
      })
    })
    Plugin.call($target, option, this)
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: tooltip.js v3.3.7
 * http://getbootstrap.com/javascript/#tooltip
 * Inspired by the original jQuery.tipsy by Jason Frame
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // TOOLTIP PUBLIC CLASS DEFINITION
  // ===============================

  var Tooltip = function (element, options) {
    this.type       = null
    this.options    = null
    this.enabled    = null
    this.timeout    = null
    this.hoverState = null
    this.$element   = null
    this.inState    = null

    this.init('tooltip', element, options)
  }

  Tooltip.VERSION  = '3.3.7'

  Tooltip.TRANSITION_DURATION = 150

  Tooltip.DEFAULTS = {
    animation: true,
    placement: 'top',
    selector: false,
    template: '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
    trigger: 'hover focus',
    title: '',
    delay: 0,
    html: false,
    container: false,
    viewport: {
      selector: 'body',
      padding: 0
    }
  }

  Tooltip.prototype.init = function (type, element, options) {
    this.enabled   = true
    this.type      = type
    this.$element  = $(element)
    this.options   = this.getOptions(options)
    this.$viewport = this.options.viewport && $($.isFunction(this.options.viewport) ? this.options.viewport.call(this, this.$element) : (this.options.viewport.selector || this.options.viewport))
    this.inState   = { click: false, hover: false, focus: false }

    if (this.$element[0] instanceof document.constructor && !this.options.selector) {
      throw new Error('`selector` option must be specified when initializing ' + this.type + ' on the window.document object!')
    }

    var triggers = this.options.trigger.split(' ')

    for (var i = triggers.length; i--;) {
      var trigger = triggers[i]

      if (trigger == 'click') {
        this.$element.on('click.' + this.type, this.options.selector, $.proxy(this.toggle, this))
      } else if (trigger != 'manual') {
        var eventIn  = trigger == 'hover' ? 'mouseenter' : 'focusin'
        var eventOut = trigger == 'hover' ? 'mouseleave' : 'focusout'

        this.$element.on(eventIn  + '.' + this.type, this.options.selector, $.proxy(this.enter, this))
        this.$element.on(eventOut + '.' + this.type, this.options.selector, $.proxy(this.leave, this))
      }
    }

    this.options.selector ?
      (this._options = $.extend({}, this.options, { trigger: 'manual', selector: '' })) :
      this.fixTitle()
  }

  Tooltip.prototype.getDefaults = function () {
    return Tooltip.DEFAULTS
  }

  Tooltip.prototype.getOptions = function (options) {
    options = $.extend({}, this.getDefaults(), this.$element.data(), options)

    if (options.delay && typeof options.delay == 'number') {
      options.delay = {
        show: options.delay,
        hide: options.delay
      }
    }

    return options
  }

  Tooltip.prototype.getDelegateOptions = function () {
    var options  = {}
    var defaults = this.getDefaults()

    this._options && $.each(this._options, function (key, value) {
      if (defaults[key] != value) options[key] = value
    })

    return options
  }

  Tooltip.prototype.enter = function (obj) {
    var self = obj instanceof this.constructor ?
      obj : $(obj.currentTarget).data('bs.' + this.type)

    if (!self) {
      self = new this.constructor(obj.currentTarget, this.getDelegateOptions())
      $(obj.currentTarget).data('bs.' + this.type, self)
    }

    if (obj instanceof $.Event) {
      self.inState[obj.type == 'focusin' ? 'focus' : 'hover'] = true
    }

    if (self.tip().hasClass('in') || self.hoverState == 'in') {
      self.hoverState = 'in'
      return
    }

    clearTimeout(self.timeout)

    self.hoverState = 'in'

    if (!self.options.delay || !self.options.delay.show) return self.show()

    self.timeout = setTimeout(function () {
      if (self.hoverState == 'in') self.show()
    }, self.options.delay.show)
  }

  Tooltip.prototype.isInStateTrue = function () {
    for (var key in this.inState) {
      if (this.inState[key]) return true
    }

    return false
  }

  Tooltip.prototype.leave = function (obj) {
    var self = obj instanceof this.constructor ?
      obj : $(obj.currentTarget).data('bs.' + this.type)

    if (!self) {
      self = new this.constructor(obj.currentTarget, this.getDelegateOptions())
      $(obj.currentTarget).data('bs.' + this.type, self)
    }

    if (obj instanceof $.Event) {
      self.inState[obj.type == 'focusout' ? 'focus' : 'hover'] = false
    }

    if (self.isInStateTrue()) return

    clearTimeout(self.timeout)

    self.hoverState = 'out'

    if (!self.options.delay || !self.options.delay.hide) return self.hide()

    self.timeout = setTimeout(function () {
      if (self.hoverState == 'out') self.hide()
    }, self.options.delay.hide)
  }

  Tooltip.prototype.show = function () {
    var e = $.Event('show.bs.' + this.type)

    if (this.hasContent() && this.enabled) {
      this.$element.trigger(e)

      var inDom = $.contains(this.$element[0].ownerDocument.documentElement, this.$element[0])
      if (e.isDefaultPrevented() || !inDom) return
      var that = this

      var $tip = this.tip()

      var tipId = this.getUID(this.type)

      this.setContent()
      $tip.attr('id', tipId)
      this.$element.attr('aria-describedby', tipId)

      if (this.options.animation) $tip.addClass('fade')

      var placement = typeof this.options.placement == 'function' ?
        this.options.placement.call(this, $tip[0], this.$element[0]) :
        this.options.placement

      var autoToken = /\s?auto?\s?/i
      var autoPlace = autoToken.test(placement)
      if (autoPlace) placement = placement.replace(autoToken, '') || 'top'

      $tip
        .detach()
        .css({ top: 0, left: 0, display: 'block' })
        .addClass(placement)
        .data('bs.' + this.type, this)

      this.options.container ? $tip.appendTo(this.options.container) : $tip.insertAfter(this.$element)
      this.$element.trigger('inserted.bs.' + this.type)

      var pos          = this.getPosition()
      var actualWidth  = $tip[0].offsetWidth
      var actualHeight = $tip[0].offsetHeight

      if (autoPlace) {
        var orgPlacement = placement
        var viewportDim = this.getPosition(this.$viewport)

        placement = placement == 'bottom' && pos.bottom + actualHeight > viewportDim.bottom ? 'top'    :
                    placement == 'top'    && pos.top    - actualHeight < viewportDim.top    ? 'bottom' :
                    placement == 'right'  && pos.right  + actualWidth  > viewportDim.width  ? 'left'   :
                    placement == 'left'   && pos.left   - actualWidth  < viewportDim.left   ? 'right'  :
                    placement

        $tip
          .removeClass(orgPlacement)
          .addClass(placement)
      }

      var calculatedOffset = this.getCalculatedOffset(placement, pos, actualWidth, actualHeight)

      this.applyPlacement(calculatedOffset, placement)

      var complete = function () {
        var prevHoverState = that.hoverState
        that.$element.trigger('shown.bs.' + that.type)
        that.hoverState = null

        if (prevHoverState == 'out') that.leave(that)
      }

      $.support.transition && this.$tip.hasClass('fade') ?
        $tip
          .one('bsTransitionEnd', complete)
          .emulateTransitionEnd(Tooltip.TRANSITION_DURATION) :
        complete()
    }
  }

  Tooltip.prototype.applyPlacement = function (offset, placement) {
    var $tip   = this.tip()
    var width  = $tip[0].offsetWidth
    var height = $tip[0].offsetHeight

    // manually read margins because getBoundingClientRect includes difference
    var marginTop = parseInt($tip.css('margin-top'), 10)
    var marginLeft = parseInt($tip.css('margin-left'), 10)

    // we must check for NaN for ie 8/9
    if (isNaN(marginTop))  marginTop  = 0
    if (isNaN(marginLeft)) marginLeft = 0

    offset.top  += marginTop
    offset.left += marginLeft

    // $.fn.offset doesn't round pixel values
    // so we use setOffset directly with our own function B-0
    $.offset.setOffset($tip[0], $.extend({
      using: function (props) {
        $tip.css({
          top: Math.round(props.top),
          left: Math.round(props.left)
        })
      }
    }, offset), 0)

    $tip.addClass('in')

    // check to see if placing tip in new offset caused the tip to resize itself
    var actualWidth  = $tip[0].offsetWidth
    var actualHeight = $tip[0].offsetHeight

    if (placement == 'top' && actualHeight != height) {
      offset.top = offset.top + height - actualHeight
    }

    var delta = this.getViewportAdjustedDelta(placement, offset, actualWidth, actualHeight)

    if (delta.left) offset.left += delta.left
    else offset.top += delta.top

    var isVertical          = /top|bottom/.test(placement)
    var arrowDelta          = isVertical ? delta.left * 2 - width + actualWidth : delta.top * 2 - height + actualHeight
    var arrowOffsetPosition = isVertical ? 'offsetWidth' : 'offsetHeight'

    $tip.offset(offset)
    this.replaceArrow(arrowDelta, $tip[0][arrowOffsetPosition], isVertical)
  }

  Tooltip.prototype.replaceArrow = function (delta, dimension, isVertical) {
    this.arrow()
      .css(isVertical ? 'left' : 'top', 50 * (1 - delta / dimension) + '%')
      .css(isVertical ? 'top' : 'left', '')
  }

  Tooltip.prototype.setContent = function () {
    var $tip  = this.tip()
    var title = this.getTitle()

    $tip.find('.tooltip-inner')[this.options.html ? 'html' : 'text'](title)
    $tip.removeClass('fade in top bottom left right')
  }

  Tooltip.prototype.hide = function (callback) {
    var that = this
    var $tip = $(this.$tip)
    var e    = $.Event('hide.bs.' + this.type)

    function complete() {
      if (that.hoverState != 'in') $tip.detach()
      if (that.$element) { // TODO: Check whether guarding this code with this `if` is really necessary.
        that.$element
          .removeAttr('aria-describedby')
          .trigger('hidden.bs.' + that.type)
      }
      callback && callback()
    }

    this.$element.trigger(e)

    if (e.isDefaultPrevented()) return

    $tip.removeClass('in')

    $.support.transition && $tip.hasClass('fade') ?
      $tip
        .one('bsTransitionEnd', complete)
        .emulateTransitionEnd(Tooltip.TRANSITION_DURATION) :
      complete()

    this.hoverState = null

    return this
  }

  Tooltip.prototype.fixTitle = function () {
    var $e = this.$element
    if ($e.attr('title') || typeof $e.attr('data-original-title') != 'string') {
      $e.attr('data-original-title', $e.attr('title') || '').attr('title', '')
    }
  }

  Tooltip.prototype.hasContent = function () {
    return this.getTitle()
  }

  Tooltip.prototype.getPosition = function ($element) {
    $element   = $element || this.$element

    var el     = $element[0]
    var isBody = el.tagName == 'BODY'

    var elRect    = el.getBoundingClientRect()
    if (elRect.width == null) {
      // width and height are missing in IE8, so compute them manually; see https://github.com/twbs/bootstrap/issues/14093
      elRect = $.extend({}, elRect, { width: elRect.right - elRect.left, height: elRect.bottom - elRect.top })
    }
    var isSvg = window.SVGElement && el instanceof window.SVGElement
    // Avoid using $.offset() on SVGs since it gives incorrect results in jQuery 3.
    // See https://github.com/twbs/bootstrap/issues/20280
    var elOffset  = isBody ? { top: 0, left: 0 } : (isSvg ? null : $element.offset())
    var scroll    = { scroll: isBody ? document.documentElement.scrollTop || document.body.scrollTop : $element.scrollTop() }
    var outerDims = isBody ? { width: $(window).width(), height: $(window).height() } : null

    return $.extend({}, elRect, scroll, outerDims, elOffset)
  }

  Tooltip.prototype.getCalculatedOffset = function (placement, pos, actualWidth, actualHeight) {
    return placement == 'bottom' ? { top: pos.top + pos.height,   left: pos.left + pos.width / 2 - actualWidth / 2 } :
           placement == 'top'    ? { top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2 } :
           placement == 'left'   ? { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth } :
        /* placement == 'right' */ { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width }

  }

  Tooltip.prototype.getViewportAdjustedDelta = function (placement, pos, actualWidth, actualHeight) {
    var delta = { top: 0, left: 0 }
    if (!this.$viewport) return delta

    var viewportPadding = this.options.viewport && this.options.viewport.padding || 0
    var viewportDimensions = this.getPosition(this.$viewport)

    if (/right|left/.test(placement)) {
      var topEdgeOffset    = pos.top - viewportPadding - viewportDimensions.scroll
      var bottomEdgeOffset = pos.top + viewportPadding - viewportDimensions.scroll + actualHeight
      if (topEdgeOffset < viewportDimensions.top) { // top overflow
        delta.top = viewportDimensions.top - topEdgeOffset
      } else if (bottomEdgeOffset > viewportDimensions.top + viewportDimensions.height) { // bottom overflow
        delta.top = viewportDimensions.top + viewportDimensions.height - bottomEdgeOffset
      }
    } else {
      var leftEdgeOffset  = pos.left - viewportPadding
      var rightEdgeOffset = pos.left + viewportPadding + actualWidth
      if (leftEdgeOffset < viewportDimensions.left) { // left overflow
        delta.left = viewportDimensions.left - leftEdgeOffset
      } else if (rightEdgeOffset > viewportDimensions.right) { // right overflow
        delta.left = viewportDimensions.left + viewportDimensions.width - rightEdgeOffset
      }
    }

    return delta
  }

  Tooltip.prototype.getTitle = function () {
    var title
    var $e = this.$element
    var o  = this.options

    title = $e.attr('data-original-title')
      || (typeof o.title == 'function' ? o.title.call($e[0]) :  o.title)

    return title
  }

  Tooltip.prototype.getUID = function (prefix) {
    do prefix += ~~(Math.random() * 1000000)
    while (document.getElementById(prefix))
    return prefix
  }

  Tooltip.prototype.tip = function () {
    if (!this.$tip) {
      this.$tip = $(this.options.template)
      if (this.$tip.length != 1) {
        throw new Error(this.type + ' `template` option must consist of exactly 1 top-level element!')
      }
    }
    return this.$tip
  }

  Tooltip.prototype.arrow = function () {
    return (this.$arrow = this.$arrow || this.tip().find('.tooltip-arrow'))
  }

  Tooltip.prototype.enable = function () {
    this.enabled = true
  }

  Tooltip.prototype.disable = function () {
    this.enabled = false
  }

  Tooltip.prototype.toggleEnabled = function () {
    this.enabled = !this.enabled
  }

  Tooltip.prototype.toggle = function (e) {
    var self = this
    if (e) {
      self = $(e.currentTarget).data('bs.' + this.type)
      if (!self) {
        self = new this.constructor(e.currentTarget, this.getDelegateOptions())
        $(e.currentTarget).data('bs.' + this.type, self)
      }
    }

    if (e) {
      self.inState.click = !self.inState.click
      if (self.isInStateTrue()) self.enter(self)
      else self.leave(self)
    } else {
      self.tip().hasClass('in') ? self.leave(self) : self.enter(self)
    }
  }

  Tooltip.prototype.destroy = function () {
    var that = this
    clearTimeout(this.timeout)
    this.hide(function () {
      that.$element.off('.' + that.type).removeData('bs.' + that.type)
      if (that.$tip) {
        that.$tip.detach()
      }
      that.$tip = null
      that.$arrow = null
      that.$viewport = null
      that.$element = null
    })
  }


  // TOOLTIP PLUGIN DEFINITION
  // =========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.tooltip')
      var options = typeof option == 'object' && option

      if (!data && /destroy|hide/.test(option)) return
      if (!data) $this.data('bs.tooltip', (data = new Tooltip(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.tooltip

  $.fn.tooltip             = Plugin
  $.fn.tooltip.Constructor = Tooltip


  // TOOLTIP NO CONFLICT
  // ===================

  $.fn.tooltip.noConflict = function () {
    $.fn.tooltip = old
    return this
  }

}(jQuery);

/* ========================================================================
 * Bootstrap: popover.js v3.3.7
 * http://getbootstrap.com/javascript/#popovers
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // POPOVER PUBLIC CLASS DEFINITION
  // ===============================

  var Popover = function (element, options) {
    this.init('popover', element, options)
  }

  if (!$.fn.tooltip) throw new Error('Popover requires tooltip.js')

  Popover.VERSION  = '3.3.7'

  Popover.DEFAULTS = $.extend({}, $.fn.tooltip.Constructor.DEFAULTS, {
    placement: 'right',
    trigger: 'click',
    content: '',
    template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'
  })


  // NOTE: POPOVER EXTENDS tooltip.js
  // ================================

  Popover.prototype = $.extend({}, $.fn.tooltip.Constructor.prototype)

  Popover.prototype.constructor = Popover

  Popover.prototype.getDefaults = function () {
    return Popover.DEFAULTS
  }

  Popover.prototype.setContent = function () {
    var $tip    = this.tip()
    var title   = this.getTitle()
    var content = this.getContent()

    $tip.find('.popover-title')[this.options.html ? 'html' : 'text'](title)
    $tip.find('.popover-content').children().detach().end()[ // we use append for html objects to maintain js events
      this.options.html ? (typeof content == 'string' ? 'html' : 'append') : 'text'
    ](content)

    $tip.removeClass('fade top bottom left right in')

    // IE8 doesn't accept hiding via the `:empty` pseudo selector, we have to do
    // this manually by checking the contents.
    if (!$tip.find('.popover-title').html()) $tip.find('.popover-title').hide()
  }

  Popover.prototype.hasContent = function () {
    return this.getTitle() || this.getContent()
  }

  Popover.prototype.getContent = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-content')
      || (typeof o.content == 'function' ?
            o.content.call($e[0]) :
            o.content)
  }

  Popover.prototype.arrow = function () {
    return (this.$arrow = this.$arrow || this.tip().find('.arrow'))
  }


  // POPOVER PLUGIN DEFINITION
  // =========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.popover')
      var options = typeof option == 'object' && option

      if (!data && /destroy|hide/.test(option)) return
      if (!data) $this.data('bs.popover', (data = new Popover(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.popover

  $.fn.popover             = Plugin
  $.fn.popover.Constructor = Popover


  // POPOVER NO CONFLICT
  // ===================

  $.fn.popover.noConflict = function () {
    $.fn.popover = old
    return this
  }

}(jQuery);

/* ========================================================================
 * Bootstrap: tab.js v3.3.7
 * http://getbootstrap.com/javascript/#tabs
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // TAB CLASS DEFINITION
  // ====================

  var Tab = function (element) {
    // jscs:disable requireDollarBeforejQueryAssignment
    this.element = $(element)
    // jscs:enable requireDollarBeforejQueryAssignment
  }

  Tab.VERSION = '3.3.7'

  Tab.TRANSITION_DURATION = 150

  Tab.prototype.show = function () {
    var $this    = this.element
    var $ul      = $this.closest('ul:not(.dropdown-menu)')
    var selector = $this.data('target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
    }

    if ($this.parent('li').hasClass('active')) return

    var $previous = $ul.find('.active:last a')
    var hideEvent = $.Event('hide.bs.tab', {
      relatedTarget: $this[0]
    })
    var showEvent = $.Event('show.bs.tab', {
      relatedTarget: $previous[0]
    })

    $previous.trigger(hideEvent)
    $this.trigger(showEvent)

    if (showEvent.isDefaultPrevented() || hideEvent.isDefaultPrevented()) return

    var $target = $(selector)

    this.activate($this.closest('li'), $ul)
    this.activate($target, $target.parent(), function () {
      $previous.trigger({
        type: 'hidden.bs.tab',
        relatedTarget: $this[0]
      })
      $this.trigger({
        type: 'shown.bs.tab',
        relatedTarget: $previous[0]
      })
    })
  }

  Tab.prototype.activate = function (element, container, callback) {
    var $active    = container.find('> .active')
    var transition = callback
      && $.support.transition
      && ($active.length && $active.hasClass('fade') || !!container.find('> .fade').length)

    function next() {
      $active
        .removeClass('active')
        .find('> .dropdown-menu > .active')
          .removeClass('active')
        .end()
        .find('[data-toggle="tab"]')
          .attr('aria-expanded', false)

      element
        .addClass('active')
        .find('[data-toggle="tab"]')
          .attr('aria-expanded', true)

      if (transition) {
        element[0].offsetWidth // reflow for transition
        element.addClass('in')
      } else {
        element.removeClass('fade')
      }

      if (element.parent('.dropdown-menu').length) {
        element
          .closest('li.dropdown')
            .addClass('active')
          .end()
          .find('[data-toggle="tab"]')
            .attr('aria-expanded', true)
      }

      callback && callback()
    }

    $active.length && transition ?
      $active
        .one('bsTransitionEnd', next)
        .emulateTransitionEnd(Tab.TRANSITION_DURATION) :
      next()

    $active.removeClass('in')
  }


  // TAB PLUGIN DEFINITION
  // =====================

  function Plugin(option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.tab')

      if (!data) $this.data('bs.tab', (data = new Tab(this)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.tab

  $.fn.tab             = Plugin
  $.fn.tab.Constructor = Tab


  // TAB NO CONFLICT
  // ===============

  $.fn.tab.noConflict = function () {
    $.fn.tab = old
    return this
  }


  // TAB DATA-API
  // ============

  var clickHandler = function (e) {
    e.preventDefault()
    Plugin.call($(this), 'show')
  }

  $(document)
    .on('click.bs.tab.data-api', '[data-toggle="tab"]', clickHandler)
    .on('click.bs.tab.data-api', '[data-toggle="pill"]', clickHandler)

}(jQuery);

/* ========================================================================
 * Bootstrap: affix.js v3.3.7
 * http://getbootstrap.com/javascript/#affix
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // AFFIX CLASS DEFINITION
  // ======================

  var Affix = function (element, options) {
    this.options = $.extend({}, Affix.DEFAULTS, options)

    this.$target = $(this.options.target)
      .on('scroll.bs.affix.data-api', $.proxy(this.checkPosition, this))
      .on('click.bs.affix.data-api',  $.proxy(this.checkPositionWithEventLoop, this))

    this.$element     = $(element)
    this.affixed      = null
    this.unpin        = null
    this.pinnedOffset = null

    this.checkPosition()
  }

  Affix.VERSION  = '3.3.7'

  Affix.RESET    = 'affix affix-top affix-bottom'

  Affix.DEFAULTS = {
    offset: 0,
    target: window
  }

  Affix.prototype.getState = function (scrollHeight, height, offsetTop, offsetBottom) {
    var scrollTop    = this.$target.scrollTop()
    var position     = this.$element.offset()
    var targetHeight = this.$target.height()

    if (offsetTop != null && this.affixed == 'top') return scrollTop < offsetTop ? 'top' : false

    if (this.affixed == 'bottom') {
      if (offsetTop != null) return (scrollTop + this.unpin <= position.top) ? false : 'bottom'
      return (scrollTop + targetHeight <= scrollHeight - offsetBottom) ? false : 'bottom'
    }

    var initializing   = this.affixed == null
    var colliderTop    = initializing ? scrollTop : position.top
    var colliderHeight = initializing ? targetHeight : height

    if (offsetTop != null && scrollTop <= offsetTop) return 'top'
    if (offsetBottom != null && (colliderTop + colliderHeight >= scrollHeight - offsetBottom)) return 'bottom'

    return false
  }

  Affix.prototype.getPinnedOffset = function () {
    if (this.pinnedOffset) return this.pinnedOffset
    this.$element.removeClass(Affix.RESET).addClass('affix')
    var scrollTop = this.$target.scrollTop()
    var position  = this.$element.offset()
    return (this.pinnedOffset = position.top - scrollTop)
  }

  Affix.prototype.checkPositionWithEventLoop = function () {
    setTimeout($.proxy(this.checkPosition, this), 1)
  }

  Affix.prototype.checkPosition = function () {
    if (!this.$element.is(':visible')) return

    var height       = this.$element.height()
    var offset       = this.options.offset
    var offsetTop    = offset.top
    var offsetBottom = offset.bottom
    var scrollHeight = Math.max($(document).height(), $(document.body).height())

    if (typeof offset != 'object')         offsetBottom = offsetTop = offset
    if (typeof offsetTop == 'function')    offsetTop    = offset.top(this.$element)
    if (typeof offsetBottom == 'function') offsetBottom = offset.bottom(this.$element)

    var affix = this.getState(scrollHeight, height, offsetTop, offsetBottom)

    if (this.affixed != affix) {
      if (this.unpin != null) this.$element.css('top', '')

      var affixType = 'affix' + (affix ? '-' + affix : '')
      var e         = $.Event(affixType + '.bs.affix')

      this.$element.trigger(e)

      if (e.isDefaultPrevented()) return

      this.affixed = affix
      this.unpin = affix == 'bottom' ? this.getPinnedOffset() : null

      this.$element
        .removeClass(Affix.RESET)
        .addClass(affixType)
        .trigger(affixType.replace('affix', 'affixed') + '.bs.affix')
    }

    if (affix == 'bottom') {
      this.$element.offset({
        top: scrollHeight - height - offsetBottom
      })
    }
  }


  // AFFIX PLUGIN DEFINITION
  // =======================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.affix')
      var options = typeof option == 'object' && option

      if (!data) $this.data('bs.affix', (data = new Affix(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.affix

  $.fn.affix             = Plugin
  $.fn.affix.Constructor = Affix


  // AFFIX NO CONFLICT
  // =================

  $.fn.affix.noConflict = function () {
    $.fn.affix = old
    return this
  }


  // AFFIX DATA-API
  // ==============

  $(window).on('load', function () {
    $('[data-spy="affix"]').each(function () {
      var $spy = $(this)
      var data = $spy.data()

      data.offset = data.offset || {}

      if (data.offsetBottom != null) data.offset.bottom = data.offsetBottom
      if (data.offsetTop    != null) data.offset.top    = data.offsetTop

      Plugin.call($spy, data)
    })
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: collapse.js v3.3.7
 * http://getbootstrap.com/javascript/#collapse
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */

/* jshint latedef: false */

+function ($) {
  'use strict';

  // COLLAPSE PUBLIC CLASS DEFINITION
  // ================================

  var Collapse = function (element, options) {
    this.$element      = $(element)
    this.options       = $.extend({}, Collapse.DEFAULTS, options)
    this.$trigger      = $('[data-toggle="collapse"][href="#' + element.id + '"],' +
                           '[data-toggle="collapse"][data-target="#' + element.id + '"]')
    this.transitioning = null

    if (this.options.parent) {
      this.$parent = this.getParent()
    } else {
      this.addAriaAndCollapsedClass(this.$element, this.$trigger)
    }

    if (this.options.toggle) this.toggle()
  }

  Collapse.VERSION  = '3.3.7'

  Collapse.TRANSITION_DURATION = 350

  Collapse.DEFAULTS = {
    toggle: true
  }

  Collapse.prototype.dimension = function () {
    var hasWidth = this.$element.hasClass('width')
    return hasWidth ? 'width' : 'height'
  }

  Collapse.prototype.show = function () {
    if (this.transitioning || this.$element.hasClass('in')) return

    var activesData
    var actives = this.$parent && this.$parent.children('.panel').children('.in, .collapsing')

    if (actives && actives.length) {
      activesData = actives.data('bs.collapse')
      if (activesData && activesData.transitioning) return
    }

    var startEvent = $.Event('show.bs.collapse')
    this.$element.trigger(startEvent)
    if (startEvent.isDefaultPrevented()) return

    if (actives && actives.length) {
      Plugin.call(actives, 'hide')
      activesData || actives.data('bs.collapse', null)
    }

    var dimension = this.dimension()

    this.$element
      .removeClass('collapse')
      .addClass('collapsing')[dimension](0)
      .attr('aria-expanded', true)

    this.$trigger
      .removeClass('collapsed')
      .attr('aria-expanded', true)

    this.transitioning = 1

    var complete = function () {
      this.$element
        .removeClass('collapsing')
        .addClass('collapse in')[dimension]('')
      this.transitioning = 0
      this.$element
        .trigger('shown.bs.collapse')
    }

    if (!$.support.transition) return complete.call(this)

    var scrollSize = $.camelCase(['scroll', dimension].join('-'))

    this.$element
      .one('bsTransitionEnd', $.proxy(complete, this))
      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)[dimension](this.$element[0][scrollSize])
  }

  Collapse.prototype.hide = function () {
    if (this.transitioning || !this.$element.hasClass('in')) return

    var startEvent = $.Event('hide.bs.collapse')
    this.$element.trigger(startEvent)
    if (startEvent.isDefaultPrevented()) return

    var dimension = this.dimension()

    this.$element[dimension](this.$element[dimension]())[0].offsetHeight

    this.$element
      .addClass('collapsing')
      .removeClass('collapse in')
      .attr('aria-expanded', false)

    this.$trigger
      .addClass('collapsed')
      .attr('aria-expanded', false)

    this.transitioning = 1

    var complete = function () {
      this.transitioning = 0
      this.$element
        .removeClass('collapsing')
        .addClass('collapse')
        .trigger('hidden.bs.collapse')
    }

    if (!$.support.transition) return complete.call(this)

    this.$element
      [dimension](0)
      .one('bsTransitionEnd', $.proxy(complete, this))
      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)
  }

  Collapse.prototype.toggle = function () {
    this[this.$element.hasClass('in') ? 'hide' : 'show']()
  }

  Collapse.prototype.getParent = function () {
    return $(this.options.parent)
      .find('[data-toggle="collapse"][data-parent="' + this.options.parent + '"]')
      .each($.proxy(function (i, element) {
        var $element = $(element)
        this.addAriaAndCollapsedClass(getTargetFromTrigger($element), $element)
      }, this))
      .end()
  }

  Collapse.prototype.addAriaAndCollapsedClass = function ($element, $trigger) {
    var isOpen = $element.hasClass('in')

    $element.attr('aria-expanded', isOpen)
    $trigger
      .toggleClass('collapsed', !isOpen)
      .attr('aria-expanded', isOpen)
  }

  function getTargetFromTrigger($trigger) {
    var href
    var target = $trigger.attr('data-target')
      || (href = $trigger.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') // strip for ie7

    return $(target)
  }


  // COLLAPSE PLUGIN DEFINITION
  // ==========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.collapse')
      var options = $.extend({}, Collapse.DEFAULTS, $this.data(), typeof option == 'object' && option)

      if (!data && options.toggle && /show|hide/.test(option)) options.toggle = false
      if (!data) $this.data('bs.collapse', (data = new Collapse(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.collapse

  $.fn.collapse             = Plugin
  $.fn.collapse.Constructor = Collapse


  // COLLAPSE NO CONFLICT
  // ====================

  $.fn.collapse.noConflict = function () {
    $.fn.collapse = old
    return this
  }


  // COLLAPSE DATA-API
  // =================

  $(document).on('click.bs.collapse.data-api', '[data-toggle="collapse"]', function (e) {
    var $this   = $(this)

    if (!$this.attr('data-target')) e.preventDefault()

    var $target = getTargetFromTrigger($this)
    var data    = $target.data('bs.collapse')
    var option  = data ? 'toggle' : $this.data()

    Plugin.call($target, option)
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: scrollspy.js v3.3.7
 * http://getbootstrap.com/javascript/#scrollspy
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // SCROLLSPY CLASS DEFINITION
  // ==========================

  function ScrollSpy(element, options) {
    this.$body          = $(document.body)
    this.$scrollElement = $(element).is(document.body) ? $(window) : $(element)
    this.options        = $.extend({}, ScrollSpy.DEFAULTS, options)
    this.selector       = (this.options.target || '') + ' .nav li > a'
    this.offsets        = []
    this.targets        = []
    this.activeTarget   = null
    this.scrollHeight   = 0

    this.$scrollElement.on('scroll.bs.scrollspy', $.proxy(this.process, this))
    this.refresh()
    this.process()
  }

  ScrollSpy.VERSION  = '3.3.7'

  ScrollSpy.DEFAULTS = {
    offset: 10
  }

  ScrollSpy.prototype.getScrollHeight = function () {
    return this.$scrollElement[0].scrollHeight || Math.max(this.$body[0].scrollHeight, document.documentElement.scrollHeight)
  }

  ScrollSpy.prototype.refresh = function () {
    var that          = this
    var offsetMethod  = 'offset'
    var offsetBase    = 0

    this.offsets      = []
    this.targets      = []
    this.scrollHeight = this.getScrollHeight()

    if (!$.isWindow(this.$scrollElement[0])) {
      offsetMethod = 'position'
      offsetBase   = this.$scrollElement.scrollTop()
    }

    this.$body
      .find(this.selector)
      .map(function () {
        var $el   = $(this)
        var href  = $el.data('target') || $el.attr('href')
        var $href = /^#./.test(href) && $(href)

        return ($href
          && $href.length
          && $href.is(':visible')
          && [[$href[offsetMethod]().top + offsetBase, href]]) || null
      })
      .sort(function (a, b) { return a[0] - b[0] })
      .each(function () {
        that.offsets.push(this[0])
        that.targets.push(this[1])
      })
  }

  ScrollSpy.prototype.process = function () {
    var scrollTop    = this.$scrollElement.scrollTop() + this.options.offset
    var scrollHeight = this.getScrollHeight()
    var maxScroll    = this.options.offset + scrollHeight - this.$scrollElement.height()
    var offsets      = this.offsets
    var targets      = this.targets
    var activeTarget = this.activeTarget
    var i

    if (this.scrollHeight != scrollHeight) {
      this.refresh()
    }

    if (scrollTop >= maxScroll) {
      return activeTarget != (i = targets[targets.length - 1]) && this.activate(i)
    }

    if (activeTarget && scrollTop < offsets[0]) {
      this.activeTarget = null
      return this.clear()
    }

    for (i = offsets.length; i--;) {
      activeTarget != targets[i]
        && scrollTop >= offsets[i]
        && (offsets[i + 1] === undefined || scrollTop < offsets[i + 1])
        && this.activate(targets[i])
    }
  }

  ScrollSpy.prototype.activate = function (target) {
    this.activeTarget = target

    this.clear()

    var selector = this.selector +
      '[data-target="' + target + '"],' +
      this.selector + '[href="' + target + '"]'

    var active = $(selector)
      .parents('li')
      .addClass('active')

    if (active.parent('.dropdown-menu').length) {
      active = active
        .closest('li.dropdown')
        .addClass('active')
    }

    active.trigger('activate.bs.scrollspy')
  }

  ScrollSpy.prototype.clear = function () {
    $(this.selector)
      .parentsUntil(this.options.target, '.active')
      .removeClass('active')
  }


  // SCROLLSPY PLUGIN DEFINITION
  // ===========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.scrollspy')
      var options = typeof option == 'object' && option

      if (!data) $this.data('bs.scrollspy', (data = new ScrollSpy(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.scrollspy

  $.fn.scrollspy             = Plugin
  $.fn.scrollspy.Constructor = ScrollSpy


  // SCROLLSPY NO CONFLICT
  // =====================

  $.fn.scrollspy.noConflict = function () {
    $.fn.scrollspy = old
    return this
  }


  // SCROLLSPY DATA-API
  // ==================

  $(window).on('load.bs.scrollspy.data-api', function () {
    $('[data-spy="scroll"]').each(function () {
      var $spy = $(this)
      Plugin.call($spy, $spy.data())
    })
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: transition.js v3.3.7
 * http://getbootstrap.com/javascript/#transitions
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // CSS TRANSITION SUPPORT (Shoutout: http://www.modernizr.com/)
  // ============================================================

  function transitionEnd() {
    var el = document.createElement('bootstrap')

    var transEndEventNames = {
      WebkitTransition : 'webkitTransitionEnd',
      MozTransition    : 'transitionend',
      OTransition      : 'oTransitionEnd otransitionend',
      transition       : 'transitionend'
    }

    for (var name in transEndEventNames) {
      if (el.style[name] !== undefined) {
        return { end: transEndEventNames[name] }
      }
    }

    return false // explicit for ie8 (  ._.)
  }

  // http://blog.alexmaccaw.com/css-transitions
  $.fn.emulateTransitionEnd = function (duration) {
    var called = false
    var $el = this
    $(this).one('bsTransitionEnd', function () { called = true })
    var callback = function () { if (!called) $($el).trigger($.support.transition.end) }
    setTimeout(callback, duration)
    return this
  }

  $(function () {
    $.support.transition = transitionEnd()

    if (!$.support.transition) return

    $.event.special.bsTransitionEnd = {
      bindType: $.support.transition.end,
      delegateType: $.support.transition.end,
      handle: function (e) {
        if ($(e.target).is(this)) return e.handleObj.handler.apply(this, arguments)
      }
    }
  })

}(jQuery);

/* ========================================================================
  =================== END OF BOOTSTRAP JS HERE ============================
 * ======================================================================== */


/*
     _ _      _       _
 ___| (_) ___| | __  (_)___
/ __| | |/ __| |/ /  | / __|
\__ \ | | (__|   < _ | \__ \
|___/_|_|\___|_|\_(_)/ |___/
                   |__/

 Version: 1.6.0
  Author: Ken Wheeler
 Website: http://kenwheeler.github.io
    Docs: http://kenwheeler.github.io/slick
    Repo: http://github.com/kenwheeler/slick
  Issues: http://github.com/kenwheeler/slick/issues

 */
/* global window, document, define, jQuery, setInterval, clearInterval */
(function(factory) {
    'use strict';
    if (typeof define === 'function' && define.amd) {
        define(['jquery'], factory);
    } else if (typeof exports !== 'undefined') {
        module.exports = factory(require('jquery'));
    } else {
        factory(jQuery);
    }

}(function($) {
    'use strict';
    var Slick = window.Slick || {};

    Slick = (function() {

        var instanceUid = 0;

        function Slick(element, settings) {

            var _ = this, dataSettings;

            _.defaults = {
                accessibility: true,
                adaptiveHeight: false,
                appendArrows: $(element),
                appendDots: $(element),
                arrows: true,
                asNavFor: null,
                prevArrow: '<button type="button" data-role="none" class="slick-prev" aria-label="Previous" tabindex="0" role="button">Previous</button>',
                nextArrow: '<button type="button" data-role="none" class="slick-next" aria-label="Next" tabindex="0" role="button">Next</button>',
                autoplay: false,
                autoplaySpeed: 3000,
                centerMode: false,
                centerPadding: '50px',
                cssEase: 'ease',
                customPaging: function(slider, i) {
                    return $('<button type="button" data-role="none" role="button" tabindex="0" />').text(i + 1);
                },
                dots: false,
                dotsClass: 'slick-dots',
                draggable: true,
                easing: 'linear',
                edgeFriction: 0.35,
                fade: false,
                focusOnSelect: false,
                infinite: true,
                initialSlide: 0,
                lazyLoad: 'ondemand',
                mobileFirst: false,
                pauseOnHover: true,
                pauseOnFocus: true,
                pauseOnDotsHover: false,
                respondTo: 'window',
                responsive: null,
                rows: 1,
                rtl: false,
                slide: '',
                slidesPerRow: 1,
                slidesToShow: 1,
                slidesToScroll: 1,
                speed: 500,
                swipe: true,
                swipeToSlide: false,
                touchMove: true,
                touchThreshold: 5,
                useCSS: true,
                useTransform: true,
                variableWidth: false,
                vertical: false,
                verticalSwiping: false,
                waitForAnimate: true,
                zIndex: 1000
            };

            _.initials = {
                animating: false,
                dragging: false,
                autoPlayTimer: null,
                currentDirection: 0,
                currentLeft: null,
                currentSlide: 0,
                direction: 1,
                $dots: null,
                listWidth: null,
                listHeight: null,
                loadIndex: 0,
                $nextArrow: null,
                $prevArrow: null,
                slideCount: null,
                slideWidth: null,
                $slideTrack: null,
                $slides: null,
                sliding: false,
                slideOffset: 0,
                swipeLeft: null,
                $list: null,
                touchObject: {},
                transformsEnabled: false,
                unslicked: false
            };

            $.extend(_, _.initials);

            _.activeBreakpoint = null;
            _.animType = null;
            _.animProp = null;
            _.breakpoints = [];
            _.breakpointSettings = [];
            _.cssTransitions = false;
            _.focussed = false;
            _.interrupted = false;
            _.hidden = 'hidden';
            _.paused = true;
            _.positionProp = null;
            _.respondTo = null;
            _.rowCount = 1;
            _.shouldClick = true;
            _.$slider = $(element);
            _.$slidesCache = null;
            _.transformType = null;
            _.transitionType = null;
            _.visibilityChange = 'visibilitychange';
            _.windowWidth = 0;
            _.windowTimer = null;

            dataSettings = $(element).data('slick') || {};

            _.options = $.extend({}, _.defaults, settings, dataSettings);

            _.currentSlide = _.options.initialSlide;

            _.originalSettings = _.options;

            if (typeof document.mozHidden !== 'undefined') {
                _.hidden = 'mozHidden';
                _.visibilityChange = 'mozvisibilitychange';
            } else if (typeof document.webkitHidden !== 'undefined') {
                _.hidden = 'webkitHidden';
                _.visibilityChange = 'webkitvisibilitychange';
            }

            _.autoPlay = $.proxy(_.autoPlay, _);
            _.autoPlayClear = $.proxy(_.autoPlayClear, _);
            _.autoPlayIterator = $.proxy(_.autoPlayIterator, _);
            _.changeSlide = $.proxy(_.changeSlide, _);
            _.clickHandler = $.proxy(_.clickHandler, _);
            _.selectHandler = $.proxy(_.selectHandler, _);
            _.setPosition = $.proxy(_.setPosition, _);
            _.swipeHandler = $.proxy(_.swipeHandler, _);
            _.dragHandler = $.proxy(_.dragHandler, _);
            _.keyHandler = $.proxy(_.keyHandler, _);

            _.instanceUid = instanceUid++;

            // A simple way to check for HTML strings
            // Strict HTML recognition (must start with <)
            // Extracted from jQuery v1.11 source
            _.htmlExpr = /^(?:\s*(<[\w\W]+>)[^>]*)$/;


            _.registerBreakpoints();
            _.init(true);

        }

        return Slick;

    }());

    Slick.prototype.activateADA = function() {
        var _ = this;

        _.$slideTrack.find('.slick-active').attr({
            'aria-hidden': 'false'
        }).find('a, input, button, select').attr({
            'tabindex': '0'
        });

    };

    Slick.prototype.addSlide = Slick.prototype.slickAdd = function(markup, index, addBefore) {

        var _ = this;

        if (typeof(index) === 'boolean') {
            addBefore = index;
            index = null;
        } else if (index < 0 || (index >= _.slideCount)) {
            return false;
        }

        _.unload();

        if (typeof(index) === 'number') {
            if (index === 0 && _.$slides.length === 0) {
                $(markup).appendTo(_.$slideTrack);
            } else if (addBefore) {
                $(markup).insertBefore(_.$slides.eq(index));
            } else {
                $(markup).insertAfter(_.$slides.eq(index));
            }
        } else {
            if (addBefore === true) {
                $(markup).prependTo(_.$slideTrack);
            } else {
                $(markup).appendTo(_.$slideTrack);
            }
        }

        _.$slides = _.$slideTrack.children(this.options.slide);

        _.$slideTrack.children(this.options.slide).detach();

        _.$slideTrack.append(_.$slides);

        _.$slides.each(function(index, element) {
            $(element).attr('data-slick-index', index);
        });

        _.$slidesCache = _.$slides;

        _.reinit();

    };

    Slick.prototype.animateHeight = function() {
        var _ = this;
        if (_.options.slidesToShow === 1 && _.options.adaptiveHeight === true && _.options.vertical === false) {
            var targetHeight = _.$slides.eq(_.currentSlide).outerHeight(true);
            _.$list.animate({
                height: targetHeight
            }, _.options.speed);
        }
    };

    Slick.prototype.animateSlide = function(targetLeft, callback) {

        var animProps = {},
            _ = this;

        _.animateHeight();

        if (_.options.rtl === true && _.options.vertical === false) {
            targetLeft = -targetLeft;
        }
        if (_.transformsEnabled === false) {
            if (_.options.vertical === false) {
                _.$slideTrack.animate({
                    left: targetLeft
                }, _.options.speed, _.options.easing, callback);
            } else {
                _.$slideTrack.animate({
                    top: targetLeft
                }, _.options.speed, _.options.easing, callback);
            }

        } else {

            if (_.cssTransitions === false) {
                if (_.options.rtl === true) {
                    _.currentLeft = -(_.currentLeft);
                }
                $({
                    animStart: _.currentLeft
                }).animate({
                    animStart: targetLeft
                }, {
                    duration: _.options.speed,
                    easing: _.options.easing,
                    step: function(now) {
                        now = Math.ceil(now);
                        if (_.options.vertical === false) {
                            animProps[_.animType] = 'translate(' +
                                now + 'px, 0px)';
                            _.$slideTrack.css(animProps);
                        } else {
                            animProps[_.animType] = 'translate(0px,' +
                                now + 'px)';
                            _.$slideTrack.css(animProps);
                        }
                    },
                    complete: function() {
                        if (callback) {
                            callback.call();
                        }
                    }
                });

            } else {

                _.applyTransition();
                targetLeft = Math.ceil(targetLeft);

                if (_.options.vertical === false) {
                    animProps[_.animType] = 'translate3d(' + targetLeft + 'px, 0px, 0px)';
                } else {
                    animProps[_.animType] = 'translate3d(0px,' + targetLeft + 'px, 0px)';
                }
                _.$slideTrack.css(animProps);

                if (callback) {
                    setTimeout(function() {

                        _.disableTransition();

                        callback.call();
                    }, _.options.speed);
                }

            }

        }

    };

    Slick.prototype.getNavTarget = function() {

        var _ = this,
            asNavFor = _.options.asNavFor;

        if ( asNavFor && asNavFor !== null ) {
            asNavFor = $(asNavFor).not(_.$slider);
        }

        return asNavFor;

    };

    Slick.prototype.asNavFor = function(index) {

        var _ = this,
            asNavFor = _.getNavTarget();

        if ( asNavFor !== null && typeof asNavFor === 'object' ) {
            asNavFor.each(function() {
                var target = $(this).slick('getSlick');
                if(!target.unslicked) {
                    target.slideHandler(index, true);
                }
            });
        }

    };

    Slick.prototype.applyTransition = function(slide) {

        var _ = this,
            transition = {};

        if (_.options.fade === false) {
            transition[_.transitionType] = _.transformType + ' ' + _.options.speed + 'ms ' + _.options.cssEase;
        } else {
            transition[_.transitionType] = 'opacity ' + _.options.speed + 'ms ' + _.options.cssEase;
        }

        if (_.options.fade === false) {
            _.$slideTrack.css(transition);
        } else {
            _.$slides.eq(slide).css(transition);
        }

    };

    Slick.prototype.autoPlay = function() {

        var _ = this;

        _.autoPlayClear();

        if ( _.slideCount > _.options.slidesToShow ) {
            _.autoPlayTimer = setInterval( _.autoPlayIterator, _.options.autoplaySpeed );
        }

    };

    Slick.prototype.autoPlayClear = function() {

        var _ = this;

        if (_.autoPlayTimer) {
            clearInterval(_.autoPlayTimer);
        }

    };

    Slick.prototype.autoPlayIterator = function() {

        var _ = this,
            slideTo = _.currentSlide + _.options.slidesToScroll;

        if ( !_.paused && !_.interrupted && !_.focussed ) {

            if ( _.options.infinite === false ) {

                if ( _.direction === 1 && ( _.currentSlide + 1 ) === ( _.slideCount - 1 )) {
                    _.direction = 0;
                }

                else if ( _.direction === 0 ) {

                    slideTo = _.currentSlide - _.options.slidesToScroll;

                    if ( _.currentSlide - 1 === 0 ) {
                        _.direction = 1;
                    }

                }

            }

            _.slideHandler( slideTo );

        }

    };

    Slick.prototype.buildArrows = function() {

        var _ = this;

        if (_.options.arrows === true ) {

            _.$prevArrow = $(_.options.prevArrow).addClass('slick-arrow');
            _.$nextArrow = $(_.options.nextArrow).addClass('slick-arrow');

            if( _.slideCount > _.options.slidesToShow ) {

                _.$prevArrow.removeClass('slick-hidden').removeAttr('aria-hidden tabindex');
                _.$nextArrow.removeClass('slick-hidden').removeAttr('aria-hidden tabindex');

                if (_.htmlExpr.test(_.options.prevArrow)) {
                    _.$prevArrow.prependTo(_.options.appendArrows);
                }

                if (_.htmlExpr.test(_.options.nextArrow)) {
                    _.$nextArrow.appendTo(_.options.appendArrows);
                }

                if (_.options.infinite !== true) {
                    _.$prevArrow
                        .addClass('slick-disabled')
                        .attr('aria-disabled', 'true');
                }

            } else {

                _.$prevArrow.add( _.$nextArrow )

                    .addClass('slick-hidden')
                    .attr({
                        'aria-disabled': 'true',
                        'tabindex': '-1'
                    });

            }

        }

    };

    Slick.prototype.buildDots = function() {

        var _ = this,
            i, dot;

        if (_.options.dots === true && _.slideCount > _.options.slidesToShow) {

            _.$slider.addClass('slick-dotted');

            dot = $('<ul />').addClass(_.options.dotsClass);

            for (i = 0; i <= _.getDotCount(); i += 1) {
                dot.append($('<li />').append(_.options.customPaging.call(this, _, i)));
            }

            _.$dots = dot.appendTo(_.options.appendDots);

            _.$dots.find('li').first().addClass('slick-active').attr('aria-hidden', 'false');

        }

    };

    Slick.prototype.buildOut = function() {

        var _ = this;

        _.$slides =
            _.$slider
                .children( _.options.slide + ':not(.slick-cloned)')
                .addClass('slick-slide');

        _.slideCount = _.$slides.length;

        _.$slides.each(function(index, element) {
            $(element)
                .attr('data-slick-index', index)
                .data('originalStyling', $(element).attr('style') || '');
        });

        _.$slider.addClass('slick-slider');

        _.$slideTrack = (_.slideCount === 0) ?
            $('<div class="slick-track"/>').appendTo(_.$slider) :
            _.$slides.wrapAll('<div class="slick-track"/>').parent();

        _.$list = _.$slideTrack.wrap(
            '<div aria-live="polite" class="slick-list"/>').parent();
        _.$slideTrack.css('opacity', 0);

        if (_.options.centerMode === true || _.options.swipeToSlide === true) {
            _.options.slidesToScroll = 1;
        }

        $('img[data-lazy]', _.$slider).not('[src]').addClass('slick-loading');

        _.setupInfinite();

        _.buildArrows();

        _.buildDots();

        _.updateDots();


        _.setSlideClasses(typeof _.currentSlide === 'number' ? _.currentSlide : 0);

        if (_.options.draggable === true) {
            _.$list.addClass('draggable');
        }

    };

    Slick.prototype.buildRows = function() {

        var _ = this, a, b, c, newSlides, numOfSlides, originalSlides,slidesPerSection;

        newSlides = document.createDocumentFragment();
        originalSlides = _.$slider.children();

        if(_.options.rows > 1) {

            slidesPerSection = _.options.slidesPerRow * _.options.rows;
            numOfSlides = Math.ceil(
                originalSlides.length / slidesPerSection
            );

            for(a = 0; a < numOfSlides; a++){
                var slide = document.createElement('div');
                for(b = 0; b < _.options.rows; b++) {
                    var row = document.createElement('div');
                    for(c = 0; c < _.options.slidesPerRow; c++) {
                        var target = (a * slidesPerSection + ((b * _.options.slidesPerRow) + c));
                        if (originalSlides.get(target)) {
                            row.appendChild(originalSlides.get(target));
                        }
                    }
                    slide.appendChild(row);
                }
                newSlides.appendChild(slide);
            }

            _.$slider.empty().append(newSlides);
            _.$slider.children().children().children()
                .css({
                    'width':(100 / _.options.slidesPerRow) + '%',
                    'display': 'inline-block'
                });

        }

    };

    Slick.prototype.checkResponsive = function(initial, forceUpdate) {

        var _ = this,
            breakpoint, targetBreakpoint, respondToWidth, triggerBreakpoint = false;
        var sliderWidth = _.$slider.width();
        var windowWidth = window.innerWidth || $(window).width();

        if (_.respondTo === 'window') {
            respondToWidth = windowWidth;
        } else if (_.respondTo === 'slider') {
            respondToWidth = sliderWidth;
        } else if (_.respondTo === 'min') {
            respondToWidth = Math.min(windowWidth, sliderWidth);
        }

        if ( _.options.responsive &&
            _.options.responsive.length &&
            _.options.responsive !== null) {

            targetBreakpoint = null;

            for (breakpoint in _.breakpoints) {
                if (_.breakpoints.hasOwnProperty(breakpoint)) {
                    if (_.originalSettings.mobileFirst === false) {
                        if (respondToWidth < _.breakpoints[breakpoint]) {
                            targetBreakpoint = _.breakpoints[breakpoint];
                        }
                    } else {
                        if (respondToWidth > _.breakpoints[breakpoint]) {
                            targetBreakpoint = _.breakpoints[breakpoint];
                        }
                    }
                }
            }

            if (targetBreakpoint !== null) {
                if (_.activeBreakpoint !== null) {
                    if (targetBreakpoint !== _.activeBreakpoint || forceUpdate) {
                        _.activeBreakpoint =
                            targetBreakpoint;
                        if (_.breakpointSettings[targetBreakpoint] === 'unslick') {
                            _.unslick(targetBreakpoint);
                        } else {
                            _.options = $.extend({}, _.originalSettings,
                                _.breakpointSettings[
                                    targetBreakpoint]);
                            if (initial === true) {
                                _.currentSlide = _.options.initialSlide;
                            }
                            _.refresh(initial);
                        }
                        triggerBreakpoint = targetBreakpoint;
                    }
                } else {
                    _.activeBreakpoint = targetBreakpoint;
                    if (_.breakpointSettings[targetBreakpoint] === 'unslick') {
                        _.unslick(targetBreakpoint);
                    } else {
                        _.options = $.extend({}, _.originalSettings,
                            _.breakpointSettings[
                                targetBreakpoint]);
                        if (initial === true) {
                            _.currentSlide = _.options.initialSlide;
                        }
                        _.refresh(initial);
                    }
                    triggerBreakpoint = targetBreakpoint;
                }
            } else {
                if (_.activeBreakpoint !== null) {
                    _.activeBreakpoint = null;
                    _.options = _.originalSettings;
                    if (initial === true) {
                        _.currentSlide = _.options.initialSlide;
                    }
                    _.refresh(initial);
                    triggerBreakpoint = targetBreakpoint;
                }
            }

            // only trigger breakpoints during an actual break. not on initialize.
            if( !initial && triggerBreakpoint !== false ) {
                _.$slider.trigger('breakpoint', [_, triggerBreakpoint]);
            }
        }

    };

    Slick.prototype.changeSlide = function(event, dontAnimate) {

        var _ = this,
            $target = $(event.currentTarget),
            indexOffset, slideOffset, unevenOffset;

        // If target is a link, prevent default action.
        if($target.is('a')) {
            event.preventDefault();
        }

        // If target is not the <li> element (ie: a child), find the <li>.
        if(!$target.is('li')) {
            $target = $target.closest('li');
        }

        unevenOffset = (_.slideCount % _.options.slidesToScroll !== 0);
        indexOffset = unevenOffset ? 0 : (_.slideCount - _.currentSlide) % _.options.slidesToScroll;

        switch (event.data.message) {

            case 'previous':
                slideOffset = indexOffset === 0 ? _.options.slidesToScroll : _.options.slidesToShow - indexOffset;
                if (_.slideCount > _.options.slidesToShow) {
                    _.slideHandler(_.currentSlide - slideOffset, false, dontAnimate);
                }
                break;

            case 'next':
                slideOffset = indexOffset === 0 ? _.options.slidesToScroll : indexOffset;
                if (_.slideCount > _.options.slidesToShow) {
                    _.slideHandler(_.currentSlide + slideOffset, false, dontAnimate);
                }
                break;

            case 'index':
                var index = event.data.index === 0 ? 0 :
                    event.data.index || $target.index() * _.options.slidesToScroll;

                _.slideHandler(_.checkNavigable(index), false, dontAnimate);
                $target.children().trigger('focus');
                break;

            default:
                return;
        }

    };

    Slick.prototype.checkNavigable = function(index) {

        var _ = this,
            navigables, prevNavigable;

        navigables = _.getNavigableIndexes();
        prevNavigable = 0;
        if (index > navigables[navigables.length - 1]) {
            index = navigables[navigables.length - 1];
        } else {
            for (var n in navigables) {
                if (index < navigables[n]) {
                    index = prevNavigable;
                    break;
                }
                prevNavigable = navigables[n];
            }
        }

        return index;
    };

    Slick.prototype.cleanUpEvents = function() {

        var _ = this;

        if (_.options.dots && _.$dots !== null) {

            $('li', _.$dots)
                .off('click.slick', _.changeSlide)
                .off('mouseenter.slick', $.proxy(_.interrupt, _, true))
                .off('mouseleave.slick', $.proxy(_.interrupt, _, false));

        }

        _.$slider.off('focus.slick blur.slick');

        if (_.options.arrows === true && _.slideCount > _.options.slidesToShow) {
            _.$prevArrow && _.$prevArrow.off('click.slick', _.changeSlide);
            _.$nextArrow && _.$nextArrow.off('click.slick', _.changeSlide);
        }

        _.$list.off('touchstart.slick mousedown.slick', _.swipeHandler);
        _.$list.off('touchmove.slick mousemove.slick', _.swipeHandler);
        _.$list.off('touchend.slick mouseup.slick', _.swipeHandler);
        _.$list.off('touchcancel.slick mouseleave.slick', _.swipeHandler);

        _.$list.off('click.slick', _.clickHandler);

        $(document).off(_.visibilityChange, _.visibility);

        _.cleanUpSlideEvents();

        if (_.options.accessibility === true) {
            _.$list.off('keydown.slick', _.keyHandler);
        }

        if (_.options.focusOnSelect === true) {
            $(_.$slideTrack).children().off('click.slick', _.selectHandler);
        }

        $(window).off('orientationchange.slick.slick-' + _.instanceUid, _.orientationChange);

        $(window).off('resize.slick.slick-' + _.instanceUid, _.resize);

        $('[draggable!=true]', _.$slideTrack).off('dragstart', _.preventDefault);

        $(window).off('load.slick.slick-' + _.instanceUid, _.setPosition);
        $(document).off('ready.slick.slick-' + _.instanceUid, _.setPosition);

    };

    Slick.prototype.cleanUpSlideEvents = function() {

        var _ = this;

        _.$list.off('mouseenter.slick', $.proxy(_.interrupt, _, true));
        _.$list.off('mouseleave.slick', $.proxy(_.interrupt, _, false));

    };

    Slick.prototype.cleanUpRows = function() {

        var _ = this, originalSlides;

        if(_.options.rows > 1) {
            originalSlides = _.$slides.children().children();
            originalSlides.removeAttr('style');
            _.$slider.empty().append(originalSlides);
        }

    };

    Slick.prototype.clickHandler = function(event) {

        var _ = this;

        if (_.shouldClick === false) {
            event.stopImmediatePropagation();
            event.stopPropagation();
            event.preventDefault();
        }

    };

    Slick.prototype.destroy = function(refresh) {

        var _ = this;

        _.autoPlayClear();

        _.touchObject = {};

        _.cleanUpEvents();

        $('.slick-cloned', _.$slider).detach();

        if (_.$dots) {
            _.$dots.remove();
        }


        if ( _.$prevArrow && _.$prevArrow.length ) {

            _.$prevArrow
                .removeClass('slick-disabled slick-arrow slick-hidden')
                .removeAttr('aria-hidden aria-disabled tabindex')
                .css('display','');

            if ( _.htmlExpr.test( _.options.prevArrow )) {
                _.$prevArrow.remove();
            }
        }

        if ( _.$nextArrow && _.$nextArrow.length ) {

            _.$nextArrow
                .removeClass('slick-disabled slick-arrow slick-hidden')
                .removeAttr('aria-hidden aria-disabled tabindex')
                .css('display','');

            if ( _.htmlExpr.test( _.options.nextArrow )) {
                _.$nextArrow.remove();
            }

        }


        if (_.$slides) {

            _.$slides
                .removeClass('slick-slide slick-active slick-center slick-visible slick-current')
                .removeAttr('aria-hidden')
                .removeAttr('data-slick-index')
                .each(function(){
                    $(this).attr('style', $(this).data('originalStyling'));
                });

            _.$slideTrack.children(this.options.slide).detach();

            _.$slideTrack.detach();

            _.$list.detach();

            _.$slider.append(_.$slides);
        }

        _.cleanUpRows();

        _.$slider.removeClass('slick-slider');
        _.$slider.removeClass('slick-initialized');
        _.$slider.removeClass('slick-dotted');

        _.unslicked = true;

        if(!refresh) {
            _.$slider.trigger('destroy', [_]);
        }

    };

    Slick.prototype.disableTransition = function(slide) {

        var _ = this,
            transition = {};

        transition[_.transitionType] = '';

        if (_.options.fade === false) {
            _.$slideTrack.css(transition);
        } else {
            _.$slides.eq(slide).css(transition);
        }

    };

    Slick.prototype.fadeSlide = function(slideIndex, callback) {

        var _ = this;

        if (_.cssTransitions === false) {

            _.$slides.eq(slideIndex).css({
                zIndex: _.options.zIndex
            });

            _.$slides.eq(slideIndex).animate({
                opacity: 1
            }, _.options.speed, _.options.easing, callback);

        } else {

            _.applyTransition(slideIndex);

            _.$slides.eq(slideIndex).css({
                opacity: 1,
                zIndex: _.options.zIndex
            });

            if (callback) {
                setTimeout(function() {

                    _.disableTransition(slideIndex);

                    callback.call();
                }, _.options.speed);
            }

        }

    };

    Slick.prototype.fadeSlideOut = function(slideIndex) {

        var _ = this;

        if (_.cssTransitions === false) {

            _.$slides.eq(slideIndex).animate({
                opacity: 0,
                zIndex: _.options.zIndex - 2
            }, _.options.speed, _.options.easing);

        } else {

            _.applyTransition(slideIndex);

            _.$slides.eq(slideIndex).css({
                opacity: 0,
                zIndex: _.options.zIndex - 2
            });

        }

    };

    Slick.prototype.filterSlides = Slick.prototype.slickFilter = function(filter) {

        var _ = this;

        if (filter !== null) {

            _.$slidesCache = _.$slides;

            _.unload();

            _.$slideTrack.children(this.options.slide).detach();

            _.$slidesCache.filter(filter).appendTo(_.$slideTrack);

            _.reinit();

        }

    };

    Slick.prototype.focusHandler = function() {

        var _ = this;

        _.$slider
            .off('focus.slick blur.slick')
            .on('focus.slick blur.slick',
                '*:not(.slick-arrow)', function(event) {

            event.stopImmediatePropagation();
            var $sf = $(this);

            setTimeout(function() {

                if( _.options.pauseOnFocus ) {
                    _.focussed = $sf.is(':focus');
                    _.autoPlay();
                }

            }, 0);

        });
    };

    Slick.prototype.getCurrent = Slick.prototype.slickCurrentSlide = function() {

        var _ = this;
        return _.currentSlide;

    };

    Slick.prototype.getDotCount = function() {

        var _ = this;

        var breakPoint = 0;
        var counter = 0;
        var pagerQty = 0;

        if (_.options.infinite === true) {
            while (breakPoint < _.slideCount) {
                ++pagerQty;
                breakPoint = counter + _.options.slidesToScroll;
                counter += _.options.slidesToScroll <= _.options.slidesToShow ? _.options.slidesToScroll : _.options.slidesToShow;
            }
        } else if (_.options.centerMode === true) {
            pagerQty = _.slideCount;
        } else if(!_.options.asNavFor) {
            pagerQty = 1 + Math.ceil((_.slideCount - _.options.slidesToShow) / _.options.slidesToScroll);
        }else {
            while (breakPoint < _.slideCount) {
                ++pagerQty;
                breakPoint = counter + _.options.slidesToScroll;
                counter += _.options.slidesToScroll <= _.options.slidesToShow ? _.options.slidesToScroll : _.options.slidesToShow;
            }
        }

        return pagerQty - 1;

    };

    Slick.prototype.getLeft = function(slideIndex) {

        var _ = this,
            targetLeft,
            verticalHeight,
            verticalOffset = 0,
            targetSlide;

        _.slideOffset = 0;
        verticalHeight = _.$slides.first().outerHeight(true);

        if (_.options.infinite === true) {
            if (_.slideCount > _.options.slidesToShow) {
                _.slideOffset = (_.slideWidth * _.options.slidesToShow) * -1;
                verticalOffset = (verticalHeight * _.options.slidesToShow) * -1;
            }
            if (_.slideCount % _.options.slidesToScroll !== 0) {
                if (slideIndex + _.options.slidesToScroll > _.slideCount && _.slideCount > _.options.slidesToShow) {
                    if (slideIndex > _.slideCount) {
                        _.slideOffset = ((_.options.slidesToShow - (slideIndex - _.slideCount)) * _.slideWidth) * -1;
                        verticalOffset = ((_.options.slidesToShow - (slideIndex - _.slideCount)) * verticalHeight) * -1;
                    } else {
                        _.slideOffset = ((_.slideCount % _.options.slidesToScroll) * _.slideWidth) * -1;
                        verticalOffset = ((_.slideCount % _.options.slidesToScroll) * verticalHeight) * -1;
                    }
                }
            }
        } else {
            if (slideIndex + _.options.slidesToShow > _.slideCount) {
                _.slideOffset = ((slideIndex + _.options.slidesToShow) - _.slideCount) * _.slideWidth;
                verticalOffset = ((slideIndex + _.options.slidesToShow) - _.slideCount) * verticalHeight;
            }
        }

        if (_.slideCount <= _.options.slidesToShow) {
            _.slideOffset = 0;
            verticalOffset = 0;
        }

        if (_.options.centerMode === true && _.options.infinite === true) {
            _.slideOffset += _.slideWidth * Math.floor(_.options.slidesToShow / 2) - _.slideWidth;
        } else if (_.options.centerMode === true) {
            _.slideOffset = 0;
            _.slideOffset += _.slideWidth * Math.floor(_.options.slidesToShow / 2);
        }

        if (_.options.vertical === false) {
            targetLeft = ((slideIndex * _.slideWidth) * -1) + _.slideOffset;
        } else {
            targetLeft = ((slideIndex * verticalHeight) * -1) + verticalOffset;
        }

        if (_.options.variableWidth === true) {

            if (_.slideCount <= _.options.slidesToShow || _.options.infinite === false) {
                targetSlide = _.$slideTrack.children('.slick-slide').eq(slideIndex);
            } else {
                targetSlide = _.$slideTrack.children('.slick-slide').eq(slideIndex + _.options.slidesToShow);
            }

            if (_.options.rtl === true) {
                if (targetSlide[0]) {
                    targetLeft = (_.$slideTrack.width() - targetSlide[0].offsetLeft - targetSlide.width()) * -1;
                } else {
                    targetLeft =  0;
                }
            } else {
                targetLeft = targetSlide[0] ? targetSlide[0].offsetLeft * -1 : 0;
            }

            if (_.options.centerMode === true) {
                if (_.slideCount <= _.options.slidesToShow || _.options.infinite === false) {
                    targetSlide = _.$slideTrack.children('.slick-slide').eq(slideIndex);
                } else {
                    targetSlide = _.$slideTrack.children('.slick-slide').eq(slideIndex + _.options.slidesToShow + 1);
                }

                if (_.options.rtl === true) {
                    if (targetSlide[0]) {
                        targetLeft = (_.$slideTrack.width() - targetSlide[0].offsetLeft - targetSlide.width()) * -1;
                    } else {
                        targetLeft =  0;
                    }
                } else {
                    targetLeft = targetSlide[0] ? targetSlide[0].offsetLeft * -1 : 0;
                }

                targetLeft += (_.$list.width() - targetSlide.outerWidth()) / 2;
            }
        }

        return targetLeft;

    };

    Slick.prototype.getOption = Slick.prototype.slickGetOption = function(option) {

        var _ = this;

        return _.options[option];

    };

    Slick.prototype.getNavigableIndexes = function() {

        var _ = this,
            breakPoint = 0,
            counter = 0,
            indexes = [],
            max;

        if (_.options.infinite === false) {
            max = _.slideCount;
        } else {
            breakPoint = _.options.slidesToScroll * -1;
            counter = _.options.slidesToScroll * -1;
            max = _.slideCount * 2;
        }

        while (breakPoint < max) {
            indexes.push(breakPoint);
            breakPoint = counter + _.options.slidesToScroll;
            counter += _.options.slidesToScroll <= _.options.slidesToShow ? _.options.slidesToScroll : _.options.slidesToShow;
        }

        return indexes;

    };

    Slick.prototype.getSlick = function() {

        return this;

    };

    Slick.prototype.getSlideCount = function() {

        var _ = this,
            slidesTraversed, swipedSlide, centerOffset;

        centerOffset = _.options.centerMode === true ? _.slideWidth * Math.floor(_.options.slidesToShow / 2) : 0;

        if (_.options.swipeToSlide === true) {
            _.$slideTrack.find('.slick-slide').each(function(index, slide) {
                if (slide.offsetLeft - centerOffset + ($(slide).outerWidth() / 2) > (_.swipeLeft * -1)) {
                    swipedSlide = slide;
                    return false;
                }
            });

            slidesTraversed = Math.abs($(swipedSlide).attr('data-slick-index') - _.currentSlide) || 1;

            return slidesTraversed;

        } else {
            return _.options.slidesToScroll;
        }

    };

    Slick.prototype.goTo = Slick.prototype.slickGoTo = function(slide, dontAnimate) {

        var _ = this;

        _.changeSlide({
            data: {
                message: 'index',
                index: parseInt(slide)
            }
        }, dontAnimate);

    };

    Slick.prototype.init = function(creation) {

        var _ = this;

        if (!$(_.$slider).hasClass('slick-initialized')) {

            $(_.$slider).addClass('slick-initialized');

            _.buildRows();
            _.buildOut();
            _.setProps();
            _.startLoad();
            _.loadSlider();
            _.initializeEvents();
            _.updateArrows();
            _.updateDots();
            _.checkResponsive(true);
            _.focusHandler();

        }

        if (creation) {
            _.$slider.trigger('init', [_]);
        }

        if (_.options.accessibility === true) {
            _.initADA();
        }

        if ( _.options.autoplay ) {

            _.paused = false;
            _.autoPlay();

        }

    };

    Slick.prototype.initADA = function() {
        var _ = this;
        _.$slides.add(_.$slideTrack.find('.slick-cloned')).attr({
            'aria-hidden': 'true',
            'tabindex': '-1'
        }).find('a, input, button, select').attr({
            'tabindex': '-1'
        });

        _.$slideTrack.attr('role', 'listbox');

        _.$slides.not(_.$slideTrack.find('.slick-cloned')).each(function(i) {
            $(this).attr({
                'role': 'option',
                'aria-describedby': 'slick-slide' + _.instanceUid + i + ''
            });
        });

        if (_.$dots !== null) {
            _.$dots.attr('role', 'tablist').find('li').each(function(i) {
                $(this).attr({
                    'role': 'presentation',
                    'aria-selected': 'false',
                    'aria-controls': 'navigation' + _.instanceUid + i + '',
                    'id': 'slick-slide' + _.instanceUid + i + ''
                });
            })
                .first().attr('aria-selected', 'true').end()
                .find('button').attr('role', 'button').end()
                .closest('div').attr('role', 'toolbar');
        }
        _.activateADA();

    };

    Slick.prototype.initArrowEvents = function() {

        var _ = this;

        if (_.options.arrows === true && _.slideCount > _.options.slidesToShow) {
            _.$prevArrow
               .off('click.slick')
               .on('click.slick', {
                    message: 'previous'
               }, _.changeSlide);
            _.$nextArrow
               .off('click.slick')
               .on('click.slick', {
                    message: 'next'
               }, _.changeSlide);
        }

    };

    Slick.prototype.initDotEvents = function() {

        var _ = this;

        if (_.options.dots === true && _.slideCount > _.options.slidesToShow) {
            $('li', _.$dots).on('click.slick', {
                message: 'index'
            }, _.changeSlide);
        }

        if ( _.options.dots === true && _.options.pauseOnDotsHover === true ) {

            $('li', _.$dots)
                .on('mouseenter.slick', $.proxy(_.interrupt, _, true))
                .on('mouseleave.slick', $.proxy(_.interrupt, _, false));

        }

    };

    Slick.prototype.initSlideEvents = function() {

        var _ = this;

        if ( _.options.pauseOnHover ) {

            _.$list.on('mouseenter.slick', $.proxy(_.interrupt, _, true));
            _.$list.on('mouseleave.slick', $.proxy(_.interrupt, _, false));

        }

    };

    Slick.prototype.initializeEvents = function() {

        var _ = this;

        _.initArrowEvents();

        _.initDotEvents();
        _.initSlideEvents();

        _.$list.on('touchstart.slick mousedown.slick', {
            action: 'start'
        }, _.swipeHandler);
        _.$list.on('touchmove.slick mousemove.slick', {
            action: 'move'
        }, _.swipeHandler);
        _.$list.on('touchend.slick mouseup.slick', {
            action: 'end'
        }, _.swipeHandler);
        _.$list.on('touchcancel.slick mouseleave.slick', {
            action: 'end'
        }, _.swipeHandler);

        _.$list.on('click.slick', _.clickHandler);

        $(document).on(_.visibilityChange, $.proxy(_.visibility, _));

        if (_.options.accessibility === true) {
            _.$list.on('keydown.slick', _.keyHandler);
        }

        if (_.options.focusOnSelect === true) {
            $(_.$slideTrack).children().on('click.slick', _.selectHandler);
        }

        $(window).on('orientationchange.slick.slick-' + _.instanceUid, $.proxy(_.orientationChange, _));

        $(window).on('resize.slick.slick-' + _.instanceUid, $.proxy(_.resize, _));

        $('[draggable!=true]', _.$slideTrack).on('dragstart', _.preventDefault);

        $(window).on('load.slick.slick-' + _.instanceUid, _.setPosition);
        $(document).on('ready.slick.slick-' + _.instanceUid, _.setPosition);

    };

    Slick.prototype.initUI = function() {

        var _ = this;

        if (_.options.arrows === true && _.slideCount > _.options.slidesToShow) {

            _.$prevArrow.show();
            _.$nextArrow.show();

        }

        if (_.options.dots === true && _.slideCount > _.options.slidesToShow) {

            _.$dots.show();

        }

    };

    Slick.prototype.keyHandler = function(event) {

        var _ = this;
         //Dont slide if the cursor is inside the form fields and arrow keys are pressed
        if(!event.target.tagName.match('TEXTAREA|INPUT|SELECT')) {
            if (event.keyCode === 37 && _.options.accessibility === true) {
                _.changeSlide({
                    data: {
                        message: _.options.rtl === true ? 'next' :  'previous'
                    }
                });
            } else if (event.keyCode === 39 && _.options.accessibility === true) {
                _.changeSlide({
                    data: {
                        message: _.options.rtl === true ? 'previous' : 'next'
                    }
                });
            }
        }

    };

    Slick.prototype.lazyLoad = function() {

        var _ = this,
            loadRange, cloneRange, rangeStart, rangeEnd;

        function loadImages(imagesScope) {

            $('img[data-lazy]', imagesScope).each(function() {

                var image = $(this),
                    imageSource = $(this).attr('data-lazy'),
                    imageToLoad = document.createElement('img');

                imageToLoad.onload = function() {

                    image
                        .animate({ opacity: 0 }, 100, function() {
                            image
                                .attr('src', imageSource)
                                .animate({ opacity: 1 }, 200, function() {
                                    image
                                        .removeAttr('data-lazy')
                                        .removeClass('slick-loading');
                                });
                            _.$slider.trigger('lazyLoaded', [_, image, imageSource]);
                        });

                };

                imageToLoad.onerror = function() {

                    image
                        .removeAttr( 'data-lazy' )
                        .removeClass( 'slick-loading' )
                        .addClass( 'slick-lazyload-error' );

                    _.$slider.trigger('lazyLoadError', [ _, image, imageSource ]);

                };

                imageToLoad.src = imageSource;

            });

        }

        if (_.options.centerMode === true) {
            if (_.options.infinite === true) {
                rangeStart = _.currentSlide + (_.options.slidesToShow / 2 + 1);
                rangeEnd = rangeStart + _.options.slidesToShow + 2;
            } else {
                rangeStart = Math.max(0, _.currentSlide - (_.options.slidesToShow / 2 + 1));
                rangeEnd = 2 + (_.options.slidesToShow / 2 + 1) + _.currentSlide;
            }
        } else {
            rangeStart = _.options.infinite ? _.options.slidesToShow + _.currentSlide : _.currentSlide;
            rangeEnd = Math.ceil(rangeStart + _.options.slidesToShow);
            if (_.options.fade === true) {
                if (rangeStart > 0) rangeStart--;
                if (rangeEnd <= _.slideCount) rangeEnd++;
            }
        }

        loadRange = _.$slider.find('.slick-slide').slice(rangeStart, rangeEnd);
        loadImages(loadRange);

        if (_.slideCount <= _.options.slidesToShow) {
            cloneRange = _.$slider.find('.slick-slide');
            loadImages(cloneRange);
        } else
        if (_.currentSlide >= _.slideCount - _.options.slidesToShow) {
            cloneRange = _.$slider.find('.slick-cloned').slice(0, _.options.slidesToShow);
            loadImages(cloneRange);
        } else if (_.currentSlide === 0) {
            cloneRange = _.$slider.find('.slick-cloned').slice(_.options.slidesToShow * -1);
            loadImages(cloneRange);
        }

    };

    Slick.prototype.loadSlider = function() {

        var _ = this;

        _.setPosition();

        _.$slideTrack.css({
            opacity: 1
        });

        _.$slider.removeClass('slick-loading');

        _.initUI();

        if (_.options.lazyLoad === 'progressive') {
            _.progressiveLazyLoad();
        }

    };

    Slick.prototype.next = Slick.prototype.slickNext = function() {

        var _ = this;

        _.changeSlide({
            data: {
                message: 'next'
            }
        });

    };

    Slick.prototype.orientationChange = function() {

        var _ = this;

        _.checkResponsive();
        _.setPosition();

    };

    Slick.prototype.pause = Slick.prototype.slickPause = function() {

        var _ = this;

        _.autoPlayClear();
        _.paused = true;

    };

    Slick.prototype.play = Slick.prototype.slickPlay = function() {

        var _ = this;

        _.autoPlay();
        _.options.autoplay = true;
        _.paused = false;
        _.focussed = false;
        _.interrupted = false;

    };

    Slick.prototype.postSlide = function(index) {

        var _ = this;

        if( !_.unslicked ) {

            _.$slider.trigger('afterChange', [_, index]);

            _.animating = false;

            _.setPosition();

            _.swipeLeft = null;

            if ( _.options.autoplay ) {
                _.autoPlay();
            }

            if (_.options.accessibility === true) {
                _.initADA();
            }

        }

    };

    Slick.prototype.prev = Slick.prototype.slickPrev = function() {

        var _ = this;

        _.changeSlide({
            data: {
                message: 'previous'
            }
        });

    };

    Slick.prototype.preventDefault = function(event) {

        event.preventDefault();

    };

    Slick.prototype.progressiveLazyLoad = function( tryCount ) {

        tryCount = tryCount || 1;

        var _ = this,
            $imgsToLoad = $( 'img[data-lazy]', _.$slider ),
            image,
            imageSource,
            imageToLoad;

        if ( $imgsToLoad.length ) {

            image = $imgsToLoad.first();
            imageSource = image.attr('data-lazy');
            imageToLoad = document.createElement('img');

            imageToLoad.onload = function() {

                image
                    .attr( 'src', imageSource )
                    .removeAttr('data-lazy')
                    .removeClass('slick-loading');

                if ( _.options.adaptiveHeight === true ) {
                    _.setPosition();
                }

                _.$slider.trigger('lazyLoaded', [ _, image, imageSource ]);
                _.progressiveLazyLoad();

            };

            imageToLoad.onerror = function() {

                if ( tryCount < 3 ) {

                    /**
                     * try to load the image 3 times,
                     * leave a slight delay so we don't get
                     * servers blocking the request.
                     */
                    setTimeout( function() {
                        _.progressiveLazyLoad( tryCount + 1 );
                    }, 500 );

                } else {

                    image
                        .removeAttr( 'data-lazy' )
                        .removeClass( 'slick-loading' )
                        .addClass( 'slick-lazyload-error' );

                    _.$slider.trigger('lazyLoadError', [ _, image, imageSource ]);

                    _.progressiveLazyLoad();

                }

            };

            imageToLoad.src = imageSource;

        } else {

            _.$slider.trigger('allImagesLoaded', [ _ ]);

        }

    };

    Slick.prototype.refresh = function( initializing ) {

        var _ = this, currentSlide, lastVisibleIndex;

        lastVisibleIndex = _.slideCount - _.options.slidesToShow;

        // in non-infinite sliders, we don't want to go past the
        // last visible index.
        if( !_.options.infinite && ( _.currentSlide > lastVisibleIndex )) {
            _.currentSlide = lastVisibleIndex;
        }

        // if less slides than to show, go to start.
        if ( _.slideCount <= _.options.slidesToShow ) {
            _.currentSlide = 0;

        }

        currentSlide = _.currentSlide;

        _.destroy(true);

        $.extend(_, _.initials, { currentSlide: currentSlide });

        _.init();

        if( !initializing ) {

            _.changeSlide({
                data: {
                    message: 'index',
                    index: currentSlide
                }
            }, false);

        }

    };

    Slick.prototype.registerBreakpoints = function() {

        var _ = this, breakpoint, currentBreakpoint, l,
            responsiveSettings = _.options.responsive || null;

        if ( $.type(responsiveSettings) === 'array' && responsiveSettings.length ) {

            _.respondTo = _.options.respondTo || 'window';

            for ( breakpoint in responsiveSettings ) {

                l = _.breakpoints.length-1;
                currentBreakpoint = responsiveSettings[breakpoint].breakpoint;

                if (responsiveSettings.hasOwnProperty(breakpoint)) {

                    // loop through the breakpoints and cut out any existing
                    // ones with the same breakpoint number, we don't want dupes.
                    while( l >= 0 ) {
                        if( _.breakpoints[l] && _.breakpoints[l] === currentBreakpoint ) {
                            _.breakpoints.splice(l,1);
                        }
                        l--;
                    }

                    _.breakpoints.push(currentBreakpoint);
                    _.breakpointSettings[currentBreakpoint] = responsiveSettings[breakpoint].settings;

                }

            }

            _.breakpoints.sort(function(a, b) {
                return ( _.options.mobileFirst ) ? a-b : b-a;
            });

        }

    };

    Slick.prototype.reinit = function() {

        var _ = this;

        _.$slides =
            _.$slideTrack
                .children(_.options.slide)
                .addClass('slick-slide');

        _.slideCount = _.$slides.length;

        if (_.currentSlide >= _.slideCount && _.currentSlide !== 0) {
            _.currentSlide = _.currentSlide - _.options.slidesToScroll;
        }

        if (_.slideCount <= _.options.slidesToShow) {
            _.currentSlide = 0;
        }

        _.registerBreakpoints();

        _.setProps();
        _.setupInfinite();
        _.buildArrows();
        _.updateArrows();
        _.initArrowEvents();
        _.buildDots();
        _.updateDots();
        _.initDotEvents();
        _.cleanUpSlideEvents();
        _.initSlideEvents();

        _.checkResponsive(false, true);

        if (_.options.focusOnSelect === true) {
            $(_.$slideTrack).children().on('click.slick', _.selectHandler);
        }

        _.setSlideClasses(typeof _.currentSlide === 'number' ? _.currentSlide : 0);

        _.setPosition();
        _.focusHandler();

        _.paused = !_.options.autoplay;
        _.autoPlay();

        _.$slider.trigger('reInit', [_]);

    };

    Slick.prototype.resize = function() {

        var _ = this;

        if ($(window).width() !== _.windowWidth) {
            clearTimeout(_.windowDelay);
            _.windowDelay = window.setTimeout(function() {
                _.windowWidth = $(window).width();
                _.checkResponsive();
                if( !_.unslicked ) { _.setPosition(); }
            }, 50);
        }
    };

    Slick.prototype.removeSlide = Slick.prototype.slickRemove = function(index, removeBefore, removeAll) {

        var _ = this;

        if (typeof(index) === 'boolean') {
            removeBefore = index;
            index = removeBefore === true ? 0 : _.slideCount - 1;
        } else {
            index = removeBefore === true ? --index : index;
        }

        if (_.slideCount < 1 || index < 0 || index > _.slideCount - 1) {
            return false;
        }

        _.unload();

        if (removeAll === true) {
            _.$slideTrack.children().remove();
        } else {
            _.$slideTrack.children(this.options.slide).eq(index).remove();
        }

        _.$slides = _.$slideTrack.children(this.options.slide);

        _.$slideTrack.children(this.options.slide).detach();

        _.$slideTrack.append(_.$slides);

        _.$slidesCache = _.$slides;

        _.reinit();

    };

    Slick.prototype.setCSS = function(position) {

        var _ = this,
            positionProps = {},
            x, y;

        if (_.options.rtl === true) {
            position = -position;
        }
        x = _.positionProp == 'left' ? Math.ceil(position) + 'px' : '0px';
        y = _.positionProp == 'top' ? Math.ceil(position) + 'px' : '0px';

        positionProps[_.positionProp] = position;

        if (_.transformsEnabled === false) {
            _.$slideTrack.css(positionProps);
        } else {
            positionProps = {};
            if (_.cssTransitions === false) {
                positionProps[_.animType] = 'translate(' + x + ', ' + y + ')';
                _.$slideTrack.css(positionProps);
            } else {
                positionProps[_.animType] = 'translate3d(' + x + ', ' + y + ', 0px)';
                _.$slideTrack.css(positionProps);
            }
        }

    };

    Slick.prototype.setDimensions = function() {

        var _ = this;

        if (_.options.vertical === false) {
            if (_.options.centerMode === true) {
                _.$list.css({
                    padding: ('0px ' + _.options.centerPadding)
                });
            }
        } else {
            _.$list.height(_.$slides.first().outerHeight(true) * _.options.slidesToShow);
            if (_.options.centerMode === true) {
                _.$list.css({
                    padding: (_.options.centerPadding + ' 0px')
                });
            }
        }

        _.listWidth = _.$list.width();
        _.listHeight = _.$list.height();


        if (_.options.vertical === false && _.options.variableWidth === false) {
            _.slideWidth = Math.ceil(_.listWidth / _.options.slidesToShow);
            _.$slideTrack.width(Math.ceil((_.slideWidth * _.$slideTrack.children('.slick-slide').length)));

        } else if (_.options.variableWidth === true) {
            _.$slideTrack.width(5000 * _.slideCount);
        } else {
            _.slideWidth = Math.ceil(_.listWidth);
            _.$slideTrack.height(Math.ceil((_.$slides.first().outerHeight(true) * _.$slideTrack.children('.slick-slide').length)));
        }

        var offset = _.$slides.first().outerWidth(true) - _.$slides.first().width();
        if (_.options.variableWidth === false) _.$slideTrack.children('.slick-slide').width(_.slideWidth - offset);

    };

    Slick.prototype.setFade = function() {

        var _ = this,
            targetLeft;

        _.$slides.each(function(index, element) {
            targetLeft = (_.slideWidth * index) * -1;
            if (_.options.rtl === true) {
                $(element).css({
                    position: 'relative',
                    right: targetLeft,
                    top: 0,
                    zIndex: _.options.zIndex - 2,
                    opacity: 0
                });
            } else {
                $(element).css({
                    position: 'relative',
                    left: targetLeft,
                    top: 0,
                    zIndex: _.options.zIndex - 2,
                    opacity: 0
                });
            }
        });

        _.$slides.eq(_.currentSlide).css({
            zIndex: _.options.zIndex - 1,
            opacity: 1
        });

    };

    Slick.prototype.setHeight = function() {

        var _ = this;

        if (_.options.slidesToShow === 1 && _.options.adaptiveHeight === true && _.options.vertical === false) {
            var targetHeight = _.$slides.eq(_.currentSlide).outerHeight(true);
            _.$list.css('height', targetHeight);
        }

    };

    Slick.prototype.setOption =
    Slick.prototype.slickSetOption = function() {

        /**
         * accepts arguments in format of:
         *
         *  - for changing a single option's value:
         *     .slick("setOption", option, value, refresh )
         *
         *  - for changing a set of responsive options:
         *     .slick("setOption", 'responsive', [{}, ...], refresh )
         *
         *  - for updating multiple values at once (not responsive)
         *     .slick("setOption", { 'option': value, ... }, refresh )
         */

        var _ = this, l, item, option, value, refresh = false, type;

        if( $.type( arguments[0] ) === 'object' ) {

            option =  arguments[0];
            refresh = arguments[1];
            type = 'multiple';

        } else if ( $.type( arguments[0] ) === 'string' ) {

            option =  arguments[0];
            value = arguments[1];
            refresh = arguments[2];

            if ( arguments[0] === 'responsive' && $.type( arguments[1] ) === 'array' ) {

                type = 'responsive';

            } else if ( typeof arguments[1] !== 'undefined' ) {

                type = 'single';

            }

        }

        if ( type === 'single' ) {

            _.options[option] = value;


        } else if ( type === 'multiple' ) {

            $.each( option , function( opt, val ) {

                _.options[opt] = val;

            });


        } else if ( type === 'responsive' ) {

            for ( item in value ) {

                if( $.type( _.options.responsive ) !== 'array' ) {

                    _.options.responsive = [ value[item] ];

                } else {

                    l = _.options.responsive.length-1;

                    // loop through the responsive object and splice out duplicates.
                    while( l >= 0 ) {

                        if( _.options.responsive[l].breakpoint === value[item].breakpoint ) {

                            _.options.responsive.splice(l,1);

                        }

                        l--;

                    }

                    _.options.responsive.push( value[item] );

                }

            }

        }

        if ( refresh ) {

            _.unload();
            _.reinit();

        }

    };

    Slick.prototype.setPosition = function() {

        var _ = this;

        _.setDimensions();

        _.setHeight();

        if (_.options.fade === false) {
            _.setCSS(_.getLeft(_.currentSlide));
        } else {
            _.setFade();
        }

        _.$slider.trigger('setPosition', [_]);

    };

    Slick.prototype.setProps = function() {

        var _ = this,
            bodyStyle = document.body.style;

        _.positionProp = _.options.vertical === true ? 'top' : 'left';

        if (_.positionProp === 'top') {
            _.$slider.addClass('slick-vertical');
        } else {
            _.$slider.removeClass('slick-vertical');
        }

        if (bodyStyle.WebkitTransition !== undefined ||
            bodyStyle.MozTransition !== undefined ||
            bodyStyle.msTransition !== undefined) {
            if (_.options.useCSS === true) {
                _.cssTransitions = true;
            }
        }

        if ( _.options.fade ) {
            if ( typeof _.options.zIndex === 'number' ) {
                if( _.options.zIndex < 3 ) {
                    _.options.zIndex = 3;
                }
            } else {
                _.options.zIndex = _.defaults.zIndex;
            }
        }

        if (bodyStyle.OTransform !== undefined) {
            _.animType = 'OTransform';
            _.transformType = '-o-transform';
            _.transitionType = 'OTransition';
            if (bodyStyle.perspectiveProperty === undefined && bodyStyle.webkitPerspective === undefined) _.animType = false;
        }
        if (bodyStyle.MozTransform !== undefined) {
            _.animType = 'MozTransform';
            _.transformType = '-moz-transform';
            _.transitionType = 'MozTransition';
            if (bodyStyle.perspectiveProperty === undefined && bodyStyle.MozPerspective === undefined) _.animType = false;
        }
        if (bodyStyle.webkitTransform !== undefined) {
            _.animType = 'webkitTransform';
            _.transformType = '-webkit-transform';
            _.transitionType = 'webkitTransition';
            if (bodyStyle.perspectiveProperty === undefined && bodyStyle.webkitPerspective === undefined) _.animType = false;
        }
        if (bodyStyle.msTransform !== undefined) {
            _.animType = 'msTransform';
            _.transformType = '-ms-transform';
            _.transitionType = 'msTransition';
            if (bodyStyle.msTransform === undefined) _.animType = false;
        }
        if (bodyStyle.transform !== undefined && _.animType !== false) {
            _.animType = 'transform';
            _.transformType = 'transform';
            _.transitionType = 'transition';
        }
        _.transformsEnabled = _.options.useTransform && (_.animType !== null && _.animType !== false);
    };


    Slick.prototype.setSlideClasses = function(index) {

        var _ = this,
            centerOffset, allSlides, indexOffset, remainder;

        allSlides = _.$slider
            .find('.slick-slide')
            .removeClass('slick-active slick-center slick-current')
            .attr('aria-hidden', 'true');

        _.$slides
            .eq(index)
            .addClass('slick-current');

        if (_.options.centerMode === true) {

            centerOffset = Math.floor(_.options.slidesToShow / 2);

            if (_.options.infinite === true) {

                if (index >= centerOffset && index <= (_.slideCount - 1) - centerOffset) {

                    _.$slides
                        .slice(index - centerOffset, index + centerOffset + 1)
                        .addClass('slick-active')
                        .attr('aria-hidden', 'false');

                } else {

                    indexOffset = _.options.slidesToShow + index;
                    allSlides
                        .slice(indexOffset - centerOffset + 1, indexOffset + centerOffset + 2)
                        .addClass('slick-active')
                        .attr('aria-hidden', 'false');

                }

                if (index === 0) {

                    allSlides
                        .eq(allSlides.length - 1 - _.options.slidesToShow)
                        .addClass('slick-center');

                } else if (index === _.slideCount - 1) {

                    allSlides
                        .eq(_.options.slidesToShow)
                        .addClass('slick-center');

                }

            }

            _.$slides
                .eq(index)
                .addClass('slick-center');

        } else {

            if (index >= 0 && index <= (_.slideCount - _.options.slidesToShow)) {

                _.$slides
                    .slice(index, index + _.options.slidesToShow)
                    .addClass('slick-active')
                    .attr('aria-hidden', 'false');

            } else if (allSlides.length <= _.options.slidesToShow) {

                allSlides
                    .addClass('slick-active')
                    .attr('aria-hidden', 'false');

            } else {

                remainder = _.slideCount % _.options.slidesToShow;
                indexOffset = _.options.infinite === true ? _.options.slidesToShow + index : index;

                if (_.options.slidesToShow == _.options.slidesToScroll && (_.slideCount - index) < _.options.slidesToShow) {

                    allSlides
                        .slice(indexOffset - (_.options.slidesToShow - remainder), indexOffset + remainder)
                        .addClass('slick-active')
                        .attr('aria-hidden', 'false');

                } else {

                    allSlides
                        .slice(indexOffset, indexOffset + _.options.slidesToShow)
                        .addClass('slick-active')
                        .attr('aria-hidden', 'false');

                }

            }

        }

        if (_.options.lazyLoad === 'ondemand') {
            _.lazyLoad();
        }

    };

    Slick.prototype.setupInfinite = function() {

        var _ = this,
            i, slideIndex, infiniteCount;

        if (_.options.fade === true) {
            _.options.centerMode = false;
        }

        if (_.options.infinite === true && _.options.fade === false) {

            slideIndex = null;

            if (_.slideCount > _.options.slidesToShow) {

                if (_.options.centerMode === true) {
                    infiniteCount = _.options.slidesToShow + 1;
                } else {
                    infiniteCount = _.options.slidesToShow;
                }

                for (i = _.slideCount; i > (_.slideCount -
                        infiniteCount); i -= 1) {
                    slideIndex = i - 1;
                    $(_.$slides[slideIndex]).clone(true).attr('id', '')
                        .attr('data-slick-index', slideIndex - _.slideCount)
                        .prependTo(_.$slideTrack).addClass('slick-cloned');
                }
                for (i = 0; i < infiniteCount; i += 1) {
                    slideIndex = i;
                    $(_.$slides[slideIndex]).clone(true).attr('id', '')
                        .attr('data-slick-index', slideIndex + _.slideCount)
                        .appendTo(_.$slideTrack).addClass('slick-cloned');
                }
                _.$slideTrack.find('.slick-cloned').find('[id]').each(function() {
                    $(this).attr('id', '');
                });

            }

        }

    };

    Slick.prototype.interrupt = function( toggle ) {

        var _ = this;

        if( !toggle ) {
            _.autoPlay();
        }
        _.interrupted = toggle;

    };

    Slick.prototype.selectHandler = function(event) {

        var _ = this;

        var targetElement =
            $(event.target).is('.slick-slide') ?
                $(event.target) :
                $(event.target).parents('.slick-slide');

        var index = parseInt(targetElement.attr('data-slick-index'));

        if (!index) index = 0;

        if (_.slideCount <= _.options.slidesToShow) {

            _.setSlideClasses(index);
            _.asNavFor(index);
            return;

        }

        _.slideHandler(index);

    };

    Slick.prototype.slideHandler = function(index, sync, dontAnimate) {

        var targetSlide, animSlide, oldSlide, slideLeft, targetLeft = null,
            _ = this, navTarget;

        sync = sync || false;

        if (_.animating === true && _.options.waitForAnimate === true) {
            return;
        }

        if (_.options.fade === true && _.currentSlide === index) {
            return;
        }

        if (_.slideCount <= _.options.slidesToShow) {
            return;
        }

        if (sync === false) {
            _.asNavFor(index);
        }

        targetSlide = index;
        targetLeft = _.getLeft(targetSlide);
        slideLeft = _.getLeft(_.currentSlide);

        _.currentLeft = _.swipeLeft === null ? slideLeft : _.swipeLeft;

        if (_.options.infinite === false && _.options.centerMode === false && (index < 0 || index > _.getDotCount() * _.options.slidesToScroll)) {
            if (_.options.fade === false) {
                targetSlide = _.currentSlide;
                if (dontAnimate !== true) {
                    _.animateSlide(slideLeft, function() {
                        _.postSlide(targetSlide);
                    });
                } else {
                    _.postSlide(targetSlide);
                }
            }
            return;
        } else if (_.options.infinite === false && _.options.centerMode === true && (index < 0 || index > (_.slideCount - _.options.slidesToScroll))) {
            if (_.options.fade === false) {
                targetSlide = _.currentSlide;
                if (dontAnimate !== true) {
                    _.animateSlide(slideLeft, function() {
                        _.postSlide(targetSlide);
                    });
                } else {
                    _.postSlide(targetSlide);
                }
            }
            return;
        }

        if ( _.options.autoplay ) {
            clearInterval(_.autoPlayTimer);
        }

        if (targetSlide < 0) {
            if (_.slideCount % _.options.slidesToScroll !== 0) {
                animSlide = _.slideCount - (_.slideCount % _.options.slidesToScroll);
            } else {
                animSlide = _.slideCount + targetSlide;
            }
        } else if (targetSlide >= _.slideCount) {
            if (_.slideCount % _.options.slidesToScroll !== 0) {
                animSlide = 0;
            } else {
                animSlide = targetSlide - _.slideCount;
            }
        } else {
            animSlide = targetSlide;
        }

        _.animating = true;

        _.$slider.trigger('beforeChange', [_, _.currentSlide, animSlide]);

        oldSlide = _.currentSlide;
        _.currentSlide = animSlide;

        _.setSlideClasses(_.currentSlide);

        if ( _.options.asNavFor ) {

            navTarget = _.getNavTarget();
            navTarget = navTarget.slick('getSlick');

            if ( navTarget.slideCount <= navTarget.options.slidesToShow ) {
                navTarget.setSlideClasses(_.currentSlide);
            }

        }

        _.updateDots();
        _.updateArrows();

        if (_.options.fade === true) {
            if (dontAnimate !== true) {

                _.fadeSlideOut(oldSlide);

                _.fadeSlide(animSlide, function() {
                    _.postSlide(animSlide);
                });

            } else {
                _.postSlide(animSlide);
            }
            _.animateHeight();
            return;
        }

        if (dontAnimate !== true) {
            _.animateSlide(targetLeft, function() {
                _.postSlide(animSlide);
            });
        } else {
            _.postSlide(animSlide);
        }

    };

    Slick.prototype.startLoad = function() {

        var _ = this;

        if (_.options.arrows === true && _.slideCount > _.options.slidesToShow) {

            _.$prevArrow.hide();
            _.$nextArrow.hide();

        }

        if (_.options.dots === true && _.slideCount > _.options.slidesToShow) {

            _.$dots.hide();

        }

        _.$slider.addClass('slick-loading');

    };

    Slick.prototype.swipeDirection = function() {

        var xDist, yDist, r, swipeAngle, _ = this;

        xDist = _.touchObject.startX - _.touchObject.curX;
        yDist = _.touchObject.startY - _.touchObject.curY;
        r = Math.atan2(yDist, xDist);

        swipeAngle = Math.round(r * 180 / Math.PI);
        if (swipeAngle < 0) {
            swipeAngle = 360 - Math.abs(swipeAngle);
        }

        if ((swipeAngle <= 45) && (swipeAngle >= 0)) {
            return (_.options.rtl === false ? 'left' : 'right');
        }
        if ((swipeAngle <= 360) && (swipeAngle >= 315)) {
            return (_.options.rtl === false ? 'left' : 'right');
        }
        if ((swipeAngle >= 135) && (swipeAngle <= 225)) {
            return (_.options.rtl === false ? 'right' : 'left');
        }
        if (_.options.verticalSwiping === true) {
            if ((swipeAngle >= 35) && (swipeAngle <= 135)) {
                return 'down';
            } else {
                return 'up';
            }
        }

        return 'vertical';

    };

    Slick.prototype.swipeEnd = function(event) {

        var _ = this,
            slideCount,
            direction;

        _.dragging = false;
        _.interrupted = false;
        _.shouldClick = ( _.touchObject.swipeLength > 10 ) ? false : true;

        if ( _.touchObject.curX === undefined ) {
            return false;
        }

        if ( _.touchObject.edgeHit === true ) {
            _.$slider.trigger('edge', [_, _.swipeDirection() ]);
        }

        if ( _.touchObject.swipeLength >= _.touchObject.minSwipe ) {

            direction = _.swipeDirection();

            switch ( direction ) {

                case 'left':
                case 'down':

                    slideCount =
                        _.options.swipeToSlide ?
                            _.checkNavigable( _.currentSlide + _.getSlideCount() ) :
                            _.currentSlide + _.getSlideCount();

                    _.currentDirection = 0;

                    break;

                case 'right':
                case 'up':

                    slideCount =
                        _.options.swipeToSlide ?
                            _.checkNavigable( _.currentSlide - _.getSlideCount() ) :
                            _.currentSlide - _.getSlideCount();

                    _.currentDirection = 1;

                    break;

                default:


            }

            if( direction != 'vertical' ) {

                _.slideHandler( slideCount );
                _.touchObject = {};
                _.$slider.trigger('swipe', [_, direction ]);

            }

        } else {

            if ( _.touchObject.startX !== _.touchObject.curX ) {

                _.slideHandler( _.currentSlide );
                _.touchObject = {};

            }

        }

    };

    Slick.prototype.swipeHandler = function(event) {

        var _ = this;

        if ((_.options.swipe === false) || ('ontouchend' in document && _.options.swipe === false)) {
            return;
        } else if (_.options.draggable === false && event.type.indexOf('mouse') !== -1) {
            return;
        }

        _.touchObject.fingerCount = event.originalEvent && event.originalEvent.touches !== undefined ?
            event.originalEvent.touches.length : 1;

        _.touchObject.minSwipe = _.listWidth / _.options
            .touchThreshold;

        if (_.options.verticalSwiping === true) {
            _.touchObject.minSwipe = _.listHeight / _.options
                .touchThreshold;
        }

        switch (event.data.action) {

            case 'start':
                _.swipeStart(event);
                break;

            case 'move':
                _.swipeMove(event);
                break;

            case 'end':
                _.swipeEnd(event);
                break;

        }

    };

    Slick.prototype.swipeMove = function(event) {

        var _ = this,
            edgeWasHit = false,
            curLeft, swipeDirection, swipeLength, positionOffset, touches;

        touches = event.originalEvent !== undefined ? event.originalEvent.touches : null;

        if (!_.dragging || touches && touches.length !== 1) {
            return false;
        }

        curLeft = _.getLeft(_.currentSlide);

        _.touchObject.curX = touches !== undefined ? touches[0].pageX : event.clientX;
        _.touchObject.curY = touches !== undefined ? touches[0].pageY : event.clientY;

        _.touchObject.swipeLength = Math.round(Math.sqrt(
            Math.pow(_.touchObject.curX - _.touchObject.startX, 2)));

        if (_.options.verticalSwiping === true) {
            _.touchObject.swipeLength = Math.round(Math.sqrt(
                Math.pow(_.touchObject.curY - _.touchObject.startY, 2)));
        }

        swipeDirection = _.swipeDirection();

        if (swipeDirection === 'vertical') {
            return;
        }

        if (event.originalEvent !== undefined && _.touchObject.swipeLength > 4) {
            event.preventDefault();
        }

        positionOffset = (_.options.rtl === false ? 1 : -1) * (_.touchObject.curX > _.touchObject.startX ? 1 : -1);
        if (_.options.verticalSwiping === true) {
            positionOffset = _.touchObject.curY > _.touchObject.startY ? 1 : -1;
        }


        swipeLength = _.touchObject.swipeLength;

        _.touchObject.edgeHit = false;

        if (_.options.infinite === false) {
            if ((_.currentSlide === 0 && swipeDirection === 'right') || (_.currentSlide >= _.getDotCount() && swipeDirection === 'left')) {
                swipeLength = _.touchObject.swipeLength * _.options.edgeFriction;
                _.touchObject.edgeHit = true;
            }
        }

        if (_.options.vertical === false) {
            _.swipeLeft = curLeft + swipeLength * positionOffset;
        } else {
            _.swipeLeft = curLeft + (swipeLength * (_.$list.height() / _.listWidth)) * positionOffset;
        }
        if (_.options.verticalSwiping === true) {
            _.swipeLeft = curLeft + swipeLength * positionOffset;
        }

        if (_.options.fade === true || _.options.touchMove === false) {
            return false;
        }

        if (_.animating === true) {
            _.swipeLeft = null;
            return false;
        }

        _.setCSS(_.swipeLeft);

    };

    Slick.prototype.swipeStart = function(event) {

        var _ = this,
            touches;

        _.interrupted = true;

        if (_.touchObject.fingerCount !== 1 || _.slideCount <= _.options.slidesToShow) {
            _.touchObject = {};
            return false;
        }

        if (event.originalEvent !== undefined && event.originalEvent.touches !== undefined) {
            touches = event.originalEvent.touches[0];
        }

        _.touchObject.startX = _.touchObject.curX = touches !== undefined ? touches.pageX : event.clientX;
        _.touchObject.startY = _.touchObject.curY = touches !== undefined ? touches.pageY : event.clientY;

        _.dragging = true;

    };

    Slick.prototype.unfilterSlides = Slick.prototype.slickUnfilter = function() {

        var _ = this;

        if (_.$slidesCache !== null) {

            _.unload();

            _.$slideTrack.children(this.options.slide).detach();

            _.$slidesCache.appendTo(_.$slideTrack);

            _.reinit();

        }

    };

    Slick.prototype.unload = function() {

        var _ = this;

        $('.slick-cloned', _.$slider).remove();

        if (_.$dots) {
            _.$dots.remove();
        }

        if (_.$prevArrow && _.htmlExpr.test(_.options.prevArrow)) {
            _.$prevArrow.remove();
        }

        if (_.$nextArrow && _.htmlExpr.test(_.options.nextArrow)) {
            _.$nextArrow.remove();
        }

        _.$slides
            .removeClass('slick-slide slick-active slick-visible slick-current')
            .attr('aria-hidden', 'true')
            .css('width', '');

    };

    Slick.prototype.unslick = function(fromBreakpoint) {

        var _ = this;
        _.$slider.trigger('unslick', [_, fromBreakpoint]);
        _.destroy();

    };

    Slick.prototype.updateArrows = function() {

        var _ = this,
            centerOffset;

        centerOffset = Math.floor(_.options.slidesToShow / 2);

        if ( _.options.arrows === true &&
            _.slideCount > _.options.slidesToShow &&
            !_.options.infinite ) {

            _.$prevArrow.removeClass('slick-disabled').attr('aria-disabled', 'false');
            _.$nextArrow.removeClass('slick-disabled').attr('aria-disabled', 'false');

            if (_.currentSlide === 0) {

                _.$prevArrow.addClass('slick-disabled').attr('aria-disabled', 'true');
                _.$nextArrow.removeClass('slick-disabled').attr('aria-disabled', 'false');

            } else if (_.currentSlide >= _.slideCount - _.options.slidesToShow && _.options.centerMode === false) {

                _.$nextArrow.addClass('slick-disabled').attr('aria-disabled', 'true');
                _.$prevArrow.removeClass('slick-disabled').attr('aria-disabled', 'false');

            } else if (_.currentSlide >= _.slideCount - 1 && _.options.centerMode === true) {

                _.$nextArrow.addClass('slick-disabled').attr('aria-disabled', 'true');
                _.$prevArrow.removeClass('slick-disabled').attr('aria-disabled', 'false');

            }

        }

    };

    Slick.prototype.updateDots = function() {

        var _ = this;

        if (_.$dots !== null) {

            _.$dots
                .find('li')
                .removeClass('slick-active')
                .attr('aria-hidden', 'true');

            _.$dots
                .find('li')
                .eq(Math.floor(_.currentSlide / _.options.slidesToScroll))
                .addClass('slick-active')
                .attr('aria-hidden', 'false');

        }

    };

    Slick.prototype.visibility = function() {

        var _ = this;

        if ( _.options.autoplay ) {

            if ( document[_.hidden] ) {

                _.interrupted = true;

            } else {

                _.interrupted = false;

            }

        }

    };

    $.fn.slick = function() {
        var _ = this,
            opt = arguments[0],
            args = Array.prototype.slice.call(arguments, 1),
            l = _.length,
            i,
            ret;
        for (i = 0; i < l; i++) {
            if (typeof opt == 'object' || typeof opt == 'undefined')
                _[i].slick = new Slick(_[i], opt);
            else
                ret = _[i].slick[opt].apply(_[i].slick, args);
            if (typeof ret != 'undefined') return ret;
        }
        return _;
    };

}));
/* XXXXXXXXXXXXXXX END OF SLICK JS HERE XXXXXXXXXXXXXXX */




/* ========================================================================
  =================== Custom Scroll JS HERE ============================
 * ======================================================================== */

/*
== malihu jquery custom scrollbar plugin == 
Version: 3.1.5 
Plugin URI: http://manos.malihu.gr/jquery-custom-content-scroller 
Author: malihu
Author URI: http://manos.malihu.gr
License: MIT License (MIT)
*/

/*
Copyright Manos Malihutsakis (email: manos@malihu.gr)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

/*
The code below is fairly long, fully commented and should be normally used in development. 
For production, use either the minified jquery.mCustomScrollbar.min.js script or 
the production-ready jquery.mCustomScrollbar.concat.min.js which contains the plugin 
and dependencies (minified). 
*/

(function(factory){
  if(typeof define==="function" && define.amd){
    define(["jquery"],factory);
  }else if(typeof module!=="undefined" && module.exports){
    module.exports=factory;
  }else{
    factory(jQuery,window,document);
  }
}(function($){
(function(init){
  var _rjs=typeof define==="function" && define.amd, /* RequireJS */
    _njs=typeof module !== "undefined" && module.exports, /* NodeJS */
    _dlp=("https:"==document.location.protocol) ? "https:" : "http:", /* location protocol */
    _url="cdnjs.cloudflare.com/ajax/libs/jquery-mousewheel/3.1.13/jquery.mousewheel.min.js";
  if(!_rjs){
    if(_njs){
      require("jquery-mousewheel")($);
    }else{
      /* load jquery-mousewheel plugin (via CDN) if it's not present or not loaded via RequireJS 
      (works when mCustomScrollbar fn is called on window load) */
      $.event.special.mousewheel || $("head").append(decodeURI("%3Cscript src="+_dlp+"//"+_url+"%3E%3C/script%3E"));
    }
  }
  init();
}(function(){
  
  /* 
  ----------------------------------------
  PLUGIN NAMESPACE, PREFIX, DEFAULT SELECTOR(S) 
  ----------------------------------------
  */
  
  var pluginNS="mCustomScrollbar",
    pluginPfx="mCS",
    defaultSelector=".mCustomScrollbar",
  
  
    
  
  
  /* 
  ----------------------------------------
  DEFAULT OPTIONS 
  ----------------------------------------
  */
  
    defaults={
      /*
      set element/content width/height programmatically 
      values: boolean, pixels, percentage 
        option            default
        -------------------------------------
        setWidth          false
        setHeight         false
      */
      /*
      set the initial css top property of content  
      values: string (e.g. "-100px", "10%" etc.)
      */
      setTop:0,
      /*
      set the initial css left property of content  
      values: string (e.g. "-100px", "10%" etc.)
      */
      setLeft:0,
      /* 
      scrollbar axis (vertical and/or horizontal scrollbars) 
      values (string): "y", "x", "yx"
      */
      axis:"y",
      /*
      position of scrollbar relative to content  
      values (string): "inside", "outside" ("outside" requires elements with position:relative)
      */
      scrollbarPosition:"inside",
      /*
      scrolling inertia
      values: integer (milliseconds)
      */
      scrollInertia:950,
      /* 
      auto-adjust scrollbar dragger length
      values: boolean
      */
      autoDraggerLength:true,
      /*
      auto-hide scrollbar when idle 
      values: boolean
        option            default
        -------------------------------------
        autoHideScrollbar     false
      */
      /*
      auto-expands scrollbar on mouse-over and dragging
      values: boolean
        option            default
        -------------------------------------
        autoExpandScrollbar     false
      */
      /*
      always show scrollbar, even when there's nothing to scroll 
      values: integer (0=disable, 1=always show dragger rail and buttons, 2=always show dragger rail, dragger and buttons), boolean
      */
      alwaysShowScrollbar:0,
      /*
      scrolling always snaps to a multiple of this number in pixels
      values: integer, array ([y,x])
        option            default
        -------------------------------------
        snapAmount          null
      */
      /*
      when snapping, snap with this number in pixels as an offset 
      values: integer
      */
      snapOffset:0,
      /* 
      mouse-wheel scrolling
      */
      mouseWheel:{
        /* 
        enable mouse-wheel scrolling
        values: boolean
        */
        enable:true,
        /* 
        scrolling amount in pixels
        values: "auto", integer 
        */
        scrollAmount:"auto",
        /* 
        mouse-wheel scrolling axis 
        the default scrolling direction when both vertical and horizontal scrollbars are present 
        values (string): "y", "x" 
        */
        axis:"y",
        /* 
        prevent the default behaviour which automatically scrolls the parent element(s) when end of scrolling is reached 
        values: boolean
          option            default
          -------------------------------------
          preventDefault        null
        */
        /*
        the reported mouse-wheel delta value. The number of lines (translated to pixels) one wheel notch scrolls.  
        values: "auto", integer 
        "auto" uses the default OS/browser value 
        */
        deltaFactor:"auto",
        /*
        normalize mouse-wheel delta to -1 or 1 (disables mouse-wheel acceleration) 
        values: boolean
          option            default
          -------------------------------------
          normalizeDelta        null
        */
        /*
        invert mouse-wheel scrolling direction 
        values: boolean
          option            default
          -------------------------------------
          invert            null
        */
        /*
        the tags that disable mouse-wheel when cursor is over them
        */
        disableOver:["select","option","keygen","datalist","textarea"]
      },
      /* 
      scrollbar buttons
      */
      scrollButtons:{ 
        /*
        enable scrollbar buttons
        values: boolean
          option            default
          -------------------------------------
          enable            null
        */
        /*
        scrollbar buttons scrolling type 
        values (string): "stepless", "stepped"
        */
        scrollType:"stepless",
        /*
        scrolling amount in pixels
        values: "auto", integer 
        */
        scrollAmount:"auto"
        /*
        tabindex of the scrollbar buttons
        values: false, integer
          option            default
          -------------------------------------
          tabindex          null
        */
      },
      /* 
      keyboard scrolling
      */
      keyboard:{ 
        /*
        enable scrolling via keyboard
        values: boolean
        */
        enable:true,
        /*
        keyboard scrolling type 
        values (string): "stepless", "stepped"
        */
        scrollType:"stepless",
        /*
        scrolling amount in pixels
        values: "auto", integer 
        */
        scrollAmount:"auto"
      },
      /*
      enable content touch-swipe scrolling 
      values: boolean, integer, string (number)
      integer values define the axis-specific minimum amount required for scrolling momentum
      */
      contentTouchScroll:25,
      /*
      enable/disable document (default) touch-swipe scrolling 
      */
      documentTouchScroll:true,
      /*
      advanced option parameters
      */
      advanced:{
        /*
        auto-expand content horizontally (for "x" or "yx" axis) 
        values: boolean, integer (the value 2 forces the non scrollHeight/scrollWidth method, the value 3 forces the scrollHeight/scrollWidth method)
          option            default
          -------------------------------------
          autoExpandHorizontalScroll  null
        */
        /*
        auto-scroll to elements with focus
        */
        autoScrollOnFocus:"input,textarea,select,button,datalist,keygen,a[tabindex],area,object,[contenteditable='true']",
        /*
        auto-update scrollbars on content, element or viewport resize 
        should be true for fluid layouts/elements, adding/removing content dynamically, hiding/showing elements, content with images etc. 
        values: boolean
        */
        updateOnContentResize:true,
        /*
        auto-update scrollbars each time each image inside the element is fully loaded 
        values: "auto", boolean
        */
        updateOnImageLoad:"auto",
        /*
        auto-update scrollbars based on the amount and size changes of specific selectors 
        useful when you need to update the scrollbar(s) automatically, each time a type of element is added, removed or changes its size 
        values: boolean, string (e.g. "ul li" will auto-update scrollbars each time list-items inside the element are changed) 
        a value of true (boolean) will auto-update scrollbars each time any element is changed
          option            default
          -------------------------------------
          updateOnSelectorChange    null
        */
        /*
        extra selectors that'll allow scrollbar dragging upon mousemove/up, pointermove/up, touchend etc. (e.g. "selector-1, selector-2")
          option            default
          -------------------------------------
          extraDraggableSelectors   null
        */
        /*
        extra selectors that'll release scrollbar dragging upon mouseup, pointerup, touchend etc. (e.g. "selector-1, selector-2")
          option            default
          -------------------------------------
          releaseDraggableSelectors null
        */
        /*
        auto-update timeout 
        values: integer (milliseconds)
        */
        autoUpdateTimeout:60
      },
      /* 
      scrollbar theme 
      values: string (see CSS/plugin URI for a list of ready-to-use themes)
      */
      theme:"light",
      /*
      user defined callback functions
      */
      callbacks:{
        /*
        Available callbacks: 
          callback          default
          -------------------------------------
          onCreate          null
          onInit            null
          onScrollStart       null
          onScroll          null
          onTotalScroll       null
          onTotalScrollBack     null
          whileScrolling        null
          onOverflowY         null
          onOverflowX         null
          onOverflowYNone       null
          onOverflowXNone       null
          onImageLoad         null
          onSelectorChange      null
          onBeforeUpdate        null
          onUpdate          null
        */
        onTotalScrollOffset:0,
        onTotalScrollBackOffset:0,
        alwaysTriggerOffsets:true
      }
      /*
      add scrollbar(s) on all elements matching the current selector, now and in the future 
      values: boolean, string 
      string values: "on" (enable), "once" (disable after first invocation), "off" (disable)
      liveSelector values: string (selector)
        option            default
        -------------------------------------
        live            false
        liveSelector        null
      */
    },
  
  
  
  
  
  /* 
  ----------------------------------------
  VARS, CONSTANTS 
  ----------------------------------------
  */
  
    totalInstances=0, /* plugin instances amount */
    liveTimers={}, /* live option timers */
    oldIE=(window.attachEvent && !window.addEventListener) ? 1 : 0, /* detect IE < 9 */
    touchActive=false,touchable, /* global touch vars (for touch and pointer events) */
    /* general plugin classes */
    classes=[
      "mCSB_dragger_onDrag","mCSB_scrollTools_onDrag","mCS_img_loaded","mCS_disabled","mCS_destroyed","mCS_no_scrollbar",
      "mCS-autoHide","mCS-dir-rtl","mCS_no_scrollbar_y","mCS_no_scrollbar_x","mCS_y_hidden","mCS_x_hidden","mCSB_draggerContainer",
      "mCSB_buttonUp","mCSB_buttonDown","mCSB_buttonLeft","mCSB_buttonRight"
    ],
    
  
  
  
  
  /* 
  ----------------------------------------
  METHODS 
  ----------------------------------------
  */
  
    methods={
      
      /* 
      plugin initialization method 
      creates the scrollbar(s), plugin data object and options
      ----------------------------------------
      */
      
      init:function(options){
        
        var options=$.extend(true,{},defaults,options),
          selector=_selector.call(this); /* validate selector */
        
        /* 
        if live option is enabled, monitor for elements matching the current selector and 
        apply scrollbar(s) when found (now and in the future) 
        */
        if(options.live){
          var liveSelector=options.liveSelector || this.selector || defaultSelector, /* live selector(s) */
            $liveSelector=$(liveSelector); /* live selector(s) as jquery object */
          if(options.live==="off"){
            /* 
            disable live if requested 
            usage: $(selector).mCustomScrollbar({live:"off"}); 
            */
            removeLiveTimers(liveSelector);
            return;
          }
          liveTimers[liveSelector]=setTimeout(function(){
            /* call mCustomScrollbar fn on live selector(s) every half-second */
            $liveSelector.mCustomScrollbar(options);
            if(options.live==="once" && $liveSelector.length){
              /* disable live after first invocation */
              removeLiveTimers(liveSelector);
            }
          },500);
        }else{
          removeLiveTimers(liveSelector);
        }
        
        /* options backward compatibility (for versions < 3.0.0) and normalization */
        options.setWidth=(options.set_width) ? options.set_width : options.setWidth;
        options.setHeight=(options.set_height) ? options.set_height : options.setHeight;
        options.axis=(options.horizontalScroll) ? "x" : _findAxis(options.axis);
        options.scrollInertia=options.scrollInertia>0 && options.scrollInertia<17 ? 17 : options.scrollInertia;
        if(typeof options.mouseWheel!=="object" &&  options.mouseWheel==true){ /* old school mouseWheel option (non-object) */
          options.mouseWheel={enable:true,scrollAmount:"auto",axis:"y",preventDefault:false,deltaFactor:"auto",normalizeDelta:false,invert:false}
        }
        options.mouseWheel.scrollAmount=!options.mouseWheelPixels ? options.mouseWheel.scrollAmount : options.mouseWheelPixels;
        options.mouseWheel.normalizeDelta=!options.advanced.normalizeMouseWheelDelta ? options.mouseWheel.normalizeDelta : options.advanced.normalizeMouseWheelDelta;
        options.scrollButtons.scrollType=_findScrollButtonsType(options.scrollButtons.scrollType); 
        
        _theme(options); /* theme-specific options */
        
        /* plugin constructor */
        return $(selector).each(function(){
          
          var $this=$(this);
          
          if(!$this.data(pluginPfx)){ /* prevent multiple instantiations */
          
            /* store options and create objects in jquery data */
            $this.data(pluginPfx,{
              idx:++totalInstances, /* instance index */
              opt:options, /* options */
              scrollRatio:{y:null,x:null}, /* scrollbar to content ratio */
              overflowed:null, /* overflowed axis */
              contentReset:{y:null,x:null}, /* object to check when content resets */
              bindEvents:false, /* object to check if events are bound */
              tweenRunning:false, /* object to check if tween is running */
              sequential:{}, /* sequential scrolling object */
              langDir:$this.css("direction"), /* detect/store direction (ltr or rtl) */
              cbOffsets:null, /* object to check whether callback offsets always trigger */
              /* 
              object to check how scrolling events where last triggered 
              "internal" (default - triggered by this script), "external" (triggered by other scripts, e.g. via scrollTo method) 
              usage: object.data("mCS").trigger
              */
              trigger:null,
              /* 
              object to check for changes in elements in order to call the update method automatically 
              */
              poll:{size:{o:0,n:0},img:{o:0,n:0},change:{o:0,n:0}}
            });
            
            var d=$this.data(pluginPfx),o=d.opt,
              /* HTML data attributes */
              htmlDataAxis=$this.data("mcs-axis"),htmlDataSbPos=$this.data("mcs-scrollbar-position"),htmlDataTheme=$this.data("mcs-theme");
             
            if(htmlDataAxis){o.axis=htmlDataAxis;} /* usage example: data-mcs-axis="y" */
            if(htmlDataSbPos){o.scrollbarPosition=htmlDataSbPos;} /* usage example: data-mcs-scrollbar-position="outside" */
            if(htmlDataTheme){ /* usage example: data-mcs-theme="minimal" */
              o.theme=htmlDataTheme;
              _theme(o); /* theme-specific options */
            }
            
            _pluginMarkup.call(this); /* add plugin markup */
            
            if(d && o.callbacks.onCreate && typeof o.callbacks.onCreate==="function"){o.callbacks.onCreate.call(this);} /* callbacks: onCreate */
            
            $("#mCSB_"+d.idx+"_container img:not(."+classes[2]+")").addClass(classes[2]); /* flag loaded images */
            
            methods.update.call(null,$this); /* call the update method */
          
          }
          
        });
        
      },
      /* ---------------------------------------- */
      
      
      
      /* 
      plugin update method 
      updates content and scrollbar(s) values, events and status 
      ----------------------------------------
      usage: $(selector).mCustomScrollbar("update");
      */
      
      update:function(el,cb){
        
        var selector=el || _selector.call(this); /* validate selector */
        
        return $(selector).each(function(){
          
          var $this=$(this);
          
          if($this.data(pluginPfx)){ /* check if plugin has initialized */
            
            var d=$this.data(pluginPfx),o=d.opt,
              mCSB_container=$("#mCSB_"+d.idx+"_container"),
              mCustomScrollBox=$("#mCSB_"+d.idx),
              mCSB_dragger=[$("#mCSB_"+d.idx+"_dragger_vertical"),$("#mCSB_"+d.idx+"_dragger_horizontal")];
            
            if(!mCSB_container.length){return;}
            
            if(d.tweenRunning){_stop($this);} /* stop any running tweens while updating */
            
            if(cb && d && o.callbacks.onBeforeUpdate && typeof o.callbacks.onBeforeUpdate==="function"){o.callbacks.onBeforeUpdate.call(this);} /* callbacks: onBeforeUpdate */
            
            /* if element was disabled or destroyed, remove class(es) */
            if($this.hasClass(classes[3])){$this.removeClass(classes[3]);}
            if($this.hasClass(classes[4])){$this.removeClass(classes[4]);}
            
            /* css flexbox fix, detect/set max-height */
            mCustomScrollBox.css("max-height","none");
            if(mCustomScrollBox.height()!==$this.height()){mCustomScrollBox.css("max-height",$this.height());}
            
            _expandContentHorizontally.call(this); /* expand content horizontally */
            
            if(o.axis!=="y" && !o.advanced.autoExpandHorizontalScroll){
              mCSB_container.css("width",_contentWidth(mCSB_container));
            }
            
            d.overflowed=_overflowed.call(this); /* determine if scrolling is required */
            
            _scrollbarVisibility.call(this); /* show/hide scrollbar(s) */
            
            /* auto-adjust scrollbar dragger length analogous to content */
            if(o.autoDraggerLength){_setDraggerLength.call(this);}
            
            _scrollRatio.call(this); /* calculate and store scrollbar to content ratio */
            
            _bindEvents.call(this); /* bind scrollbar events */
            
            /* reset scrolling position and/or events */
            var to=[Math.abs(mCSB_container[0].offsetTop),Math.abs(mCSB_container[0].offsetLeft)];
            if(o.axis!=="x"){ /* y/yx axis */
              if(!d.overflowed[0]){ /* y scrolling is not required */
                _resetContentPosition.call(this); /* reset content position */
                if(o.axis==="y"){
                  _unbindEvents.call(this);
                }else if(o.axis==="yx" && d.overflowed[1]){
                  _scrollTo($this,to[1].toString(),{dir:"x",dur:0,overwrite:"none"});
                }
              }else if(mCSB_dragger[0].height()>mCSB_dragger[0].parent().height()){
                _resetContentPosition.call(this); /* reset content position */
              }else{ /* y scrolling is required */
                _scrollTo($this,to[0].toString(),{dir:"y",dur:0,overwrite:"none"});
                d.contentReset.y=null;
              }
            }
            if(o.axis!=="y"){ /* x/yx axis */
              if(!d.overflowed[1]){ /* x scrolling is not required */
                _resetContentPosition.call(this); /* reset content position */
                if(o.axis==="x"){
                  _unbindEvents.call(this);
                }else if(o.axis==="yx" && d.overflowed[0]){
                  _scrollTo($this,to[0].toString(),{dir:"y",dur:0,overwrite:"none"});
                }
              }else if(mCSB_dragger[1].width()>mCSB_dragger[1].parent().width()){
                _resetContentPosition.call(this); /* reset content position */
              }else{ /* x scrolling is required */
                _scrollTo($this,to[1].toString(),{dir:"x",dur:0,overwrite:"none"});
                d.contentReset.x=null;
              }
            }
            
            /* callbacks: onImageLoad, onSelectorChange, onUpdate */
            if(cb && d){
              if(cb===2 && o.callbacks.onImageLoad && typeof o.callbacks.onImageLoad==="function"){
                o.callbacks.onImageLoad.call(this);
              }else if(cb===3 && o.callbacks.onSelectorChange && typeof o.callbacks.onSelectorChange==="function"){
                o.callbacks.onSelectorChange.call(this);
              }else if(o.callbacks.onUpdate && typeof o.callbacks.onUpdate==="function"){
                o.callbacks.onUpdate.call(this);
              }
            }
            
            _autoUpdate.call(this); /* initialize automatic updating (for dynamic content, fluid layouts etc.) */
            
          }
          
        });
        
      },
      /* ---------------------------------------- */
      
      
      
      /* 
      plugin scrollTo method 
      triggers a scrolling event to a specific value
      ----------------------------------------
      usage: $(selector).mCustomScrollbar("scrollTo",value,options);
      */
    
      scrollTo:function(val,options){
        
        /* prevent silly things like $(selector).mCustomScrollbar("scrollTo",undefined); */
        if(typeof val=="undefined" || val==null){return;}
        
        var selector=_selector.call(this); /* validate selector */
        
        return $(selector).each(function(){
          
          var $this=$(this);
          
          if($this.data(pluginPfx)){ /* check if plugin has initialized */
          
            var d=$this.data(pluginPfx),o=d.opt,
              /* method default options */
              methodDefaults={
                trigger:"external", /* method is by default triggered externally (e.g. from other scripts) */
                scrollInertia:o.scrollInertia, /* scrolling inertia (animation duration) */
                scrollEasing:"mcsEaseInOut", /* animation easing */
                moveDragger:false, /* move dragger instead of content */
                timeout:60, /* scroll-to delay */
                callbacks:true, /* enable/disable callbacks */
                onStart:true,
                onUpdate:true,
                onComplete:true
              },
              methodOptions=$.extend(true,{},methodDefaults,options),
              to=_arr.call(this,val),dur=methodOptions.scrollInertia>0 && methodOptions.scrollInertia<17 ? 17 : methodOptions.scrollInertia;
            
            /* translate yx values to actual scroll-to positions */
            to[0]=_to.call(this,to[0],"y");
            to[1]=_to.call(this,to[1],"x");
            
            /* 
            check if scroll-to value moves the dragger instead of content. 
            Only pixel values apply on dragger (e.g. 100, "100px", "-=100" etc.) 
            */
            if(methodOptions.moveDragger){
              to[0]*=d.scrollRatio.y;
              to[1]*=d.scrollRatio.x;
            }
            
            methodOptions.dur=_isTabHidden() ? 0 : dur; //skip animations if browser tab is hidden
            
            setTimeout(function(){ 
              /* do the scrolling */
              if(to[0]!==null && typeof to[0]!=="undefined" && o.axis!=="x" && d.overflowed[0]){ /* scroll y */
                methodOptions.dir="y";
                methodOptions.overwrite="all";
                _scrollTo($this,to[0].toString(),methodOptions);
              }
              if(to[1]!==null && typeof to[1]!=="undefined" && o.axis!=="y" && d.overflowed[1]){ /* scroll x */
                methodOptions.dir="x";
                methodOptions.overwrite="none";
                _scrollTo($this,to[1].toString(),methodOptions);
              }
            },methodOptions.timeout);
            
          }
          
        });
        
      },
      /* ---------------------------------------- */
      
      
      
      /*
      plugin stop method 
      stops scrolling animation
      ----------------------------------------
      usage: $(selector).mCustomScrollbar("stop");
      */
      stop:function(){
        
        var selector=_selector.call(this); /* validate selector */
        
        return $(selector).each(function(){
          
          var $this=$(this);
          
          if($this.data(pluginPfx)){ /* check if plugin has initialized */
                    
            _stop($this);
          
          }
          
        });
        
      },
      /* ---------------------------------------- */
      
      
      
      /*
      plugin disable method 
      temporarily disables the scrollbar(s) 
      ----------------------------------------
      usage: $(selector).mCustomScrollbar("disable",reset); 
      reset (boolean): resets content position to 0 
      */
      disable:function(r){
        
        var selector=_selector.call(this); /* validate selector */
        
        return $(selector).each(function(){
          
          var $this=$(this);
          
          if($this.data(pluginPfx)){ /* check if plugin has initialized */
            
            var d=$this.data(pluginPfx);
            
            _autoUpdate.call(this,"remove"); /* remove automatic updating */
            
            _unbindEvents.call(this); /* unbind events */
            
            if(r){_resetContentPosition.call(this);} /* reset content position */
            
            _scrollbarVisibility.call(this,true); /* show/hide scrollbar(s) */
            
            $this.addClass(classes[3]); /* add disable class */
          
          }
          
        });
        
      },
      /* ---------------------------------------- */
      
      
      
      /*
      plugin destroy method 
      completely removes the scrollbar(s) and returns the element to its original state
      ----------------------------------------
      usage: $(selector).mCustomScrollbar("destroy"); 
      */
      destroy:function(){
        
        var selector=_selector.call(this); /* validate selector */
        
        return $(selector).each(function(){
          
          var $this=$(this);
          
          if($this.data(pluginPfx)){ /* check if plugin has initialized */
          
            var d=$this.data(pluginPfx),o=d.opt,
              mCustomScrollBox=$("#mCSB_"+d.idx),
              mCSB_container=$("#mCSB_"+d.idx+"_container"),
              scrollbar=$(".mCSB_"+d.idx+"_scrollbar");
          
            if(o.live){removeLiveTimers(o.liveSelector || $(selector).selector);} /* remove live timers */
            
            _autoUpdate.call(this,"remove"); /* remove automatic updating */
            
            _unbindEvents.call(this); /* unbind events */
            
            _resetContentPosition.call(this); /* reset content position */
            
            $this.removeData(pluginPfx); /* remove plugin data object */
            
            _delete(this,"mcs"); /* delete callbacks object */
            
            /* remove plugin markup */
            scrollbar.remove(); /* remove scrollbar(s) first (those can be either inside or outside plugin's inner wrapper) */
            mCSB_container.find("img."+classes[2]).removeClass(classes[2]); /* remove loaded images flag */
            mCustomScrollBox.replaceWith(mCSB_container.contents()); /* replace plugin's inner wrapper with the original content */
            /* remove plugin classes from the element and add destroy class */
            $this.removeClass(pluginNS+" _"+pluginPfx+"_"+d.idx+" "+classes[6]+" "+classes[7]+" "+classes[5]+" "+classes[3]).addClass(classes[4]);
          
          }
          
        });
        
      }
      /* ---------------------------------------- */
      
    },
  
  
  
  
    
  /* 
  ----------------------------------------
  FUNCTIONS
  ----------------------------------------
  */
  
    /* validates selector (if selector is invalid or undefined uses the default one) */
    _selector=function(){
      return (typeof $(this)!=="object" || $(this).length<1) ? defaultSelector : this;
    },
    /* -------------------- */
    
    
    /* changes options according to theme */
    _theme=function(obj){
      var fixedSizeScrollbarThemes=["rounded","rounded-dark","rounded-dots","rounded-dots-dark"],
        nonExpandedScrollbarThemes=["rounded-dots","rounded-dots-dark","3d","3d-dark","3d-thick","3d-thick-dark","inset","inset-dark","inset-2","inset-2-dark","inset-3","inset-3-dark"],
        disabledScrollButtonsThemes=["minimal","minimal-dark"],
        enabledAutoHideScrollbarThemes=["minimal","minimal-dark"],
        scrollbarPositionOutsideThemes=["minimal","minimal-dark"];
      obj.autoDraggerLength=$.inArray(obj.theme,fixedSizeScrollbarThemes) > -1 ? false : obj.autoDraggerLength;
      obj.autoExpandScrollbar=$.inArray(obj.theme,nonExpandedScrollbarThemes) > -1 ? false : obj.autoExpandScrollbar;
      obj.scrollButtons.enable=$.inArray(obj.theme,disabledScrollButtonsThemes) > -1 ? false : obj.scrollButtons.enable;
      obj.autoHideScrollbar=$.inArray(obj.theme,enabledAutoHideScrollbarThemes) > -1 ? true : obj.autoHideScrollbar;
      obj.scrollbarPosition=$.inArray(obj.theme,scrollbarPositionOutsideThemes) > -1 ? "outside" : obj.scrollbarPosition;
    },
    /* -------------------- */
    
    
    /* live option timers removal */
    removeLiveTimers=function(selector){
      if(liveTimers[selector]){
        clearTimeout(liveTimers[selector]);
        _delete(liveTimers,selector);
      }
    },
    /* -------------------- */
    
    
    /* normalizes axis option to valid values: "y", "x", "yx" */
    _findAxis=function(val){
      return (val==="yx" || val==="xy" || val==="auto") ? "yx" : (val==="x" || val==="horizontal") ? "x" : "y";
    },
    /* -------------------- */
    
    
    /* normalizes scrollButtons.scrollType option to valid values: "stepless", "stepped" */
    _findScrollButtonsType=function(val){
      return (val==="stepped" || val==="pixels" || val==="step" || val==="click") ? "stepped" : "stepless";
    },
    /* -------------------- */
    
    
    /* generates plugin markup */
    _pluginMarkup=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        expandClass=o.autoExpandScrollbar ? " "+classes[1]+"_expand" : "",
        scrollbar=["<div id='mCSB_"+d.idx+"_scrollbar_vertical' class='mCSB_scrollTools mCSB_"+d.idx+"_scrollbar mCS-"+o.theme+" mCSB_scrollTools_vertical"+expandClass+"'><div class='"+classes[12]+"'><div id='mCSB_"+d.idx+"_dragger_vertical' class='mCSB_dragger' style='position:absolute;'><div class='mCSB_dragger_bar' /></div><div class='mCSB_draggerRail' /></div></div>","<div id='mCSB_"+d.idx+"_scrollbar_horizontal' class='mCSB_scrollTools mCSB_"+d.idx+"_scrollbar mCS-"+o.theme+" mCSB_scrollTools_horizontal"+expandClass+"'><div class='"+classes[12]+"'><div id='mCSB_"+d.idx+"_dragger_horizontal' class='mCSB_dragger' style='position:absolute;'><div class='mCSB_dragger_bar' /></div><div class='mCSB_draggerRail' /></div></div>"],
        wrapperClass=o.axis==="yx" ? "mCSB_vertical_horizontal" : o.axis==="x" ? "mCSB_horizontal" : "mCSB_vertical",
        scrollbars=o.axis==="yx" ? scrollbar[0]+scrollbar[1] : o.axis==="x" ? scrollbar[1] : scrollbar[0],
        contentWrapper=o.axis==="yx" ? "<div id='mCSB_"+d.idx+"_container_wrapper' class='mCSB_container_wrapper' />" : "",
        autoHideClass=o.autoHideScrollbar ? " "+classes[6] : "",
        scrollbarDirClass=(o.axis!=="x" && d.langDir==="rtl") ? " "+classes[7] : "";
      if(o.setWidth){$this.css("width",o.setWidth);} /* set element width */
      if(o.setHeight){$this.css("height",o.setHeight);} /* set element height */
      o.setLeft=(o.axis!=="y" && d.langDir==="rtl") ? "989999px" : o.setLeft; /* adjust left position for rtl direction */
      $this.addClass(pluginNS+" _"+pluginPfx+"_"+d.idx+autoHideClass+scrollbarDirClass).wrapInner("<div id='mCSB_"+d.idx+"' class='mCustomScrollBox mCS-"+o.theme+" "+wrapperClass+"'><div id='mCSB_"+d.idx+"_container' class='mCSB_container' style='position:relative; top:"+o.setTop+"; left:"+o.setLeft+";' dir='"+d.langDir+"' /></div>");
      var mCustomScrollBox=$("#mCSB_"+d.idx),
        mCSB_container=$("#mCSB_"+d.idx+"_container");
      if(o.axis!=="y" && !o.advanced.autoExpandHorizontalScroll){
        mCSB_container.css("width",_contentWidth(mCSB_container));
      }
      if(o.scrollbarPosition==="outside"){
        if($this.css("position")==="static"){ /* requires elements with non-static position */
          $this.css("position","relative");
        }
        $this.css("overflow","visible");
        mCustomScrollBox.addClass("mCSB_outside").after(scrollbars);
      }else{
        mCustomScrollBox.addClass("mCSB_inside").append(scrollbars);
        mCSB_container.wrap(contentWrapper);
      }
      _scrollButtons.call(this); /* add scrollbar buttons */
      /* minimum dragger length */
      var mCSB_dragger=[$("#mCSB_"+d.idx+"_dragger_vertical"),$("#mCSB_"+d.idx+"_dragger_horizontal")];
      mCSB_dragger[0].css("min-height",mCSB_dragger[0].height());
      mCSB_dragger[1].css("min-width",mCSB_dragger[1].width());
    },
    /* -------------------- */
    
    
    /* calculates content width */
    _contentWidth=function(el){
      var val=[el[0].scrollWidth,Math.max.apply(Math,el.children().map(function(){return $(this).outerWidth(true);}).get())],w=el.parent().width();
      return val[0]>w ? val[0] : val[1]>w ? val[1] : "100%";
    },
    /* -------------------- */
    
    
    /* expands content horizontally */
    _expandContentHorizontally=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        mCSB_container=$("#mCSB_"+d.idx+"_container");
      if(o.advanced.autoExpandHorizontalScroll && o.axis!=="y"){
        /* calculate scrollWidth */
        mCSB_container.css({"width":"auto","min-width":0,"overflow-x":"scroll"});
        var w=Math.ceil(mCSB_container[0].scrollWidth);
        if(o.advanced.autoExpandHorizontalScroll===3 || (o.advanced.autoExpandHorizontalScroll!==2 && w>mCSB_container.parent().width())){
          mCSB_container.css({"width":w,"min-width":"100%","overflow-x":"inherit"});
        }else{
          /* 
          wrap content with an infinite width div and set its position to absolute and width to auto. 
          Setting width to auto before calculating the actual width is important! 
          We must let the browser set the width as browser zoom values are impossible to calculate.
          */
          mCSB_container.css({"overflow-x":"inherit","position":"absolute"})
            .wrap("<div class='mCSB_h_wrapper' style='position:relative; left:0; width:999999px;' />")
            .css({ /* set actual width, original position and un-wrap */
              /* 
              get the exact width (with decimals) and then round-up. 
              Using jquery outerWidth() will round the width value which will mess up with inner elements that have non-integer width
              */
              "width":(Math.ceil(mCSB_container[0].getBoundingClientRect().right+0.4)-Math.floor(mCSB_container[0].getBoundingClientRect().left)),
              "min-width":"100%",
              "position":"relative"
            }).unwrap();
        }
      }
    },
    /* -------------------- */
    
    
    /* adds scrollbar buttons */
    _scrollButtons=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        mCSB_scrollTools=$(".mCSB_"+d.idx+"_scrollbar:first"),
        tabindex=!_isNumeric(o.scrollButtons.tabindex) ? "" : "tabindex='"+o.scrollButtons.tabindex+"'",
        btnHTML=[
          "<a href='#' class='"+classes[13]+"' "+tabindex+" />",
          "<a href='#' class='"+classes[14]+"' "+tabindex+" />",
          "<a href='#' class='"+classes[15]+"' "+tabindex+" />",
          "<a href='#' class='"+classes[16]+"' "+tabindex+" />"
        ],
        btn=[(o.axis==="x" ? btnHTML[2] : btnHTML[0]),(o.axis==="x" ? btnHTML[3] : btnHTML[1]),btnHTML[2],btnHTML[3]];
      if(o.scrollButtons.enable){
        mCSB_scrollTools.prepend(btn[0]).append(btn[1]).next(".mCSB_scrollTools").prepend(btn[2]).append(btn[3]);
      }
    },
    /* -------------------- */
    
    
    /* auto-adjusts scrollbar dragger length */
    _setDraggerLength=function(){
      var $this=$(this),d=$this.data(pluginPfx),
        mCustomScrollBox=$("#mCSB_"+d.idx),
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        mCSB_dragger=[$("#mCSB_"+d.idx+"_dragger_vertical"),$("#mCSB_"+d.idx+"_dragger_horizontal")],
        ratio=[mCustomScrollBox.height()/mCSB_container.outerHeight(false),mCustomScrollBox.width()/mCSB_container.outerWidth(false)],
        l=[
          parseInt(mCSB_dragger[0].css("min-height")),Math.round(ratio[0]*mCSB_dragger[0].parent().height()),
          parseInt(mCSB_dragger[1].css("min-width")),Math.round(ratio[1]*mCSB_dragger[1].parent().width())
        ],
        h=oldIE && (l[1]<l[0]) ? l[0] : l[1],w=oldIE && (l[3]<l[2]) ? l[2] : l[3];
      mCSB_dragger[0].css({
        "height":h,"max-height":(mCSB_dragger[0].parent().height()-10)
      }).find(".mCSB_dragger_bar").css({"line-height":l[0]+"px"});
      mCSB_dragger[1].css({
        "width":w,"max-width":(mCSB_dragger[1].parent().width()-10)
      });
    },
    /* -------------------- */
    
    
    /* calculates scrollbar to content ratio */
    _scrollRatio=function(){
      var $this=$(this),d=$this.data(pluginPfx),
        mCustomScrollBox=$("#mCSB_"+d.idx),
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        mCSB_dragger=[$("#mCSB_"+d.idx+"_dragger_vertical"),$("#mCSB_"+d.idx+"_dragger_horizontal")],
        scrollAmount=[mCSB_container.outerHeight(false)-mCustomScrollBox.height(),mCSB_container.outerWidth(false)-mCustomScrollBox.width()],
        ratio=[
          scrollAmount[0]/(mCSB_dragger[0].parent().height()-mCSB_dragger[0].height()),
          scrollAmount[1]/(mCSB_dragger[1].parent().width()-mCSB_dragger[1].width())
        ];
      d.scrollRatio={y:ratio[0],x:ratio[1]};
    },
    /* -------------------- */
    
    
    /* toggles scrolling classes */
    _onDragClasses=function(el,action,xpnd){
      var expandClass=xpnd ? classes[0]+"_expanded" : "",
        scrollbar=el.closest(".mCSB_scrollTools");
      if(action==="active"){
        el.toggleClass(classes[0]+" "+expandClass); scrollbar.toggleClass(classes[1]); 
        el[0]._draggable=el[0]._draggable ? 0 : 1;
      }else{
        if(!el[0]._draggable){
          if(action==="hide"){
            el.removeClass(classes[0]); scrollbar.removeClass(classes[1]);
          }else{
            el.addClass(classes[0]); scrollbar.addClass(classes[1]);
          }
        }
      }
    },
    /* -------------------- */
    
    
    /* checks if content overflows its container to determine if scrolling is required */
    _overflowed=function(){
      var $this=$(this),d=$this.data(pluginPfx),
        mCustomScrollBox=$("#mCSB_"+d.idx),
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        contentHeight=d.overflowed==null ? mCSB_container.height() : mCSB_container.outerHeight(false),
        contentWidth=d.overflowed==null ? mCSB_container.width() : mCSB_container.outerWidth(false),
        h=mCSB_container[0].scrollHeight,w=mCSB_container[0].scrollWidth;
      if(h>contentHeight){contentHeight=h;}
      if(w>contentWidth){contentWidth=w;}
      return [contentHeight>mCustomScrollBox.height(),contentWidth>mCustomScrollBox.width()];
    },
    /* -------------------- */
    
    
    /* resets content position to 0 */
    _resetContentPosition=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        mCustomScrollBox=$("#mCSB_"+d.idx),
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        mCSB_dragger=[$("#mCSB_"+d.idx+"_dragger_vertical"),$("#mCSB_"+d.idx+"_dragger_horizontal")];
      _stop($this); /* stop any current scrolling before resetting */
      if((o.axis!=="x" && !d.overflowed[0]) || (o.axis==="y" && d.overflowed[0])){ /* reset y */
        mCSB_dragger[0].add(mCSB_container).css("top",0);
        _scrollTo($this,"_resetY");
      }
      if((o.axis!=="y" && !d.overflowed[1]) || (o.axis==="x" && d.overflowed[1])){ /* reset x */
        var cx=dx=0;
        if(d.langDir==="rtl"){ /* adjust left position for rtl direction */
          cx=mCustomScrollBox.width()-mCSB_container.outerWidth(false);
          dx=Math.abs(cx/d.scrollRatio.x);
        }
        mCSB_container.css("left",cx);
        mCSB_dragger[1].css("left",dx);
        _scrollTo($this,"_resetX");
      }
    },
    /* -------------------- */
    
    
    /* binds scrollbar events */
    _bindEvents=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt;
      if(!d.bindEvents){ /* check if events are already bound */
        _draggable.call(this);
        if(o.contentTouchScroll){_contentDraggable.call(this);}
        _selectable.call(this);
        if(o.mouseWheel.enable){ /* bind mousewheel fn when plugin is available */
          function _mwt(){
            mousewheelTimeout=setTimeout(function(){
              if(!$.event.special.mousewheel){
                _mwt();
              }else{
                clearTimeout(mousewheelTimeout);
                _mousewheel.call($this[0]);
              }
            },100);
          }
          var mousewheelTimeout;
          _mwt();
        }
        _draggerRail.call(this);
        _wrapperScroll.call(this);
        if(o.advanced.autoScrollOnFocus){_focus.call(this);}
        if(o.scrollButtons.enable){_buttons.call(this);}
        if(o.keyboard.enable){_keyboard.call(this);}
        d.bindEvents=true;
      }
    },
    /* -------------------- */
    
    
    /* unbinds scrollbar events */
    _unbindEvents=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        namespace=pluginPfx+"_"+d.idx,
        sb=".mCSB_"+d.idx+"_scrollbar",
        sel=$("#mCSB_"+d.idx+",#mCSB_"+d.idx+"_container,#mCSB_"+d.idx+"_container_wrapper,"+sb+" ."+classes[12]+",#mCSB_"+d.idx+"_dragger_vertical,#mCSB_"+d.idx+"_dragger_horizontal,"+sb+">a"),
        mCSB_container=$("#mCSB_"+d.idx+"_container");
      if(o.advanced.releaseDraggableSelectors){sel.add($(o.advanced.releaseDraggableSelectors));}
      if(o.advanced.extraDraggableSelectors){sel.add($(o.advanced.extraDraggableSelectors));}
      if(d.bindEvents){ /* check if events are bound */
        /* unbind namespaced events from document/selectors */
        $(document).add($(!_canAccessIFrame() || top.document)).unbind("."+namespace);
        sel.each(function(){
          $(this).unbind("."+namespace);
        });
        /* clear and delete timeouts/objects */
        clearTimeout($this[0]._focusTimeout); _delete($this[0],"_focusTimeout");
        clearTimeout(d.sequential.step); _delete(d.sequential,"step");
        clearTimeout(mCSB_container[0].onCompleteTimeout); _delete(mCSB_container[0],"onCompleteTimeout");
        d.bindEvents=false;
      }
    },
    /* -------------------- */
    
    
    /* toggles scrollbar visibility */
    _scrollbarVisibility=function(disabled){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        contentWrapper=$("#mCSB_"+d.idx+"_container_wrapper"),
        content=contentWrapper.length ? contentWrapper : $("#mCSB_"+d.idx+"_container"),
        scrollbar=[$("#mCSB_"+d.idx+"_scrollbar_vertical"),$("#mCSB_"+d.idx+"_scrollbar_horizontal")],
        mCSB_dragger=[scrollbar[0].find(".mCSB_dragger"),scrollbar[1].find(".mCSB_dragger")];
      if(o.axis!=="x"){
        if(d.overflowed[0] && !disabled){
          scrollbar[0].add(mCSB_dragger[0]).add(scrollbar[0].children("a")).css("display","block");
          content.removeClass(classes[8]+" "+classes[10]);
        }else{
          if(o.alwaysShowScrollbar){
            if(o.alwaysShowScrollbar!==2){mCSB_dragger[0].css("display","none");}
            content.removeClass(classes[10]);
          }else{
            scrollbar[0].css("display","none");
            content.addClass(classes[10]);
          }
          content.addClass(classes[8]);
        }
      }
      if(o.axis!=="y"){
        if(d.overflowed[1] && !disabled){
          scrollbar[1].add(mCSB_dragger[1]).add(scrollbar[1].children("a")).css("display","block");
          content.removeClass(classes[9]+" "+classes[11]);
        }else{
          if(o.alwaysShowScrollbar){
            if(o.alwaysShowScrollbar!==2){mCSB_dragger[1].css("display","none");}
            content.removeClass(classes[11]);
          }else{
            scrollbar[1].css("display","none");
            content.addClass(classes[11]);
          }
          content.addClass(classes[9]);
        }
      }
      if(!d.overflowed[0] && !d.overflowed[1]){
        $this.addClass(classes[5]);
      }else{
        $this.removeClass(classes[5]);
      }
    },
    /* -------------------- */
    
    
    /* returns input coordinates of pointer, touch and mouse events (relative to document) */
    _coordinates=function(e){
      var t=e.type,o=e.target.ownerDocument!==document && frameElement!==null ? [$(frameElement).offset().top,$(frameElement).offset().left] : null,
        io=_canAccessIFrame() && e.target.ownerDocument!==top.document && frameElement!==null ? [$(e.view.frameElement).offset().top,$(e.view.frameElement).offset().left] : [0,0];
      switch(t){
        case "pointerdown": case "MSPointerDown": case "pointermove": case "MSPointerMove": case "pointerup": case "MSPointerUp":
          return o ? [e.originalEvent.pageY-o[0]+io[0],e.originalEvent.pageX-o[1]+io[1],false] : [e.originalEvent.pageY,e.originalEvent.pageX,false];
          break;
        case "touchstart": case "touchmove": case "touchend":
          var touch=e.originalEvent.touches[0] || e.originalEvent.changedTouches[0],
            touches=e.originalEvent.touches.length || e.originalEvent.changedTouches.length;
          return e.target.ownerDocument!==document ? [touch.screenY,touch.screenX,touches>1] : [touch.pageY,touch.pageX,touches>1];
          break;
        default:
          return o ? [e.pageY-o[0]+io[0],e.pageX-o[1]+io[1],false] : [e.pageY,e.pageX,false];
      }
    },
    /* -------------------- */
    
    
    /* 
    SCROLLBAR DRAG EVENTS
    scrolls content via scrollbar dragging 
    */
    _draggable=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        namespace=pluginPfx+"_"+d.idx,
        draggerId=["mCSB_"+d.idx+"_dragger_vertical","mCSB_"+d.idx+"_dragger_horizontal"],
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        mCSB_dragger=$("#"+draggerId[0]+",#"+draggerId[1]),
        draggable,dragY,dragX,
        rds=o.advanced.releaseDraggableSelectors ? mCSB_dragger.add($(o.advanced.releaseDraggableSelectors)) : mCSB_dragger,
        eds=o.advanced.extraDraggableSelectors ? $(!_canAccessIFrame() || top.document).add($(o.advanced.extraDraggableSelectors)) : $(!_canAccessIFrame() || top.document);
      mCSB_dragger.bind("contextmenu."+namespace,function(e){
        e.preventDefault(); //prevent right click
      }).bind("mousedown."+namespace+" touchstart."+namespace+" pointerdown."+namespace+" MSPointerDown."+namespace,function(e){
        e.stopImmediatePropagation();
        e.preventDefault();
        if(!_mouseBtnLeft(e)){return;} /* left mouse button only */
        touchActive=true;
        if(oldIE){document.onselectstart=function(){return false;}} /* disable text selection for IE < 9 */
        _iframe.call(mCSB_container,false); /* enable scrollbar dragging over iframes by disabling their events */
        _stop($this);
        draggable=$(this);
        var offset=draggable.offset(),y=_coordinates(e)[0]-offset.top,x=_coordinates(e)[1]-offset.left,
          h=draggable.height()+offset.top,w=draggable.width()+offset.left;
        if(y<h && y>0 && x<w && x>0){
          dragY=y; 
          dragX=x;
        }
        _onDragClasses(draggable,"active",o.autoExpandScrollbar); 
      }).bind("touchmove."+namespace,function(e){
        e.stopImmediatePropagation();
        e.preventDefault();
        var offset=draggable.offset(),y=_coordinates(e)[0]-offset.top,x=_coordinates(e)[1]-offset.left;
        _drag(dragY,dragX,y,x);
      });
      $(document).add(eds).bind("mousemove."+namespace+" pointermove."+namespace+" MSPointerMove."+namespace,function(e){
        if(draggable){
          var offset=draggable.offset(),y=_coordinates(e)[0]-offset.top,x=_coordinates(e)[1]-offset.left;
          if(dragY===y && dragX===x){return;} /* has it really moved? */
          _drag(dragY,dragX,y,x);
        }
      }).add(rds).bind("mouseup."+namespace+" touchend."+namespace+" pointerup."+namespace+" MSPointerUp."+namespace,function(e){
        if(draggable){
          _onDragClasses(draggable,"active",o.autoExpandScrollbar); 
          draggable=null;
        }
        touchActive=false;
        if(oldIE){document.onselectstart=null;} /* enable text selection for IE < 9 */
        _iframe.call(mCSB_container,true); /* enable iframes events */
      });
      function _drag(dragY,dragX,y,x){
        mCSB_container[0].idleTimer=o.scrollInertia<233 ? 250 : 0;
        if(draggable.attr("id")===draggerId[1]){
          var dir="x",to=((draggable[0].offsetLeft-dragX)+x)*d.scrollRatio.x;
        }else{
          var dir="y",to=((draggable[0].offsetTop-dragY)+y)*d.scrollRatio.y;
        }
        _scrollTo($this,to.toString(),{dir:dir,drag:true});
      }
    },
    /* -------------------- */
    
    
    /* 
    TOUCH SWIPE EVENTS
    scrolls content via touch swipe 
    Emulates the native touch-swipe scrolling with momentum found in iOS, Android and WP devices 
    */
    _contentDraggable=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        namespace=pluginPfx+"_"+d.idx,
        mCustomScrollBox=$("#mCSB_"+d.idx),
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        mCSB_dragger=[$("#mCSB_"+d.idx+"_dragger_vertical"),$("#mCSB_"+d.idx+"_dragger_horizontal")],
        draggable,dragY,dragX,touchStartY,touchStartX,touchMoveY=[],touchMoveX=[],startTime,runningTime,endTime,distance,speed,amount,
        durA=0,durB,overwrite=o.axis==="yx" ? "none" : "all",touchIntent=[],touchDrag,docDrag,
        iframe=mCSB_container.find("iframe"),
        events=[
          "touchstart."+namespace+" pointerdown."+namespace+" MSPointerDown."+namespace, //start
          "touchmove."+namespace+" pointermove."+namespace+" MSPointerMove."+namespace, //move
          "touchend."+namespace+" pointerup."+namespace+" MSPointerUp."+namespace //end
        ],
        touchAction=document.body.style.touchAction!==undefined && document.body.style.touchAction!=="";
      mCSB_container.bind(events[0],function(e){
        _onTouchstart(e);
      }).bind(events[1],function(e){
        _onTouchmove(e);
      });
      mCustomScrollBox.bind(events[0],function(e){
        _onTouchstart2(e);
      }).bind(events[2],function(e){
        _onTouchend(e);
      });
      if(iframe.length){
        iframe.each(function(){
          $(this).bind("load",function(){
            /* bind events on accessible iframes */
            if(_canAccessIFrame(this)){
              $(this.contentDocument || this.contentWindow.document).bind(events[0],function(e){
                _onTouchstart(e);
                _onTouchstart2(e);
              }).bind(events[1],function(e){
                _onTouchmove(e);
              }).bind(events[2],function(e){
                _onTouchend(e);
              });
            }
          });
        });
      }
      function _onTouchstart(e){
        if(!_pointerTouch(e) || touchActive || _coordinates(e)[2]){touchable=0; return;}
        touchable=1; touchDrag=0; docDrag=0; draggable=1;
        $this.removeClass("mCS_touch_action");
        var offset=mCSB_container.offset();
        dragY=_coordinates(e)[0]-offset.top;
        dragX=_coordinates(e)[1]-offset.left;
        touchIntent=[_coordinates(e)[0],_coordinates(e)[1]];
      }
      function _onTouchmove(e){
        if(!_pointerTouch(e) || touchActive || _coordinates(e)[2]){return;}
        if(!o.documentTouchScroll){e.preventDefault();} 
        e.stopImmediatePropagation();
        if(docDrag && !touchDrag){return;}
        if(draggable){
          runningTime=_getTime();
          var offset=mCustomScrollBox.offset(),y=_coordinates(e)[0]-offset.top,x=_coordinates(e)[1]-offset.left,
            easing="mcsLinearOut";
          touchMoveY.push(y);
          touchMoveX.push(x);
          touchIntent[2]=Math.abs(_coordinates(e)[0]-touchIntent[0]); touchIntent[3]=Math.abs(_coordinates(e)[1]-touchIntent[1]);
          if(d.overflowed[0]){
            var limit=mCSB_dragger[0].parent().height()-mCSB_dragger[0].height(),
              prevent=((dragY-y)>0 && (y-dragY)>-(limit*d.scrollRatio.y) && (touchIntent[3]*2<touchIntent[2] || o.axis==="yx"));
          }
          if(d.overflowed[1]){
            var limitX=mCSB_dragger[1].parent().width()-mCSB_dragger[1].width(),
              preventX=((dragX-x)>0 && (x-dragX)>-(limitX*d.scrollRatio.x) && (touchIntent[2]*2<touchIntent[3] || o.axis==="yx"));
          }
          if(prevent || preventX){ /* prevent native document scrolling */
            if(!touchAction){e.preventDefault();} 
            touchDrag=1;
          }else{
            docDrag=1;
            $this.addClass("mCS_touch_action");
          }
          if(touchAction){e.preventDefault();} 
          amount=o.axis==="yx" ? [(dragY-y),(dragX-x)] : o.axis==="x" ? [null,(dragX-x)] : [(dragY-y),null];
          mCSB_container[0].idleTimer=250;
          if(d.overflowed[0]){_drag(amount[0],durA,easing,"y","all",true);}
          if(d.overflowed[1]){_drag(amount[1],durA,easing,"x",overwrite,true);}
        }
      }
      function _onTouchstart2(e){
        if(!_pointerTouch(e) || touchActive || _coordinates(e)[2]){touchable=0; return;}
        touchable=1;
        e.stopImmediatePropagation();
        _stop($this);
        startTime=_getTime();
        var offset=mCustomScrollBox.offset();
        touchStartY=_coordinates(e)[0]-offset.top;
        touchStartX=_coordinates(e)[1]-offset.left;
        touchMoveY=[]; touchMoveX=[];
      }
      function _onTouchend(e){
        if(!_pointerTouch(e) || touchActive || _coordinates(e)[2]){return;}
        draggable=0;
        e.stopImmediatePropagation();
        touchDrag=0; docDrag=0;
        endTime=_getTime();
        var offset=mCustomScrollBox.offset(),y=_coordinates(e)[0]-offset.top,x=_coordinates(e)[1]-offset.left;
        if((endTime-runningTime)>30){return;}
        speed=1000/(endTime-startTime);
        var easing="mcsEaseOut",slow=speed<2.5,
          diff=slow ? [touchMoveY[touchMoveY.length-2],touchMoveX[touchMoveX.length-2]] : [0,0];
        distance=slow ? [(y-diff[0]),(x-diff[1])] : [y-touchStartY,x-touchStartX];
        var absDistance=[Math.abs(distance[0]),Math.abs(distance[1])];
        speed=slow ? [Math.abs(distance[0]/4),Math.abs(distance[1]/4)] : [speed,speed];
        var a=[
          Math.abs(mCSB_container[0].offsetTop)-(distance[0]*_m((absDistance[0]/speed[0]),speed[0])),
          Math.abs(mCSB_container[0].offsetLeft)-(distance[1]*_m((absDistance[1]/speed[1]),speed[1]))
        ];
        amount=o.axis==="yx" ? [a[0],a[1]] : o.axis==="x" ? [null,a[1]] : [a[0],null];
        durB=[(absDistance[0]*4)+o.scrollInertia,(absDistance[1]*4)+o.scrollInertia];
        var md=parseInt(o.contentTouchScroll) || 0; /* absolute minimum distance required */
        amount[0]=absDistance[0]>md ? amount[0] : 0;
        amount[1]=absDistance[1]>md ? amount[1] : 0;
        if(d.overflowed[0]){_drag(amount[0],durB[0],easing,"y",overwrite,false);}
        if(d.overflowed[1]){_drag(amount[1],durB[1],easing,"x",overwrite,false);}
      }
      function _m(ds,s){
        var r=[s*1.5,s*2,s/1.5,s/2];
        if(ds>90){
          return s>4 ? r[0] : r[3];
        }else if(ds>60){
          return s>3 ? r[3] : r[2];
        }else if(ds>30){
          return s>8 ? r[1] : s>6 ? r[0] : s>4 ? s : r[2];
        }else{
          return s>8 ? s : r[3];
        }
      }
      function _drag(amount,dur,easing,dir,overwrite,drag){
        if(!amount){return;}
        _scrollTo($this,amount.toString(),{dur:dur,scrollEasing:easing,dir:dir,overwrite:overwrite,drag:drag});
      }
    },
    /* -------------------- */
    
    
    /* 
    SELECT TEXT EVENTS 
    scrolls content when text is selected 
    */
    _selectable=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,seq=d.sequential,
        namespace=pluginPfx+"_"+d.idx,
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        wrapper=mCSB_container.parent(),
        action;
      mCSB_container.bind("mousedown."+namespace,function(e){
        if(touchable){return;}
        if(!action){action=1; touchActive=true;}
      }).add(document).bind("mousemove."+namespace,function(e){
        if(!touchable && action && _sel()){
          var offset=mCSB_container.offset(),
            y=_coordinates(e)[0]-offset.top+mCSB_container[0].offsetTop,x=_coordinates(e)[1]-offset.left+mCSB_container[0].offsetLeft;
          if(y>0 && y<wrapper.height() && x>0 && x<wrapper.width()){
            if(seq.step){_seq("off",null,"stepped");}
          }else{
            if(o.axis!=="x" && d.overflowed[0]){
              if(y<0){
                _seq("on",38);
              }else if(y>wrapper.height()){
                _seq("on",40);
              }
            }
            if(o.axis!=="y" && d.overflowed[1]){
              if(x<0){
                _seq("on",37);
              }else if(x>wrapper.width()){
                _seq("on",39);
              }
            }
          }
        }
      }).bind("mouseup."+namespace+" dragend."+namespace,function(e){
        if(touchable){return;}
        if(action){action=0; _seq("off",null);}
        touchActive=false;
      });
      function _sel(){
        return  window.getSelection ? window.getSelection().toString() : 
            document.selection && document.selection.type!="Control" ? document.selection.createRange().text : 0;
      }
      function _seq(a,c,s){
        seq.type=s && action ? "stepped" : "stepless";
        seq.scrollAmount=10;
        _sequentialScroll($this,a,c,"mcsLinearOut",s ? 60 : null);
      }
    },
    /* -------------------- */
    
    
    /* 
    MOUSE WHEEL EVENT
    scrolls content via mouse-wheel 
    via mouse-wheel plugin (https://github.com/brandonaaron/jquery-mousewheel)
    */
    _mousewheel=function(){
      if(!$(this).data(pluginPfx)){return;} /* Check if the scrollbar is ready to use mousewheel events (issue: #185) */
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        namespace=pluginPfx+"_"+d.idx,
        mCustomScrollBox=$("#mCSB_"+d.idx),
        mCSB_dragger=[$("#mCSB_"+d.idx+"_dragger_vertical"),$("#mCSB_"+d.idx+"_dragger_horizontal")],
        iframe=$("#mCSB_"+d.idx+"_container").find("iframe");
      if(iframe.length){
        iframe.each(function(){
          $(this).bind("load",function(){
            /* bind events on accessible iframes */
            if(_canAccessIFrame(this)){
              $(this.contentDocument || this.contentWindow.document).bind("mousewheel."+namespace,function(e,delta){
                _onMousewheel(e,delta);
              });
            }
          });
        });
      }
      mCustomScrollBox.bind("mousewheel."+namespace,function(e,delta){
        _onMousewheel(e,delta);
      });
      function _onMousewheel(e,delta){
        _stop($this);
        if(_disableMousewheel($this,e.target)){return;} /* disables mouse-wheel when hovering specific elements */
        var deltaFactor=o.mouseWheel.deltaFactor!=="auto" ? parseInt(o.mouseWheel.deltaFactor) : (oldIE && e.deltaFactor<100) ? 100 : e.deltaFactor || 100,
          dur=o.scrollInertia;
        if(o.axis==="x" || o.mouseWheel.axis==="x"){
          var dir="x",
            px=[Math.round(deltaFactor*d.scrollRatio.x),parseInt(o.mouseWheel.scrollAmount)],
            amount=o.mouseWheel.scrollAmount!=="auto" ? px[1] : px[0]>=mCustomScrollBox.width() ? mCustomScrollBox.width()*0.9 : px[0],
            contentPos=Math.abs($("#mCSB_"+d.idx+"_container")[0].offsetLeft),
            draggerPos=mCSB_dragger[1][0].offsetLeft,
            limit=mCSB_dragger[1].parent().width()-mCSB_dragger[1].width(),
            dlt=o.mouseWheel.axis==="y" ? (e.deltaY || delta) : e.deltaX;
        }else{
          var dir="y",
            px=[Math.round(deltaFactor*d.scrollRatio.y),parseInt(o.mouseWheel.scrollAmount)],
            amount=o.mouseWheel.scrollAmount!=="auto" ? px[1] : px[0]>=mCustomScrollBox.height() ? mCustomScrollBox.height()*0.9 : px[0],
            contentPos=Math.abs($("#mCSB_"+d.idx+"_container")[0].offsetTop),
            draggerPos=mCSB_dragger[0][0].offsetTop,
            limit=mCSB_dragger[0].parent().height()-mCSB_dragger[0].height(),
            dlt=e.deltaY || delta;
        }
        if((dir==="y" && !d.overflowed[0]) || (dir==="x" && !d.overflowed[1])){return;}
        if(o.mouseWheel.invert || e.webkitDirectionInvertedFromDevice){dlt=-dlt;}
        if(o.mouseWheel.normalizeDelta){dlt=dlt<0 ? -1 : 1;}
        if((dlt>0 && draggerPos!==0) || (dlt<0 && draggerPos!==limit) || o.mouseWheel.preventDefault){
          e.stopImmediatePropagation();
          e.preventDefault();
        }
        if(e.deltaFactor<5 && !o.mouseWheel.normalizeDelta){
          //very low deltaFactor values mean some kind of delta acceleration (e.g. osx trackpad), so adjusting scrolling accordingly
          amount=e.deltaFactor; dur=17;
        }
        _scrollTo($this,(contentPos-(dlt*amount)).toString(),{dir:dir,dur:dur});
      }
    },
    /* -------------------- */
    
    
    /* checks if iframe can be accessed */
    _canAccessIFrameCache=new Object(),
    _canAccessIFrame=function(iframe){
        var result=false,cacheKey=false,html=null;
        if(iframe===undefined){
        cacheKey="#empty";
        }else if($(iframe).attr("id")!==undefined){
        cacheKey=$(iframe).attr("id");
        }
      if(cacheKey!==false && _canAccessIFrameCache[cacheKey]!==undefined){
        return _canAccessIFrameCache[cacheKey];
      }
      if(!iframe){
        try{
          var doc=top.document;
          html=doc.body.innerHTML;
        }catch(err){/* do nothing */}
        result=(html!==null);
      }else{
        try{
          var doc=iframe.contentDocument || iframe.contentWindow.document;
          html=doc.body.innerHTML;
        }catch(err){/* do nothing */}
        result=(html!==null);
      }
      if(cacheKey!==false){_canAccessIFrameCache[cacheKey]=result;}
      return result;
    },
    /* -------------------- */
    
    
    /* switches iframe's pointer-events property (drag, mousewheel etc. over cross-domain iframes) */
    _iframe=function(evt){
      var el=this.find("iframe");
      if(!el.length){return;} /* check if content contains iframes */
      var val=!evt ? "none" : "auto";
      el.css("pointer-events",val); /* for IE11, iframe's display property should not be "block" */
    },
    /* -------------------- */
    
    
    /* disables mouse-wheel when hovering specific elements like select, datalist etc. */
    _disableMousewheel=function(el,target){
      var tag=target.nodeName.toLowerCase(),
        tags=el.data(pluginPfx).opt.mouseWheel.disableOver,
        /* elements that require focus */
        focusTags=["select","textarea"];
      return $.inArray(tag,tags) > -1 && !($.inArray(tag,focusTags) > -1 && !$(target).is(":focus"));
    },
    /* -------------------- */
    
    
    /* 
    DRAGGER RAIL CLICK EVENT
    scrolls content via dragger rail 
    */
    _draggerRail=function(){
      var $this=$(this),d=$this.data(pluginPfx),
        namespace=pluginPfx+"_"+d.idx,
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        wrapper=mCSB_container.parent(),
        mCSB_draggerContainer=$(".mCSB_"+d.idx+"_scrollbar ."+classes[12]),
        clickable;
      mCSB_draggerContainer.bind("mousedown."+namespace+" touchstart."+namespace+" pointerdown."+namespace+" MSPointerDown."+namespace,function(e){
        touchActive=true;
        if(!$(e.target).hasClass("mCSB_dragger")){clickable=1;}
      }).bind("touchend."+namespace+" pointerup."+namespace+" MSPointerUp."+namespace,function(e){
        touchActive=false;
      }).bind("click."+namespace,function(e){
        if(!clickable){return;}
        clickable=0;
        if($(e.target).hasClass(classes[12]) || $(e.target).hasClass("mCSB_draggerRail")){
          _stop($this);
          var el=$(this),mCSB_dragger=el.find(".mCSB_dragger");
          if(el.parent(".mCSB_scrollTools_horizontal").length>0){
            if(!d.overflowed[1]){return;}
            var dir="x",
              clickDir=e.pageX>mCSB_dragger.offset().left ? -1 : 1,
              to=Math.abs(mCSB_container[0].offsetLeft)-(clickDir*(wrapper.width()*0.9));
          }else{
            if(!d.overflowed[0]){return;}
            var dir="y",
              clickDir=e.pageY>mCSB_dragger.offset().top ? -1 : 1,
              to=Math.abs(mCSB_container[0].offsetTop)-(clickDir*(wrapper.height()*0.9));
          }
          _scrollTo($this,to.toString(),{dir:dir,scrollEasing:"mcsEaseInOut"});
        }
      });
    },
    /* -------------------- */
    
    
    /* 
    FOCUS EVENT
    scrolls content via element focus (e.g. clicking an input, pressing TAB key etc.)
    */
    _focus=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        namespace=pluginPfx+"_"+d.idx,
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        wrapper=mCSB_container.parent();
      mCSB_container.bind("focusin."+namespace,function(e){
        var el=$(document.activeElement),
          nested=mCSB_container.find(".mCustomScrollBox").length,
          dur=0;
        if(!el.is(o.advanced.autoScrollOnFocus)){return;}
        _stop($this);
        clearTimeout($this[0]._focusTimeout);
        $this[0]._focusTimer=nested ? (dur+17)*nested : 0;
        $this[0]._focusTimeout=setTimeout(function(){
          var to=[_childPos(el)[0],_childPos(el)[1]],
            contentPos=[mCSB_container[0].offsetTop,mCSB_container[0].offsetLeft],
            isVisible=[
              (contentPos[0]+to[0]>=0 && contentPos[0]+to[0]<wrapper.height()-el.outerHeight(false)),
              (contentPos[1]+to[1]>=0 && contentPos[0]+to[1]<wrapper.width()-el.outerWidth(false))
            ],
            overwrite=(o.axis==="yx" && !isVisible[0] && !isVisible[1]) ? "none" : "all";
          if(o.axis!=="x" && !isVisible[0]){
            _scrollTo($this,to[0].toString(),{dir:"y",scrollEasing:"mcsEaseInOut",overwrite:overwrite,dur:dur});
          }
          if(o.axis!=="y" && !isVisible[1]){
            _scrollTo($this,to[1].toString(),{dir:"x",scrollEasing:"mcsEaseInOut",overwrite:overwrite,dur:dur});
          }
        },$this[0]._focusTimer);
      });
    },
    /* -------------------- */
    
    
    /* sets content wrapper scrollTop/scrollLeft always to 0 */
    _wrapperScroll=function(){
      var $this=$(this),d=$this.data(pluginPfx),
        namespace=pluginPfx+"_"+d.idx,
        wrapper=$("#mCSB_"+d.idx+"_container").parent();
      wrapper.bind("scroll."+namespace,function(e){
        if(wrapper.scrollTop()!==0 || wrapper.scrollLeft()!==0){
          $(".mCSB_"+d.idx+"_scrollbar").css("visibility","hidden"); /* hide scrollbar(s) */
        }
      });
    },
    /* -------------------- */
    
    
    /* 
    BUTTONS EVENTS
    scrolls content via up, down, left and right buttons 
    */
    _buttons=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,seq=d.sequential,
        namespace=pluginPfx+"_"+d.idx,
        sel=".mCSB_"+d.idx+"_scrollbar",
        btn=$(sel+">a");
      btn.bind("contextmenu."+namespace,function(e){
        e.preventDefault(); //prevent right click
      }).bind("mousedown."+namespace+" touchstart."+namespace+" pointerdown."+namespace+" MSPointerDown."+namespace+" mouseup."+namespace+" touchend."+namespace+" pointerup."+namespace+" MSPointerUp."+namespace+" mouseout."+namespace+" pointerout."+namespace+" MSPointerOut."+namespace+" click."+namespace,function(e){
        e.preventDefault();
        if(!_mouseBtnLeft(e)){return;} /* left mouse button only */
        var btnClass=$(this).attr("class");
        seq.type=o.scrollButtons.scrollType;
        switch(e.type){
          case "mousedown": case "touchstart": case "pointerdown": case "MSPointerDown":
            if(seq.type==="stepped"){return;}
            touchActive=true;
            d.tweenRunning=false;
            _seq("on",btnClass);
            break;
          case "mouseup": case "touchend": case "pointerup": case "MSPointerUp":
          case "mouseout": case "pointerout": case "MSPointerOut":
            if(seq.type==="stepped"){return;}
            touchActive=false;
            if(seq.dir){_seq("off",btnClass);}
            break;
          case "click":
            if(seq.type!=="stepped" || d.tweenRunning){return;}
            _seq("on",btnClass);
            break;
        }
        function _seq(a,c){
          seq.scrollAmount=o.scrollButtons.scrollAmount;
          _sequentialScroll($this,a,c);
        }
      });
    },
    /* -------------------- */
    
    
    /* 
    KEYBOARD EVENTS
    scrolls content via keyboard 
    Keys: up arrow, down arrow, left arrow, right arrow, PgUp, PgDn, Home, End
    */
    _keyboard=function(){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,seq=d.sequential,
        namespace=pluginPfx+"_"+d.idx,
        mCustomScrollBox=$("#mCSB_"+d.idx),
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        wrapper=mCSB_container.parent(),
        editables="input,textarea,select,datalist,keygen,[contenteditable='true']",
        iframe=mCSB_container.find("iframe"),
        events=["blur."+namespace+" keydown."+namespace+" keyup."+namespace];
      if(iframe.length){
        iframe.each(function(){
          $(this).bind("load",function(){
            /* bind events on accessible iframes */
            if(_canAccessIFrame(this)){
              $(this.contentDocument || this.contentWindow.document).bind(events[0],function(e){
                _onKeyboard(e);
              });
            }
          });
        });
      }
      mCustomScrollBox.attr("tabindex","0").bind(events[0],function(e){
        _onKeyboard(e);
      });
      function _onKeyboard(e){
        switch(e.type){
          case "blur":
            if(d.tweenRunning && seq.dir){_seq("off",null);}
            break;
          case "keydown": case "keyup":
            var code=e.keyCode ? e.keyCode : e.which,action="on";
            if((o.axis!=="x" && (code===38 || code===40)) || (o.axis!=="y" && (code===37 || code===39))){
              /* up (38), down (40), left (37), right (39) arrows */
              if(((code===38 || code===40) && !d.overflowed[0]) || ((code===37 || code===39) && !d.overflowed[1])){return;}
              if(e.type==="keyup"){action="off";}
              if(!$(document.activeElement).is(editables)){
                e.preventDefault();
                e.stopImmediatePropagation();
                _seq(action,code);
              }
            }else if(code===33 || code===34){
              /* PgUp (33), PgDn (34) */
              if(d.overflowed[0] || d.overflowed[1]){
                e.preventDefault();
                e.stopImmediatePropagation();
              }
              if(e.type==="keyup"){
                _stop($this);
                var keyboardDir=code===34 ? -1 : 1;
                if(o.axis==="x" || (o.axis==="yx" && d.overflowed[1] && !d.overflowed[0])){
                  var dir="x",to=Math.abs(mCSB_container[0].offsetLeft)-(keyboardDir*(wrapper.width()*0.9));
                }else{
                  var dir="y",to=Math.abs(mCSB_container[0].offsetTop)-(keyboardDir*(wrapper.height()*0.9));
                }
                _scrollTo($this,to.toString(),{dir:dir,scrollEasing:"mcsEaseInOut"});
              }
            }else if(code===35 || code===36){
              /* End (35), Home (36) */
              if(!$(document.activeElement).is(editables)){
                if(d.overflowed[0] || d.overflowed[1]){
                  e.preventDefault();
                  e.stopImmediatePropagation();
                }
                if(e.type==="keyup"){
                  if(o.axis==="x" || (o.axis==="yx" && d.overflowed[1] && !d.overflowed[0])){
                    var dir="x",to=code===35 ? Math.abs(wrapper.width()-mCSB_container.outerWidth(false)) : 0;
                  }else{
                    var dir="y",to=code===35 ? Math.abs(wrapper.height()-mCSB_container.outerHeight(false)) : 0;
                  }
                  _scrollTo($this,to.toString(),{dir:dir,scrollEasing:"mcsEaseInOut"});
                }
              }
            }
            break;
        }
        function _seq(a,c){
          seq.type=o.keyboard.scrollType;
          seq.scrollAmount=o.keyboard.scrollAmount;
          if(seq.type==="stepped" && d.tweenRunning){return;}
          _sequentialScroll($this,a,c);
        }
      }
    },
    /* -------------------- */
    
    
    /* scrolls content sequentially (used when scrolling via buttons, keyboard arrows etc.) */
    _sequentialScroll=function(el,action,trigger,e,s){
      var d=el.data(pluginPfx),o=d.opt,seq=d.sequential,
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        once=seq.type==="stepped" ? true : false,
        steplessSpeed=o.scrollInertia < 26 ? 26 : o.scrollInertia, /* 26/1.5=17 */
        steppedSpeed=o.scrollInertia < 1 ? 17 : o.scrollInertia;
      switch(action){
        case "on":
          seq.dir=[
            (trigger===classes[16] || trigger===classes[15] || trigger===39 || trigger===37 ? "x" : "y"),
            (trigger===classes[13] || trigger===classes[15] || trigger===38 || trigger===37 ? -1 : 1)
          ];
          _stop(el);
          if(_isNumeric(trigger) && seq.type==="stepped"){return;}
          _on(once);
          break;
        case "off":
          _off();
          if(once || (d.tweenRunning && seq.dir)){
            _on(true);
          }
          break;
      }
      
      /* starts sequence */
      function _on(once){
        if(o.snapAmount){seq.scrollAmount=!(o.snapAmount instanceof Array) ? o.snapAmount : seq.dir[0]==="x" ? o.snapAmount[1] : o.snapAmount[0];} /* scrolling snapping */
        var c=seq.type!=="stepped", /* continuous scrolling */
          t=s ? s : !once ? 1000/60 : c ? steplessSpeed/1.5 : steppedSpeed, /* timer */
          m=!once ? 2.5 : c ? 7.5 : 40, /* multiplier */
          contentPos=[Math.abs(mCSB_container[0].offsetTop),Math.abs(mCSB_container[0].offsetLeft)],
          ratio=[d.scrollRatio.y>10 ? 10 : d.scrollRatio.y,d.scrollRatio.x>10 ? 10 : d.scrollRatio.x],
          amount=seq.dir[0]==="x" ? contentPos[1]+(seq.dir[1]*(ratio[1]*m)) : contentPos[0]+(seq.dir[1]*(ratio[0]*m)),
          px=seq.dir[0]==="x" ? contentPos[1]+(seq.dir[1]*parseInt(seq.scrollAmount)) : contentPos[0]+(seq.dir[1]*parseInt(seq.scrollAmount)),
          to=seq.scrollAmount!=="auto" ? px : amount,
          easing=e ? e : !once ? "mcsLinear" : c ? "mcsLinearOut" : "mcsEaseInOut",
          onComplete=!once ? false : true;
        if(once && t<17){
          to=seq.dir[0]==="x" ? contentPos[1] : contentPos[0];
        }
        _scrollTo(el,to.toString(),{dir:seq.dir[0],scrollEasing:easing,dur:t,onComplete:onComplete});
        if(once){
          seq.dir=false;
          return;
        }
        clearTimeout(seq.step);
        seq.step=setTimeout(function(){
          _on();
        },t);
      }
      /* stops sequence */
      function _off(){
        clearTimeout(seq.step);
        _delete(seq,"step");
        _stop(el);
      }
    },
    /* -------------------- */
    
    
    /* returns a yx array from value */
    _arr=function(val){
      var o=$(this).data(pluginPfx).opt,vals=[];
      if(typeof val==="function"){val=val();} /* check if the value is a single anonymous function */
      /* check if value is object or array, its length and create an array with yx values */
      if(!(val instanceof Array)){ /* object value (e.g. {y:"100",x:"100"}, 100 etc.) */
        vals[0]=val.y ? val.y : val.x || o.axis==="x" ? null : val;
        vals[1]=val.x ? val.x : val.y || o.axis==="y" ? null : val;
      }else{ /* array value (e.g. [100,100]) */
        vals=val.length>1 ? [val[0],val[1]] : o.axis==="x" ? [null,val[0]] : [val[0],null];
      }
      /* check if array values are anonymous functions */
      if(typeof vals[0]==="function"){vals[0]=vals[0]();}
      if(typeof vals[1]==="function"){vals[1]=vals[1]();}
      return vals;
    },
    /* -------------------- */
    
    
    /* translates values (e.g. "top", 100, "100px", "#id") to actual scroll-to positions */
    _to=function(val,dir){
      if(val==null || typeof val=="undefined"){return;}
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        wrapper=mCSB_container.parent(),
        t=typeof val;
      if(!dir){dir=o.axis==="x" ? "x" : "y";}
      var contentLength=dir==="x" ? mCSB_container.outerWidth(false)-wrapper.width() : mCSB_container.outerHeight(false)-wrapper.height(),
        contentPos=dir==="x" ? mCSB_container[0].offsetLeft : mCSB_container[0].offsetTop,
        cssProp=dir==="x" ? "left" : "top";
      switch(t){
        case "function": /* this currently is not used. Consider removing it */
          return val();
          break;
        case "object": /* js/jquery object */
          var obj=val.jquery ? val : $(val);
          if(!obj.length){return;}
          return dir==="x" ? _childPos(obj)[1] : _childPos(obj)[0];
          break;
        case "string": case "number":
          if(_isNumeric(val)){ /* numeric value */
            return Math.abs(val);
          }else if(val.indexOf("%")!==-1){ /* percentage value */
            return Math.abs(contentLength*parseInt(val)/100);
          }else if(val.indexOf("-=")!==-1){ /* decrease value */
            return Math.abs(contentPos-parseInt(val.split("-=")[1]));
          }else if(val.indexOf("+=")!==-1){ /* inrease value */
            var p=(contentPos+parseInt(val.split("+=")[1]));
            return p>=0 ? 0 : Math.abs(p);
          }else if(val.indexOf("px")!==-1 && _isNumeric(val.split("px")[0])){ /* pixels string value (e.g. "100px") */
            return Math.abs(val.split("px")[0]);
          }else{
            if(val==="top" || val==="left"){ /* special strings */
              return 0;
            }else if(val==="bottom"){
              return Math.abs(wrapper.height()-mCSB_container.outerHeight(false));
            }else if(val==="right"){
              return Math.abs(wrapper.width()-mCSB_container.outerWidth(false));
            }else if(val==="first" || val==="last"){
              var obj=mCSB_container.find(":"+val);
              return dir==="x" ? _childPos(obj)[1] : _childPos(obj)[0];
            }else{
              if($(val).length){ /* jquery selector */
                return dir==="x" ? _childPos($(val))[1] : _childPos($(val))[0];
              }else{ /* other values (e.g. "100em") */
                mCSB_container.css(cssProp,val);
                methods.update.call(null,$this[0]);
                return;
              }
            }
          }
          break;
      }
    },
    /* -------------------- */
    
    
    /* calls the update method automatically */
    _autoUpdate=function(rem){
      var $this=$(this),d=$this.data(pluginPfx),o=d.opt,
        mCSB_container=$("#mCSB_"+d.idx+"_container");
      if(rem){
        /* 
        removes autoUpdate timer 
        usage: _autoUpdate.call(this,"remove");
        */
        clearTimeout(mCSB_container[0].autoUpdate);
        _delete(mCSB_container[0],"autoUpdate");
        return;
      }
      upd();
      function upd(){
        clearTimeout(mCSB_container[0].autoUpdate);
        if($this.parents("html").length===0){
          /* check element in dom tree */
          $this=null;
          return;
        }
        mCSB_container[0].autoUpdate=setTimeout(function(){
          /* update on specific selector(s) length and size change */
          if(o.advanced.updateOnSelectorChange){
            d.poll.change.n=sizesSum();
            if(d.poll.change.n!==d.poll.change.o){
              d.poll.change.o=d.poll.change.n;
              doUpd(3);
              return;
            }
          }
          /* update on main element and scrollbar size changes */
          if(o.advanced.updateOnContentResize){
            d.poll.size.n=$this[0].scrollHeight+$this[0].scrollWidth+mCSB_container[0].offsetHeight+$this[0].offsetHeight+$this[0].offsetWidth;
            if(d.poll.size.n!==d.poll.size.o){
              d.poll.size.o=d.poll.size.n;
              doUpd(1);
              return;
            }
          }
          /* update on image load */
          if(o.advanced.updateOnImageLoad){
            if(!(o.advanced.updateOnImageLoad==="auto" && o.axis==="y")){ //by default, it doesn't run on vertical content
              d.poll.img.n=mCSB_container.find("img").length;
              if(d.poll.img.n!==d.poll.img.o){
                d.poll.img.o=d.poll.img.n;
                mCSB_container.find("img").each(function(){
                  imgLoader(this);
                });
                return;
              }
            }
          }
          if(o.advanced.updateOnSelectorChange || o.advanced.updateOnContentResize || o.advanced.updateOnImageLoad){upd();}
        },o.advanced.autoUpdateTimeout);
      }
      /* a tiny image loader */
      function imgLoader(el){
        if($(el).hasClass(classes[2])){doUpd(); return;}
        var img=new Image();
        function createDelegate(contextObject,delegateMethod){
          return function(){return delegateMethod.apply(contextObject,arguments);}
        }
        function imgOnLoad(){
          this.onload=null;
          $(el).addClass(classes[2]);
          doUpd(2);
        }
        img.onload=createDelegate(img,imgOnLoad);
        img.src=el.src;
      }
      /* returns the total height and width sum of all elements matching the selector */
      function sizesSum(){
        if(o.advanced.updateOnSelectorChange===true){o.advanced.updateOnSelectorChange="*";}
        var total=0,sel=mCSB_container.find(o.advanced.updateOnSelectorChange);
        if(o.advanced.updateOnSelectorChange && sel.length>0){sel.each(function(){total+=this.offsetHeight+this.offsetWidth;});}
        return total;
      }
      /* calls the update method */
      function doUpd(cb){
        clearTimeout(mCSB_container[0].autoUpdate);
        methods.update.call(null,$this[0],cb);
      }
    },
    /* -------------------- */
    
    
    /* snaps scrolling to a multiple of a pixels number */
    _snapAmount=function(to,amount,offset){
      return (Math.round(to/amount)*amount-offset); 
    },
    /* -------------------- */
    
    
    /* stops content and scrollbar animations */
    _stop=function(el){
      var d=el.data(pluginPfx),
        sel=$("#mCSB_"+d.idx+"_container,#mCSB_"+d.idx+"_container_wrapper,#mCSB_"+d.idx+"_dragger_vertical,#mCSB_"+d.idx+"_dragger_horizontal");
      sel.each(function(){
        _stopTween.call(this);
      });
    },
    /* -------------------- */
    
    
    /* 
    ANIMATES CONTENT 
    This is where the actual scrolling happens
    */
    _scrollTo=function(el,to,options){
      var d=el.data(pluginPfx),o=d.opt,
        defaults={
          trigger:"internal",
          dir:"y",
          scrollEasing:"mcsEaseOut",
          drag:false,
          dur:o.scrollInertia,
          overwrite:"all",
          callbacks:true,
          onStart:true,
          onUpdate:true,
          onComplete:true
        },
        options=$.extend(defaults,options),
        dur=[options.dur,(options.drag ? 0 : options.dur)],
        mCustomScrollBox=$("#mCSB_"+d.idx),
        mCSB_container=$("#mCSB_"+d.idx+"_container"),
        wrapper=mCSB_container.parent(),
        totalScrollOffsets=o.callbacks.onTotalScrollOffset ? _arr.call(el,o.callbacks.onTotalScrollOffset) : [0,0],
        totalScrollBackOffsets=o.callbacks.onTotalScrollBackOffset ? _arr.call(el,o.callbacks.onTotalScrollBackOffset) : [0,0];
      d.trigger=options.trigger;
      if(wrapper.scrollTop()!==0 || wrapper.scrollLeft()!==0){ /* always reset scrollTop/Left */
        $(".mCSB_"+d.idx+"_scrollbar").css("visibility","visible");
        wrapper.scrollTop(0).scrollLeft(0);
      }
      if(to==="_resetY" && !d.contentReset.y){
        /* callbacks: onOverflowYNone */
        if(_cb("onOverflowYNone")){o.callbacks.onOverflowYNone.call(el[0]);}
        d.contentReset.y=1;
      }
      if(to==="_resetX" && !d.contentReset.x){
        /* callbacks: onOverflowXNone */
        if(_cb("onOverflowXNone")){o.callbacks.onOverflowXNone.call(el[0]);}
        d.contentReset.x=1;
      }
      if(to==="_resetY" || to==="_resetX"){return;}
      if((d.contentReset.y || !el[0].mcs) && d.overflowed[0]){
        /* callbacks: onOverflowY */
        if(_cb("onOverflowY")){o.callbacks.onOverflowY.call(el[0]);}
        d.contentReset.x=null;
      }
      if((d.contentReset.x || !el[0].mcs) && d.overflowed[1]){
        /* callbacks: onOverflowX */
        if(_cb("onOverflowX")){o.callbacks.onOverflowX.call(el[0]);}
        d.contentReset.x=null;
      }
      if(o.snapAmount){ /* scrolling snapping */
        var snapAmount=!(o.snapAmount instanceof Array) ? o.snapAmount : options.dir==="x" ? o.snapAmount[1] : o.snapAmount[0];
        to=_snapAmount(to,snapAmount,o.snapOffset);
      }
      switch(options.dir){
        case "x":
          var mCSB_dragger=$("#mCSB_"+d.idx+"_dragger_horizontal"),
            property="left",
            contentPos=mCSB_container[0].offsetLeft,
            limit=[
              mCustomScrollBox.width()-mCSB_container.outerWidth(false),
              mCSB_dragger.parent().width()-mCSB_dragger.width()
            ],
            scrollTo=[to,to===0 ? 0 : (to/d.scrollRatio.x)],
            tso=totalScrollOffsets[1],
            tsbo=totalScrollBackOffsets[1],
            totalScrollOffset=tso>0 ? tso/d.scrollRatio.x : 0,
            totalScrollBackOffset=tsbo>0 ? tsbo/d.scrollRatio.x : 0;
          break;
        case "y":
          var mCSB_dragger=$("#mCSB_"+d.idx+"_dragger_vertical"),
            property="top",
            contentPos=mCSB_container[0].offsetTop,
            limit=[
              mCustomScrollBox.height()-mCSB_container.outerHeight(false),
              mCSB_dragger.parent().height()-mCSB_dragger.height()
            ],
            scrollTo=[to,to===0 ? 0 : (to/d.scrollRatio.y)],
            tso=totalScrollOffsets[0],
            tsbo=totalScrollBackOffsets[0],
            totalScrollOffset=tso>0 ? tso/d.scrollRatio.y : 0,
            totalScrollBackOffset=tsbo>0 ? tsbo/d.scrollRatio.y : 0;
          break;
      }
      if(scrollTo[1]<0 || (scrollTo[0]===0 && scrollTo[1]===0)){
        scrollTo=[0,0];
      }else if(scrollTo[1]>=limit[1]){
        scrollTo=[limit[0],limit[1]];
      }else{
        scrollTo[0]=-scrollTo[0];
      }
      if(!el[0].mcs){
        _mcs();  /* init mcs object (once) to make it available before callbacks */
        if(_cb("onInit")){o.callbacks.onInit.call(el[0]);} /* callbacks: onInit */
      }
      clearTimeout(mCSB_container[0].onCompleteTimeout);
      _tweenTo(mCSB_dragger[0],property,Math.round(scrollTo[1]),dur[1],options.scrollEasing);
      if(!d.tweenRunning && ((contentPos===0 && scrollTo[0]>=0) || (contentPos===limit[0] && scrollTo[0]<=limit[0]))){return;}
      _tweenTo(mCSB_container[0],property,Math.round(scrollTo[0]),dur[0],options.scrollEasing,options.overwrite,{
        onStart:function(){
          if(options.callbacks && options.onStart && !d.tweenRunning){
            /* callbacks: onScrollStart */
            if(_cb("onScrollStart")){_mcs(); o.callbacks.onScrollStart.call(el[0]);}
            d.tweenRunning=true;
            _onDragClasses(mCSB_dragger);
            d.cbOffsets=_cbOffsets();
          }
        },onUpdate:function(){
          if(options.callbacks && options.onUpdate){
            /* callbacks: whileScrolling */
            if(_cb("whileScrolling")){_mcs(); o.callbacks.whileScrolling.call(el[0]);}
          }
        },onComplete:function(){
          if(options.callbacks && options.onComplete){
            if(o.axis==="yx"){clearTimeout(mCSB_container[0].onCompleteTimeout);}
            var t=mCSB_container[0].idleTimer || 0;
            mCSB_container[0].onCompleteTimeout=setTimeout(function(){
              /* callbacks: onScroll, onTotalScroll, onTotalScrollBack */
              if(_cb("onScroll")){_mcs(); o.callbacks.onScroll.call(el[0]);}
              if(_cb("onTotalScroll") && scrollTo[1]>=limit[1]-totalScrollOffset && d.cbOffsets[0]){_mcs(); o.callbacks.onTotalScroll.call(el[0]);}
              if(_cb("onTotalScrollBack") && scrollTo[1]<=totalScrollBackOffset && d.cbOffsets[1]){_mcs(); o.callbacks.onTotalScrollBack.call(el[0]);}
              d.tweenRunning=false;
              mCSB_container[0].idleTimer=0;
              _onDragClasses(mCSB_dragger,"hide");
            },t);
          }
        }
      });
      /* checks if callback function exists */
      function _cb(cb){
        return d && o.callbacks[cb] && typeof o.callbacks[cb]==="function";
      }
      /* checks whether callback offsets always trigger */
      function _cbOffsets(){
        return [o.callbacks.alwaysTriggerOffsets || contentPos>=limit[0]+tso,o.callbacks.alwaysTriggerOffsets || contentPos<=-tsbo];
      }
      /* 
      populates object with useful values for the user 
      values: 
        content: this.mcs.content
        content top position: this.mcs.top 
        content left position: this.mcs.left 
        dragger top position: this.mcs.draggerTop 
        dragger left position: this.mcs.draggerLeft 
        scrolling y percentage: this.mcs.topPct 
        scrolling x percentage: this.mcs.leftPct 
        scrolling direction: this.mcs.direction
      */
      function _mcs(){
        var cp=[mCSB_container[0].offsetTop,mCSB_container[0].offsetLeft], /* content position */
          dp=[mCSB_dragger[0].offsetTop,mCSB_dragger[0].offsetLeft], /* dragger position */
          cl=[mCSB_container.outerHeight(false),mCSB_container.outerWidth(false)], /* content length */
          pl=[mCustomScrollBox.height(),mCustomScrollBox.width()]; /* content parent length */
        el[0].mcs={
          content:mCSB_container, /* original content wrapper as jquery object */
          top:cp[0],left:cp[1],draggerTop:dp[0],draggerLeft:dp[1],
          topPct:Math.round((100*Math.abs(cp[0]))/(Math.abs(cl[0])-pl[0])),leftPct:Math.round((100*Math.abs(cp[1]))/(Math.abs(cl[1])-pl[1])),
          direction:options.dir
        };
        /* 
        this refers to the original element containing the scrollbar(s)
        usage: this.mcs.top, this.mcs.leftPct etc. 
        */
      }
    },
    /* -------------------- */
    
    
    /* 
    CUSTOM JAVASCRIPT ANIMATION TWEEN 
    Lighter and faster than jquery animate() and css transitions 
    Animates top/left properties and includes easings 
    */
    _tweenTo=function(el,prop,to,duration,easing,overwrite,callbacks){
      if(!el._mTween){el._mTween={top:{},left:{}};}
      var callbacks=callbacks || {},
        onStart=callbacks.onStart || function(){},onUpdate=callbacks.onUpdate || function(){},onComplete=callbacks.onComplete || function(){},
        startTime=_getTime(),_delay,progress=0,from=el.offsetTop,elStyle=el.style,_request,tobj=el._mTween[prop];
      if(prop==="left"){from=el.offsetLeft;}
      var diff=to-from;
      tobj.stop=0;
      if(overwrite!=="none"){_cancelTween();}
      _startTween();
      function _step(){
        if(tobj.stop){return;}
        if(!progress){onStart.call();}
        progress=_getTime()-startTime;
        _tween();
        if(progress>=tobj.time){
          tobj.time=(progress>tobj.time) ? progress+_delay-(progress-tobj.time) : progress+_delay-1;
          if(tobj.time<progress+1){tobj.time=progress+1;}
        }
        if(tobj.time<duration){tobj.id=_request(_step);}else{onComplete.call();}
      }
      function _tween(){
        if(duration>0){
          tobj.currVal=_ease(tobj.time,from,diff,duration,easing);
          elStyle[prop]=Math.round(tobj.currVal)+"px";
        }else{
          elStyle[prop]=to+"px";
        }
        onUpdate.call();
      }
      function _startTween(){
        _delay=1000/60;
        tobj.time=progress+_delay;
        _request=(!window.requestAnimationFrame) ? function(f){_tween(); return setTimeout(f,0.01);} : window.requestAnimationFrame;
        tobj.id=_request(_step);
      }
      function _cancelTween(){
        if(tobj.id==null){return;}
        if(!window.requestAnimationFrame){clearTimeout(tobj.id);
        }else{window.cancelAnimationFrame(tobj.id);}
        tobj.id=null;
      }
      function _ease(t,b,c,d,type){
        switch(type){
          case "linear": case "mcsLinear":
            return c*t/d + b;
            break;
          case "mcsLinearOut":
            t/=d; t--; return c * Math.sqrt(1 - t*t) + b;
            break;
          case "easeInOutSmooth":
            t/=d/2;
            if(t<1) return c/2*t*t + b;
            t--;
            return -c/2 * (t*(t-2) - 1) + b;
            break;
          case "easeInOutStrong":
            t/=d/2;
            if(t<1) return c/2 * Math.pow( 2, 10 * (t - 1) ) + b;
            t--;
            return c/2 * ( -Math.pow( 2, -10 * t) + 2 ) + b;
            break;
          case "easeInOut": case "mcsEaseInOut":
            t/=d/2;
            if(t<1) return c/2*t*t*t + b;
            t-=2;
            return c/2*(t*t*t + 2) + b;
            break;
          case "easeOutSmooth":
            t/=d; t--;
            return -c * (t*t*t*t - 1) + b;
            break;
          case "easeOutStrong":
            return c * ( -Math.pow( 2, -10 * t/d ) + 1 ) + b;
            break;
          case "easeOut": case "mcsEaseOut": default:
            var ts=(t/=d)*t,tc=ts*t;
            return b+c*(0.499999999999997*tc*ts + -2.5*ts*ts + 5.5*tc + -6.5*ts + 4*t);
        }
      }
    },
    /* -------------------- */
    
    
    /* returns current time */
    _getTime=function(){
      if(window.performance && window.performance.now){
        return window.performance.now();
      }else{
        if(window.performance && window.performance.webkitNow){
          return window.performance.webkitNow();
        }else{
          if(Date.now){return Date.now();}else{return new Date().getTime();}
        }
      }
    },
    /* -------------------- */
    
    
    /* stops a tween */
    _stopTween=function(){
      var el=this;
      if(!el._mTween){el._mTween={top:{},left:{}};}
      var props=["top","left"];
      for(var i=0; i<props.length; i++){
        var prop=props[i];
        if(el._mTween[prop].id){
          if(!window.requestAnimationFrame){clearTimeout(el._mTween[prop].id);
          }else{window.cancelAnimationFrame(el._mTween[prop].id);}
          el._mTween[prop].id=null;
          el._mTween[prop].stop=1;
        }
      }
    },
    /* -------------------- */
    
    
    /* deletes a property (avoiding the exception thrown by IE) */
    _delete=function(c,m){
      try{delete c[m];}catch(e){c[m]=null;}
    },
    /* -------------------- */
    
    
    /* detects left mouse button */
    _mouseBtnLeft=function(e){
      return !(e.which && e.which!==1);
    },
    /* -------------------- */
    
    
    /* detects if pointer type event is touch */
    _pointerTouch=function(e){
      var t=e.originalEvent.pointerType;
      return !(t && t!=="touch" && t!==2);
    },
    /* -------------------- */
    
    
    /* checks if value is numeric */
    _isNumeric=function(val){
      return !isNaN(parseFloat(val)) && isFinite(val);
    },
    /* -------------------- */
    
    
    /* returns element position according to content */
    _childPos=function(el){
      var p=el.parents(".mCSB_container");
      return [el.offset().top-p.offset().top,el.offset().left-p.offset().left];
    },
    /* -------------------- */
    
    
    /* checks if browser tab is hidden/inactive via Page Visibility API */
    _isTabHidden=function(){
      var prop=_getHiddenProp();
      if(!prop) return false;
      return document[prop];
      function _getHiddenProp(){
        var pfx=["webkit","moz","ms","o"];
        if("hidden" in document) return "hidden"; //natively supported
        for(var i=0; i<pfx.length; i++){ //prefixed
            if((pfx[i]+"Hidden") in document) 
                return pfx[i]+"Hidden";
        }
        return null; //not supported
      }
    };
    /* -------------------- */
    
  
  
  
  
  /* 
  ----------------------------------------
  PLUGIN SETUP 
  ----------------------------------------
  */
  
  /* plugin constructor functions */
  $.fn[pluginNS]=function(method){ /* usage: $(selector).mCustomScrollbar(); */
    if(methods[method]){
      return methods[method].apply(this,Array.prototype.slice.call(arguments,1));
    }else if(typeof method==="object" || !method){
      return methods.init.apply(this,arguments);
    }else{
      $.error("Method "+method+" does not exist");
    }
  };
  $[pluginNS]=function(method){ /* usage: $.mCustomScrollbar(); */
    if(methods[method]){
      return methods[method].apply(this,Array.prototype.slice.call(arguments,1));
    }else if(typeof method==="object" || !method){
      return methods.init.apply(this,arguments);
    }else{
      $.error("Method "+method+" does not exist");
    }
  };
  
  /* 
  allow setting plugin default options. 
  usage: $.mCustomScrollbar.defaults.scrollInertia=500; 
  to apply any changed default options on default selectors (below), use inside document ready fn 
  e.g.: $(document).ready(function(){ $.mCustomScrollbar.defaults.scrollInertia=500; });
  */
  $[pluginNS].defaults=defaults;
  
  /* 
  add window object (window.mCustomScrollbar) 
  usage: if(window.mCustomScrollbar){console.log("custom scrollbar plugin loaded");}
  */
  window[pluginNS]=true;
  
  $(window).bind("load",function(){
    
    $(defaultSelector)[pluginNS](); /* add scrollbars automatically on default selector */
    
    /* extend jQuery expressions */
    $.extend($.expr[":"],{
      /* checks if element is within scrollable viewport */
      mcsInView:$.expr[":"].mcsInView || function(el){
        var $el=$(el),content=$el.parents(".mCSB_container"),wrapper,cPos;
        if(!content.length){return;}
        wrapper=content.parent();
        cPos=[content[0].offsetTop,content[0].offsetLeft];
        return  cPos[0]+_childPos($el)[0]>=0 && cPos[0]+_childPos($el)[0]<wrapper.height()-$el.outerHeight(false) && 
            cPos[1]+_childPos($el)[1]>=0 && cPos[1]+_childPos($el)[1]<wrapper.width()-$el.outerWidth(false);
      },
      /* checks if element or part of element is in view of scrollable viewport */
      mcsInSight:$.expr[":"].mcsInSight || function(el,i,m){
        var $el=$(el),elD,content=$el.parents(".mCSB_container"),wrapperView,pos,wrapperViewPct,
          pctVals=m[3]==="exact" ? [[1,0],[1,0]] : [[0.9,0.1],[0.6,0.4]];
        if(!content.length){return;}
        elD=[$el.outerHeight(false),$el.outerWidth(false)];
        pos=[content[0].offsetTop+_childPos($el)[0],content[0].offsetLeft+_childPos($el)[1]];
        wrapperView=[content.parent()[0].offsetHeight,content.parent()[0].offsetWidth];
        wrapperViewPct=[elD[0]<wrapperView[0] ? pctVals[0] : pctVals[1],elD[1]<wrapperView[1] ? pctVals[0] : pctVals[1]];
        return  pos[0]-(wrapperView[0]*wrapperViewPct[0][0])<0 && pos[0]+elD[0]-(wrapperView[0]*wrapperViewPct[0][1])>=0 && 
            pos[1]-(wrapperView[1]*wrapperViewPct[1][0])<0 && pos[1]+elD[1]-(wrapperView[1]*wrapperViewPct[1][1])>=0;
      },
      /* checks if element is overflowed having visible scrollbar(s) */
      mcsOverflow:$.expr[":"].mcsOverflow || function(el){
        var d=$(el).data(pluginPfx);
        if(!d){return;}
        return d.overflowed[0] || d.overflowed[1];
      }
    });
  
  });

}))}));


/* ================================================================================
  =================== Bootstrap-slider JS starts here  ============================
 * ============================================================================= */

/*! =======================================================
                      VERSION  9.8.1              
========================================================= */
"use strict";

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

/*! =========================================================
 * bootstrap-slider.js
 *
 * Maintainers:
 *    Kyle Kemp
 *      - Twitter: @seiyria
 *      - Github:  seiyria
 *    Rohit Kalkur
 *      - Twitter: @Rovolutionary
 *      - Github:  rovolution
 *
 * =========================================================
 *
 * bootstrap-slider is released under the MIT License
 * Copyright (c) 2017 Kyle Kemp, Rohit Kalkur, and contributors
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 *
 * ========================================================= */

/**
 * Bridget makes jQuery widgets
 * v1.0.1
 * MIT license
 */
var windowIsDefined = (typeof window === "undefined" ? "undefined" : _typeof(window)) === "object";

(function (factory) {
  if (typeof define === "function" && define.amd) {
    define(["jquery"], factory);
  } else if ((typeof module === "undefined" ? "undefined" : _typeof(module)) === "object" && module.exports) {
    var jQuery;
    try {
      jQuery = require("jquery");
    } catch (err) {
      jQuery = null;
    }
    module.exports = factory(jQuery);
  } else if (window) {
    window.Slider = factory(window.jQuery);
  }
})(function ($) {
  // Constants
  var NAMESPACE_MAIN = 'slider';
  var NAMESPACE_ALTERNATE = 'bootstrapSlider';

  // Polyfill console methods
  if (windowIsDefined && !window.console) {
    window.console = {};
  }
  if (windowIsDefined && !window.console.log) {
    window.console.log = function () {};
  }
  if (windowIsDefined && !window.console.warn) {
    window.console.warn = function () {};
  }

  // Reference to Slider constructor
  var Slider;

  (function ($) {

    'use strict';

    // -------------------------- utils -------------------------- //

    var slice = Array.prototype.slice;

    function noop() {}

    // -------------------------- definition -------------------------- //

    function defineBridget($) {

      // bail if no jQuery
      if (!$) {
        return;
      }

      // -------------------------- addOptionMethod -------------------------- //

      /**
    * adds option method -> $().plugin('option', {...})
    * @param {Function} PluginClass - constructor class
    */
      function addOptionMethod(PluginClass) {
        // don't overwrite original option method
        if (PluginClass.prototype.option) {
          return;
        }

        // option setter
        PluginClass.prototype.option = function (opts) {
          // bail out if not an object
          if (!$.isPlainObject(opts)) {
            return;
          }
          this.options = $.extend(true, this.options, opts);
        };
      }

      // -------------------------- plugin bridge -------------------------- //

      // helper function for logging errors
      // $.error breaks jQuery chaining
      var logError = typeof console === 'undefined' ? noop : function (message) {
        console.error(message);
      };

      /**
    * jQuery plugin bridge, access methods like $elem.plugin('method')
    * @param {String} namespace - plugin name
    * @param {Function} PluginClass - constructor class
    */
      function bridge(namespace, PluginClass) {
        // add to jQuery fn namespace
        $.fn[namespace] = function (options) {
          if (typeof options === 'string') {
            // call plugin method when first argument is a string
            // get arguments for method
            var args = slice.call(arguments, 1);

            for (var i = 0, len = this.length; i < len; i++) {
              var elem = this[i];
              var instance = $.data(elem, namespace);
              if (!instance) {
                logError("cannot call methods on " + namespace + " prior to initialization; " + "attempted to call '" + options + "'");
                continue;
              }
              if (!$.isFunction(instance[options]) || options.charAt(0) === '_') {
                logError("no such method '" + options + "' for " + namespace + " instance");
                continue;
              }

              // trigger method with arguments
              var returnValue = instance[options].apply(instance, args);

              // break look and return first value if provided
              if (returnValue !== undefined && returnValue !== instance) {
                return returnValue;
              }
            }
            // return this if no return value
            return this;
          } else {
            var objects = this.map(function () {
              var instance = $.data(this, namespace);
              if (instance) {
                // apply options & init
                instance.option(options);
                instance._init();
              } else {
                // initialize new instance
                instance = new PluginClass(this, options);
                $.data(this, namespace, instance);
              }
              return $(this);
            });

            if (!objects || objects.length > 1) {
              return objects;
            } else {
              return objects[0];
            }
          }
        };
      }

      // -------------------------- bridget -------------------------- //

      /**
    * converts a Prototypical class into a proper jQuery plugin
    *   the class must have a ._init method
    * @param {String} namespace - plugin name, used in $().pluginName
    * @param {Function} PluginClass - constructor class
    */
      $.bridget = function (namespace, PluginClass) {
        addOptionMethod(PluginClass);
        bridge(namespace, PluginClass);
      };

      return $.bridget;
    }

    // get jquery from browser global
    defineBridget($);
  })($);

  /*************************************************
      BOOTSTRAP-SLIDER SOURCE CODE
  **************************************************/

  (function ($) {

    var ErrorMsgs = {
      formatInvalidInputErrorMsg: function formatInvalidInputErrorMsg(input) {
        return "Invalid input value '" + input + "' passed in";
      },
      callingContextNotSliderInstance: "Calling context element does not have instance of Slider bound to it. Check your code to make sure the JQuery object returned from the call to the slider() initializer is calling the method"
    };

    var SliderScale = {
      linear: {
        toValue: function toValue(percentage) {
          var rawValue = percentage / 100 * (this.options.max - this.options.min);
          var shouldAdjustWithBase = true;
          if (this.options.ticks_positions.length > 0) {
            var minv,
                maxv,
                minp,
                maxp = 0;
            for (var i = 1; i < this.options.ticks_positions.length; i++) {
              if (percentage <= this.options.ticks_positions[i]) {
                minv = this.options.ticks[i - 1];
                minp = this.options.ticks_positions[i - 1];
                maxv = this.options.ticks[i];
                maxp = this.options.ticks_positions[i];

                break;
              }
            }
            var partialPercentage = (percentage - minp) / (maxp - minp);
            rawValue = minv + partialPercentage * (maxv - minv);
            shouldAdjustWithBase = false;
          }

          var adjustment = shouldAdjustWithBase ? this.options.min : 0;
          var value = adjustment + Math.round(rawValue / this.options.step) * this.options.step;
          if (value < this.options.min) {
            return this.options.min;
          } else if (value > this.options.max) {
            return this.options.max;
          } else {
            return value;
          }
        },
        toPercentage: function toPercentage(value) {
          if (this.options.max === this.options.min) {
            return 0;
          }

          if (this.options.ticks_positions.length > 0) {
            var minv,
                maxv,
                minp,
                maxp = 0;
            for (var i = 0; i < this.options.ticks.length; i++) {
              if (value <= this.options.ticks[i]) {
                minv = i > 0 ? this.options.ticks[i - 1] : 0;
                minp = i > 0 ? this.options.ticks_positions[i - 1] : 0;
                maxv = this.options.ticks[i];
                maxp = this.options.ticks_positions[i];

                break;
              }
            }
            if (i > 0) {
              var partialPercentage = (value - minv) / (maxv - minv);
              return minp + partialPercentage * (maxp - minp);
            }
          }

          return 100 * (value - this.options.min) / (this.options.max - this.options.min);
        }
      },

      logarithmic: {
        /* Based on http://stackoverflow.com/questions/846221/logarithmic-slider */
        toValue: function toValue(percentage) {
          var min = this.options.min === 0 ? 0 : Math.log(this.options.min);
          var max = Math.log(this.options.max);
          var value = Math.exp(min + (max - min) * percentage / 100);
          if (Math.round(value) === this.options.max) {
            return this.options.max;
          }
          value = this.options.min + Math.round((value - this.options.min) / this.options.step) * this.options.step;
          /* Rounding to the nearest step could exceed the min or
      * max, so clip to those values. */
          if (value < this.options.min) {
            return this.options.min;
          } else if (value > this.options.max) {
            return this.options.max;
          } else {
            return value;
          }
        },
        toPercentage: function toPercentage(value) {
          if (this.options.max === this.options.min) {
            return 0;
          } else {
            var max = Math.log(this.options.max);
            var min = this.options.min === 0 ? 0 : Math.log(this.options.min);
            var v = value === 0 ? 0 : Math.log(value);
            return 100 * (v - min) / (max - min);
          }
        }
      }
    };

    /*************************************************
              CONSTRUCTOR
    **************************************************/
    Slider = function Slider(element, options) {
      createNewSlider.call(this, element, options);
      return this;
    };

    function createNewSlider(element, options) {

      /*
    The internal state object is used to store data about the current 'state' of slider.
    This includes values such as the `value`, `enabled`, etc...
   */
      this._state = {
        value: null,
        enabled: null,
        offset: null,
        size: null,
        percentage: null,
        inDrag: false,
        over: false
      };

      // The objects used to store the reference to the tick methods if ticks_tooltip is on
      this.ticksCallbackMap = {};
      this.handleCallbackMap = {};

      if (typeof element === "string") {
        this.element = document.querySelector(element);
      } else if (element instanceof HTMLElement) {
        this.element = element;
      }

      /*************************************************
            Process Options
    **************************************************/
      options = options ? options : {};
      var optionTypes = Object.keys(this.defaultOptions);

      for (var i = 0; i < optionTypes.length; i++) {
        var optName = optionTypes[i];

        // First check if an option was passed in via the constructor
        var val = options[optName];
        // If no data attrib, then check data atrributes
        val = typeof val !== 'undefined' ? val : getDataAttrib(this.element, optName);
        // Finally, if nothing was specified, use the defaults
        val = val !== null ? val : this.defaultOptions[optName];

        // Set all options on the instance of the Slider
        if (!this.options) {
          this.options = {};
        }
        this.options[optName] = val;
      }

      // Check options.rtl
      if (this.options.rtl === 'auto') {
        this.options.rtl = window.getComputedStyle(this.element).direction === 'rtl';
      }

      /*
    Validate `tooltip_position` against 'orientation`
    - if `tooltip_position` is incompatible with orientation, swith it to a default compatible with specified `orientation`
      -- default for "vertical" -> "right", "left" if rtl
      -- default for "horizontal" -> "top"
   */
      if (this.options.orientation === "vertical" && (this.options.tooltip_position === "top" || this.options.tooltip_position === "bottom")) {
        if (this.options.rtl) {
          this.options.tooltip_position = "left";
        } else {
          this.options.tooltip_position = "right";
        }
      } else if (this.options.orientation === "horizontal" && (this.options.tooltip_position === "left" || this.options.tooltip_position === "right")) {

        this.options.tooltip_position = "top";
      }

      function getDataAttrib(element, optName) {
        var dataName = "data-slider-" + optName.replace(/_/g, '-');
        var dataValString = element.getAttribute(dataName);

        try {
          return JSON.parse(dataValString);
        } catch (err) {
          return dataValString;
        }
      }

      /*************************************************
            Create Markup
    **************************************************/

      var origWidth = this.element.style.width;
      var updateSlider = false;
      var parent = this.element.parentNode;
      var sliderTrackSelection;
      var sliderTrackLow, sliderTrackHigh;
      var sliderMinHandle;
      var sliderMaxHandle;

      if (this.sliderElem) {
        updateSlider = true;
      } else {
        /* Create elements needed for slider */
        this.sliderElem = document.createElement("div");
        this.sliderElem.className = "slider";

        /* Create slider track elements */
        var sliderTrack = document.createElement("div");
        sliderTrack.className = "slider-track";

        sliderTrackLow = document.createElement("div");
        sliderTrackLow.className = "slider-track-low";

        sliderTrackSelection = document.createElement("div");
        sliderTrackSelection.className = "slider-selection";

        sliderTrackHigh = document.createElement("div");
        sliderTrackHigh.className = "slider-track-high";

        sliderMinHandle = document.createElement("div");
        sliderMinHandle.className = "slider-handle min-slider-handle";
        sliderMinHandle.setAttribute('role', 'slider');
        sliderMinHandle.setAttribute('aria-valuemin', this.options.min);
        sliderMinHandle.setAttribute('aria-valuemax', this.options.max);

        sliderMaxHandle = document.createElement("div");
        sliderMaxHandle.className = "slider-handle max-slider-handle";
        sliderMaxHandle.setAttribute('role', 'slider');
        sliderMaxHandle.setAttribute('aria-valuemin', this.options.min);
        sliderMaxHandle.setAttribute('aria-valuemax', this.options.max);

        sliderTrack.appendChild(sliderTrackLow);
        sliderTrack.appendChild(sliderTrackSelection);
        sliderTrack.appendChild(sliderTrackHigh);

        /* Create highlight range elements */
        this.rangeHighlightElements = [];
        var rangeHighlightsOpts = this.options.rangeHighlights;
        if (Array.isArray(rangeHighlightsOpts) && rangeHighlightsOpts.length > 0) {
          for (var j = 0; j < rangeHighlightsOpts.length; j++) {
            var rangeHighlightElement = document.createElement("div");
            var customClassString = rangeHighlightsOpts[j].class || "";
            rangeHighlightElement.className = "slider-rangeHighlight slider-selection " + customClassString;
            this.rangeHighlightElements.push(rangeHighlightElement);
            sliderTrack.appendChild(rangeHighlightElement);
          }
        }

        /* Add aria-labelledby to handle's */
        var isLabelledbyArray = Array.isArray(this.options.labelledby);
        if (isLabelledbyArray && this.options.labelledby[0]) {
          sliderMinHandle.setAttribute('aria-labelledby', this.options.labelledby[0]);
        }
        if (isLabelledbyArray && this.options.labelledby[1]) {
          sliderMaxHandle.setAttribute('aria-labelledby', this.options.labelledby[1]);
        }
        if (!isLabelledbyArray && this.options.labelledby) {
          sliderMinHandle.setAttribute('aria-labelledby', this.options.labelledby);
          sliderMaxHandle.setAttribute('aria-labelledby', this.options.labelledby);
        }

        /* Create ticks */
        this.ticks = [];
        if (Array.isArray(this.options.ticks) && this.options.ticks.length > 0) {
          this.ticksContainer = document.createElement('div');
          this.ticksContainer.className = 'slider-tick-container';

          for (i = 0; i < this.options.ticks.length; i++) {
            var tick = document.createElement('div');
            tick.className = 'slider-tick';
            if (this.options.ticks_tooltip) {
              var tickListenerReference = this._addTickListener();
              var enterCallback = tickListenerReference.addMouseEnter(this, tick, i);
              var leaveCallback = tickListenerReference.addMouseLeave(this, tick);

              this.ticksCallbackMap[i] = {
                mouseEnter: enterCallback,
                mouseLeave: leaveCallback
              };
            }
            this.ticks.push(tick);
            this.ticksContainer.appendChild(tick);
          }

          sliderTrackSelection.className += " tick-slider-selection";
        }

        this.tickLabels = [];
        if (Array.isArray(this.options.ticks_labels) && this.options.ticks_labels.length > 0) {
          this.tickLabelContainer = document.createElement('div');
          this.tickLabelContainer.className = 'slider-tick-label-container';

          for (i = 0; i < this.options.ticks_labels.length; i++) {
            var label = document.createElement('div');
            var noTickPositionsSpecified = this.options.ticks_positions.length === 0;
            var tickLabelsIndex = this.options.reversed && noTickPositionsSpecified ? this.options.ticks_labels.length - (i + 1) : i;
            label.className = 'slider-tick-label';
            label.innerHTML = this.options.ticks_labels[tickLabelsIndex];

            this.tickLabels.push(label);
            this.tickLabelContainer.appendChild(label);
          }
        }

        var createAndAppendTooltipSubElements = function createAndAppendTooltipSubElements(tooltipElem) {
          var arrow = document.createElement("div");
          arrow.className = "tooltip-arrow";

          var inner = document.createElement("div");
          inner.className = "tooltip-inner";

          tooltipElem.appendChild(arrow);
          tooltipElem.appendChild(inner);
        };

        /* Create tooltip elements */
        var sliderTooltip = document.createElement("div");
        sliderTooltip.className = "tooltip tooltip-main";
        sliderTooltip.setAttribute('role', 'presentation');
        createAndAppendTooltipSubElements(sliderTooltip);

        var sliderTooltipMin = document.createElement("div");
        sliderTooltipMin.className = "tooltip tooltip-min";
        sliderTooltipMin.setAttribute('role', 'presentation');
        createAndAppendTooltipSubElements(sliderTooltipMin);

        var sliderTooltipMax = document.createElement("div");
        sliderTooltipMax.className = "tooltip tooltip-max";
        sliderTooltipMax.setAttribute('role', 'presentation');
        createAndAppendTooltipSubElements(sliderTooltipMax);

        /* Append components to sliderElem */
        this.sliderElem.appendChild(sliderTrack);
        this.sliderElem.appendChild(sliderTooltip);
        this.sliderElem.appendChild(sliderTooltipMin);
        this.sliderElem.appendChild(sliderTooltipMax);

        if (this.tickLabelContainer) {
          this.sliderElem.appendChild(this.tickLabelContainer);
        }
        if (this.ticksContainer) {
          this.sliderElem.appendChild(this.ticksContainer);
        }

        this.sliderElem.appendChild(sliderMinHandle);
        this.sliderElem.appendChild(sliderMaxHandle);

        /* Append slider element to parent container, right before the original <input> element */
        parent.insertBefore(this.sliderElem, this.element);

        /* Hide original <input> element */
        this.element.style.display = "none";
      }
      /* If JQuery exists, cache JQ references */
      if ($) {
        this.$element = $(this.element);
        this.$sliderElem = $(this.sliderElem);
      }

      /*************************************************
              Setup
    **************************************************/
      this.eventToCallbackMap = {};
      this.sliderElem.id = this.options.id;

      this.touchCapable = 'ontouchstart' in window || window.DocumentTouch && document instanceof window.DocumentTouch;

      this.touchX = 0;
      this.touchY = 0;

      this.tooltip = this.sliderElem.querySelector('.tooltip-main');
      this.tooltipInner = this.tooltip.querySelector('.tooltip-inner');

      this.tooltip_min = this.sliderElem.querySelector('.tooltip-min');
      this.tooltipInner_min = this.tooltip_min.querySelector('.tooltip-inner');

      this.tooltip_max = this.sliderElem.querySelector('.tooltip-max');
      this.tooltipInner_max = this.tooltip_max.querySelector('.tooltip-inner');

      if (SliderScale[this.options.scale]) {
        this.options.scale = SliderScale[this.options.scale];
      }

      if (updateSlider === true) {
        // Reset classes
        this._removeClass(this.sliderElem, 'slider-horizontal');
        this._removeClass(this.sliderElem, 'slider-vertical');
        this._removeClass(this.sliderElem, 'slider-rtl');
        this._removeClass(this.tooltip, 'hide');
        this._removeClass(this.tooltip_min, 'hide');
        this._removeClass(this.tooltip_max, 'hide');

        // Undo existing inline styles for track
        ["left", "right", "top", "width", "height"].forEach(function (prop) {
          this._removeProperty(this.trackLow, prop);
          this._removeProperty(this.trackSelection, prop);
          this._removeProperty(this.trackHigh, prop);
        }, this);

        // Undo inline styles on handles
        [this.handle1, this.handle2].forEach(function (handle) {
          this._removeProperty(handle, 'left');
          this._removeProperty(handle, 'right');
          this._removeProperty(handle, 'top');
        }, this);

        // Undo inline styles and classes on tooltips
        [this.tooltip, this.tooltip_min, this.tooltip_max].forEach(function (tooltip) {
          this._removeProperty(tooltip, 'left');
          this._removeProperty(tooltip, 'right');
          this._removeProperty(tooltip, 'top');
          this._removeProperty(tooltip, 'margin-left');
          this._removeProperty(tooltip, 'margin-right');
          this._removeProperty(tooltip, 'margin-top');

          this._removeClass(tooltip, 'right');
          this._removeClass(tooltip, 'left');
          this._removeClass(tooltip, 'top');
        }, this);
      }

      if (this.options.orientation === 'vertical') {
        this._addClass(this.sliderElem, 'slider-vertical');
        this.stylePos = 'top';
        this.mousePos = 'pageY';
        this.sizePos = 'offsetHeight';
      } else {
        this._addClass(this.sliderElem, 'slider-horizontal');
        this.sliderElem.style.width = origWidth;
        this.options.orientation = 'horizontal';
        if (this.options.rtl) {
          this.stylePos = 'right';
        } else {
          this.stylePos = 'left';
        }
        this.mousePos = 'pageX';
        this.sizePos = 'offsetWidth';
      }
      // specific rtl class
      if (this.options.rtl) {
        this._addClass(this.sliderElem, 'slider-rtl');
      }
      this._setTooltipPosition();
      /* In case ticks are specified, overwrite the min and max bounds */
      if (Array.isArray(this.options.ticks) && this.options.ticks.length > 0) {
        this.options.max = Math.max.apply(Math, this.options.ticks);
        this.options.min = Math.min.apply(Math, this.options.ticks);
      }

      if (Array.isArray(this.options.value)) {
        this.options.range = true;
        this._state.value = this.options.value;
      } else if (this.options.range) {
        // User wants a range, but value is not an array
        this._state.value = [this.options.value, this.options.max];
      } else {
        this._state.value = this.options.value;
      }

      this.trackLow = sliderTrackLow || this.trackLow;
      this.trackSelection = sliderTrackSelection || this.trackSelection;
      this.trackHigh = sliderTrackHigh || this.trackHigh;

      if (this.options.selection === 'none') {
        this._addClass(this.trackLow, 'hide');
        this._addClass(this.trackSelection, 'hide');
        this._addClass(this.trackHigh, 'hide');
      } else if (this.options.selection === 'after' || this.options.selection === 'before') {
        this._removeClass(this.trackLow, 'hide');
        this._removeClass(this.trackSelection, 'hide');
        this._removeClass(this.trackHigh, 'hide');
      }

      this.handle1 = sliderMinHandle || this.handle1;
      this.handle2 = sliderMaxHandle || this.handle2;

      if (updateSlider === true) {
        // Reset classes
        this._removeClass(this.handle1, 'round triangle');
        this._removeClass(this.handle2, 'round triangle hide');

        for (i = 0; i < this.ticks.length; i++) {
          this._removeClass(this.ticks[i], 'round triangle hide');
        }
      }

      var availableHandleModifiers = ['round', 'triangle', 'custom'];
      var isValidHandleType = availableHandleModifiers.indexOf(this.options.handle) !== -1;
      if (isValidHandleType) {
        this._addClass(this.handle1, this.options.handle);
        this._addClass(this.handle2, this.options.handle);

        for (i = 0; i < this.ticks.length; i++) {
          this._addClass(this.ticks[i], this.options.handle);
        }
      }

      this._state.offset = this._offset(this.sliderElem);
      this._state.size = this.sliderElem[this.sizePos];
      this.setValue(this._state.value);

      /******************************************
          Bind Event Listeners
    ******************************************/

      // Bind keyboard handlers
      this.handle1Keydown = this._keydown.bind(this, 0);
      this.handle1.addEventListener("keydown", this.handle1Keydown, false);

      this.handle2Keydown = this._keydown.bind(this, 1);
      this.handle2.addEventListener("keydown", this.handle2Keydown, false);

      this.mousedown = this._mousedown.bind(this);
      this.touchstart = this._touchstart.bind(this);
      this.touchmove = this._touchmove.bind(this);

      if (this.touchCapable) {
        // Test for passive event support
        var supportsPassive = false;
        try {
          var opts = Object.defineProperty({}, 'passive', {
            get: function get() {
              supportsPassive = true;
            }
          });
          window.addEventListener("test", null, opts);
        } catch (e) {}
        // Use our detect's results. passive applied if supported, capture will be false either way.
        var eventOptions = supportsPassive ? { passive: true } : false;
        // Bind touch handlers
        this.sliderElem.addEventListener("touchstart", this.touchstart, eventOptions);
        this.sliderElem.addEventListener("touchmove", this.touchmove, eventOptions);
      }
      this.sliderElem.addEventListener("mousedown", this.mousedown, false);

      // Bind window handlers
      this.resize = this._resize.bind(this);
      window.addEventListener("resize", this.resize, false);

      // Bind tooltip-related handlers
      if (this.options.tooltip === 'hide') {
        this._addClass(this.tooltip, 'hide');
        this._addClass(this.tooltip_min, 'hide');
        this._addClass(this.tooltip_max, 'hide');
      } else if (this.options.tooltip === 'always') {
        this._showTooltip();
        this._alwaysShowTooltip = true;
      } else {
        this.showTooltip = this._showTooltip.bind(this);
        this.hideTooltip = this._hideTooltip.bind(this);

        if (this.options.ticks_tooltip) {
          var callbackHandle = this._addTickListener();
          //create handle1 listeners and store references in map
          var mouseEnter = callbackHandle.addMouseEnter(this, this.handle1);
          var mouseLeave = callbackHandle.addMouseLeave(this, this.handle1);
          this.handleCallbackMap.handle1 = {
            mouseEnter: mouseEnter,
            mouseLeave: mouseLeave
          };
          //create handle2 listeners and store references in map
          mouseEnter = callbackHandle.addMouseEnter(this, this.handle2);
          mouseLeave = callbackHandle.addMouseLeave(this, this.handle2);
          this.handleCallbackMap.handle2 = {
            mouseEnter: mouseEnter,
            mouseLeave: mouseLeave
          };
        } else {
          this.sliderElem.addEventListener("mouseenter", this.showTooltip, false);
          this.sliderElem.addEventListener("mouseleave", this.hideTooltip, false);
        }

        this.handle1.addEventListener("focus", this.showTooltip, false);
        this.handle1.addEventListener("blur", this.hideTooltip, false);

        this.handle2.addEventListener("focus", this.showTooltip, false);
        this.handle2.addEventListener("blur", this.hideTooltip, false);
      }

      if (this.options.enabled) {
        this.enable();
      } else {
        this.disable();
      }
    }

    /*************************************************
          INSTANCE PROPERTIES/METHODS
    - Any methods bound to the prototype are considered
  part of the plugin's `public` interface
    **************************************************/
    Slider.prototype = {
      _init: function _init() {}, // NOTE: Must exist to support bridget

      constructor: Slider,

      defaultOptions: {
        id: "",
        min: 0,
        max: 10,
        step: 1,
        precision: 0,
        orientation: 'horizontal',
        value: 5,
        range: false,
        selection: 'before',
        tooltip: 'show',
        tooltip_split: false,
        handle: 'round',
        reversed: false,
        rtl: 'auto',
        enabled: true,
        formatter: function formatter(val) {
          if (Array.isArray(val)) {
            return val[0] + " : " + val[1];
          } else {
            return val;
          }
        },
        natural_arrow_keys: false,
        ticks: [],
        ticks_positions: [],
        ticks_labels: [],
        ticks_snap_bounds: 0,
        ticks_tooltip: false,
        scale: 'linear',
        focus: false,
        tooltip_position: null,
        labelledby: null,
        rangeHighlights: []
      },

      getElement: function getElement() {
        return this.sliderElem;
      },

      getValue: function getValue() {
        if (this.options.range) {
          return this._state.value;
        } else {
          return this._state.value[0];
        }
      },

      setValue: function setValue(val, triggerSlideEvent, triggerChangeEvent) {
        if (!val) {
          val = 0;
        }
        var oldValue = this.getValue();
        this._state.value = this._validateInputValue(val);
        var applyPrecision = this._applyPrecision.bind(this);

        if (this.options.range) {
          this._state.value[0] = applyPrecision(this._state.value[0]);
          this._state.value[1] = applyPrecision(this._state.value[1]);

          this._state.value[0] = Math.max(this.options.min, Math.min(this.options.max, this._state.value[0]));
          this._state.value[1] = Math.max(this.options.min, Math.min(this.options.max, this._state.value[1]));
        } else {
          this._state.value = applyPrecision(this._state.value);
          this._state.value = [Math.max(this.options.min, Math.min(this.options.max, this._state.value))];
          this._addClass(this.handle2, 'hide');
          if (this.options.selection === 'after') {
            this._state.value[1] = this.options.max;
          } else {
            this._state.value[1] = this.options.min;
          }
        }

        if (this.options.max > this.options.min) {
          this._state.percentage = [this._toPercentage(this._state.value[0]), this._toPercentage(this._state.value[1]), this.options.step * 100 / (this.options.max - this.options.min)];
        } else {
          this._state.percentage = [0, 0, 100];
        }

        this._layout();
        var newValue = this.options.range ? this._state.value : this._state.value[0];

        this._setDataVal(newValue);
        if (triggerSlideEvent === true) {
          this._trigger('slide', newValue);
        }
        if (oldValue !== newValue && triggerChangeEvent === true) {
          this._trigger('change', {
            oldValue: oldValue,
            newValue: newValue
          });
        }

        return this;
      },

      destroy: function destroy() {
        // Remove event handlers on slider elements
        this._removeSliderEventHandlers();

        // Remove the slider from the DOM
        this.sliderElem.parentNode.removeChild(this.sliderElem);
        /* Show original <input> element */
        this.element.style.display = "";

        // Clear out custom event bindings
        this._cleanUpEventCallbacksMap();

        // Remove data values
        this.element.removeAttribute("data");

        // Remove JQuery handlers/data
        if ($) {
          this._unbindJQueryEventHandlers();
          this.$element.removeData('slider');
        }
      },

      disable: function disable() {
        this._state.enabled = false;
        this.handle1.removeAttribute("tabindex");
        this.handle2.removeAttribute("tabindex");
        this._addClass(this.sliderElem, 'slider-disabled');
        this._trigger('slideDisabled');

        return this;
      },

      enable: function enable() {
        this._state.enabled = true;
        this.handle1.setAttribute("tabindex", 0);
        this.handle2.setAttribute("tabindex", 0);
        this._removeClass(this.sliderElem, 'slider-disabled');
        this._trigger('slideEnabled');

        return this;
      },

      toggle: function toggle() {
        if (this._state.enabled) {
          this.disable();
        } else {
          this.enable();
        }
        return this;
      },

      isEnabled: function isEnabled() {
        return this._state.enabled;
      },

      on: function on(evt, callback) {
        this._bindNonQueryEventHandler(evt, callback);
        return this;
      },

      off: function off(evt, callback) {
        if ($) {
          this.$element.off(evt, callback);
          this.$sliderElem.off(evt, callback);
        } else {
          this._unbindNonQueryEventHandler(evt, callback);
        }
      },

      getAttribute: function getAttribute(attribute) {
        if (attribute) {
          return this.options[attribute];
        } else {
          return this.options;
        }
      },

      setAttribute: function setAttribute(attribute, value) {
        this.options[attribute] = value;
        return this;
      },

      refresh: function refresh() {
        this._removeSliderEventHandlers();
        createNewSlider.call(this, this.element, this.options);
        if ($) {
          // Bind new instance of slider to the element
          $.data(this.element, 'slider', this);
        }
        return this;
      },

      relayout: function relayout() {
        this._resize();
        this._layout();
        return this;
      },

      /******************************+
          HELPERS
    - Any method that is not part of the public interface.
   - Place it underneath this comment block and write its signature like so:
      _fnName : function() {...}
    ********************************/
      _removeSliderEventHandlers: function _removeSliderEventHandlers() {
        // Remove keydown event listeners
        this.handle1.removeEventListener("keydown", this.handle1Keydown, false);
        this.handle2.removeEventListener("keydown", this.handle2Keydown, false);

        //remove the listeners from the ticks and handles if they had their own listeners
        if (this.options.ticks_tooltip) {
          var ticks = this.ticksContainer.getElementsByClassName('slider-tick');
          for (var i = 0; i < ticks.length; i++) {
            ticks[i].removeEventListener('mouseenter', this.ticksCallbackMap[i].mouseEnter, false);
            ticks[i].removeEventListener('mouseleave', this.ticksCallbackMap[i].mouseLeave, false);
          }
          this.handle1.removeEventListener('mouseenter', this.handleCallbackMap.handle1.mouseEnter, false);
          this.handle2.removeEventListener('mouseenter', this.handleCallbackMap.handle2.mouseEnter, false);
          this.handle1.removeEventListener('mouseleave', this.handleCallbackMap.handle1.mouseLeave, false);
          this.handle2.removeEventListener('mouseleave', this.handleCallbackMap.handle2.mouseLeave, false);
        }

        this.handleCallbackMap = null;
        this.ticksCallbackMap = null;

        if (this.showTooltip) {
          this.handle1.removeEventListener("focus", this.showTooltip, false);
          this.handle2.removeEventListener("focus", this.showTooltip, false);
        }
        if (this.hideTooltip) {
          this.handle1.removeEventListener("blur", this.hideTooltip, false);
          this.handle2.removeEventListener("blur", this.hideTooltip, false);
        }

        // Remove event listeners from sliderElem
        if (this.showTooltip) {
          this.sliderElem.removeEventListener("mouseenter", this.showTooltip, false);
        }
        if (this.hideTooltip) {
          this.sliderElem.removeEventListener("mouseleave", this.hideTooltip, false);
        }
        this.sliderElem.removeEventListener("touchstart", this.touchstart, false);
        this.sliderElem.removeEventListener("touchmove", this.touchmove, false);
        this.sliderElem.removeEventListener("mousedown", this.mousedown, false);

        // Remove window event listener
        window.removeEventListener("resize", this.resize, false);
      },
      _bindNonQueryEventHandler: function _bindNonQueryEventHandler(evt, callback) {
        if (this.eventToCallbackMap[evt] === undefined) {
          this.eventToCallbackMap[evt] = [];
        }
        this.eventToCallbackMap[evt].push(callback);
      },
      _unbindNonQueryEventHandler: function _unbindNonQueryEventHandler(evt, callback) {
        var callbacks = this.eventToCallbackMap[evt];
        if (callbacks !== undefined) {
          for (var i = 0; i < callbacks.length; i++) {
            if (callbacks[i] === callback) {
              callbacks.splice(i, 1);
              break;
            }
          }
        }
      },
      _cleanUpEventCallbacksMap: function _cleanUpEventCallbacksMap() {
        var eventNames = Object.keys(this.eventToCallbackMap);
        for (var i = 0; i < eventNames.length; i++) {
          var eventName = eventNames[i];
          delete this.eventToCallbackMap[eventName];
        }
      },
      _showTooltip: function _showTooltip() {
        if (this.options.tooltip_split === false) {
          this._addClass(this.tooltip, 'in');
          this.tooltip_min.style.display = 'none';
          this.tooltip_max.style.display = 'none';
        } else {
          this._addClass(this.tooltip_min, 'in');
          this._addClass(this.tooltip_max, 'in');
          this.tooltip.style.display = 'none';
        }
        this._state.over = true;
      },
      _hideTooltip: function _hideTooltip() {
        if (this._state.inDrag === false && this.alwaysShowTooltip !== true) {
          this._removeClass(this.tooltip, 'in');
          this._removeClass(this.tooltip_min, 'in');
          this._removeClass(this.tooltip_max, 'in');
        }
        this._state.over = false;
      },
      _setToolTipOnMouseOver: function _setToolTipOnMouseOver(tempState) {
        var formattedTooltipVal = this.options.formatter(!tempState ? this._state.value[0] : tempState.value[0]);
        var positionPercentages = !tempState ? getPositionPercentages(this._state, this.options.reversed) : getPositionPercentages(tempState, this.options.reversed);
        this._setText(this.tooltipInner, formattedTooltipVal);

        this.tooltip.style[this.stylePos] = positionPercentages[0] + "%";
        if (this.options.orientation === 'vertical') {
          this._css(this.tooltip, "margin-" + this.stylePos, -this.tooltip.offsetHeight / 2 + "px");
        } else {
          this._css(this.tooltip, "margin-" + this.stylePos, -this.tooltip.offsetWidth / 2 + "px");
        }

        function getPositionPercentages(state, reversed) {
          if (reversed) {
            return [100 - state.percentage[0], this.options.range ? 100 - state.percentage[1] : state.percentage[1]];
          }
          return [state.percentage[0], state.percentage[1]];
        }
      },
      _addTickListener: function _addTickListener() {
        return {
          addMouseEnter: function addMouseEnter(reference, tick, index) {
            var enter = function enter() {
              var tempState = reference._state;
              var idString = index >= 0 ? index : this.attributes['aria-valuenow'].value;
              var hoverIndex = parseInt(idString, 10);
              tempState.value[0] = hoverIndex;
              tempState.percentage[0] = reference.options.ticks_positions[hoverIndex];
              reference._setToolTipOnMouseOver(tempState);
              reference._showTooltip();
            };
            tick.addEventListener("mouseenter", enter, false);
            return enter;
          },
          addMouseLeave: function addMouseLeave(reference, tick) {
            var leave = function leave() {
              reference._hideTooltip();
            };
            tick.addEventListener("mouseleave", leave, false);
            return leave;
          }
        };
      },
      _layout: function _layout() {
        var positionPercentages;

        if (this.options.reversed) {
          positionPercentages = [100 - this._state.percentage[0], this.options.range ? 100 - this._state.percentage[1] : this._state.percentage[1]];
        } else {
          positionPercentages = [this._state.percentage[0], this._state.percentage[1]];
        }

        this.handle1.style[this.stylePos] = positionPercentages[0] + "%";
        this.handle1.setAttribute('aria-valuenow', this._state.value[0]);
        if (isNaN(this.options.formatter(this._state.value[0]))) {
          this.handle1.setAttribute('aria-valuetext', this.options.formatter(this._state.value[0]));
        }

        this.handle2.style[this.stylePos] = positionPercentages[1] + "%";
        this.handle2.setAttribute('aria-valuenow', this._state.value[1]);
        if (isNaN(this.options.formatter(this._state.value[1]))) {
          this.handle2.setAttribute('aria-valuetext', this.options.formatter(this._state.value[1]));
        }

        /* Position highlight range elements */
        if (this.rangeHighlightElements.length > 0 && Array.isArray(this.options.rangeHighlights) && this.options.rangeHighlights.length > 0) {
          for (var _i = 0; _i < this.options.rangeHighlights.length; _i++) {
            var startPercent = this._toPercentage(this.options.rangeHighlights[_i].start);
            var endPercent = this._toPercentage(this.options.rangeHighlights[_i].end);

            if (this.options.reversed) {
              var sp = 100 - endPercent;
              endPercent = 100 - startPercent;
              startPercent = sp;
            }

            var currentRange = this._createHighlightRange(startPercent, endPercent);

            if (currentRange) {
              if (this.options.orientation === 'vertical') {
                this.rangeHighlightElements[_i].style.top = currentRange.start + "%";
                this.rangeHighlightElements[_i].style.height = currentRange.size + "%";
              } else {
                if (this.options.rtl) {
                  this.rangeHighlightElements[_i].style.right = currentRange.start + "%";
                } else {
                  this.rangeHighlightElements[_i].style.left = currentRange.start + "%";
                }
                this.rangeHighlightElements[_i].style.width = currentRange.size + "%";
              }
            } else {
              this.rangeHighlightElements[_i].style.display = "none";
            }
          }
        }

        /* Position ticks and labels */
        if (Array.isArray(this.options.ticks) && this.options.ticks.length > 0) {

          var styleSize = this.options.orientation === 'vertical' ? 'height' : 'width';
          var styleMargin;
          if (this.options.orientation === 'vertical') {
            styleMargin = 'marginTop';
          } else {
            if (this.options.rtl) {
              styleMargin = 'marginRight';
            } else {
              styleMargin = 'marginLeft';
            }
          }
          var labelSize = this._state.size / (this.options.ticks.length - 1);

          if (this.tickLabelContainer) {
            var extraMargin = 0;
            if (this.options.ticks_positions.length === 0) {
              if (this.options.orientation !== 'vertical') {
                this.tickLabelContainer.style[styleMargin] = -labelSize / 2 + "px";
              }

              extraMargin = this.tickLabelContainer.offsetHeight;
            } else {
              /* Chidren are position absolute, calculate height by finding the max offsetHeight of a child */
              for (i = 0; i < this.tickLabelContainer.childNodes.length; i++) {
                if (this.tickLabelContainer.childNodes[i].offsetHeight > extraMargin) {
                  extraMargin = this.tickLabelContainer.childNodes[i].offsetHeight;
                }
              }
            }
            if (this.options.orientation === 'horizontal') {
              this.sliderElem.style.marginBottom = extraMargin + "px";
            }
          }
          for (var i = 0; i < this.options.ticks.length; i++) {

            var percentage = this.options.ticks_positions[i] || this._toPercentage(this.options.ticks[i]);

            if (this.options.reversed) {
              percentage = 100 - percentage;
            }

            this.ticks[i].style[this.stylePos] = percentage + "%";

            /* Set class labels to denote whether ticks are in the selection */
            this._removeClass(this.ticks[i], 'in-selection');
            if (!this.options.range) {
              if (this.options.selection === 'after' && percentage >= positionPercentages[0]) {
                this._addClass(this.ticks[i], 'in-selection');
              } else if (this.options.selection === 'before' && percentage <= positionPercentages[0]) {
                this._addClass(this.ticks[i], 'in-selection');
              }
            } else if (percentage >= positionPercentages[0] && percentage <= positionPercentages[1]) {
              this._addClass(this.ticks[i], 'in-selection');
            }

            if (this.tickLabels[i]) {
              this.tickLabels[i].style[styleSize] = labelSize + "px";

              if (this.options.orientation !== 'vertical' && this.options.ticks_positions[i] !== undefined) {
                this.tickLabels[i].style.position = 'absolute';
                this.tickLabels[i].style[this.stylePos] = percentage + "%";
                this.tickLabels[i].style[styleMargin] = -labelSize / 2 + 'px';
              } else if (this.options.orientation === 'vertical') {
                if (this.options.rtl) {
                  this.tickLabels[i].style['marginRight'] = this.sliderElem.offsetWidth + "px";
                } else {
                  this.tickLabels[i].style['marginLeft'] = this.sliderElem.offsetWidth + "px";
                }
                this.tickLabelContainer.style[styleMargin] = this.sliderElem.offsetWidth / 2 * -1 + 'px';
              }
            }
          }
        }

        var formattedTooltipVal;

        if (this.options.range) {
          formattedTooltipVal = this.options.formatter(this._state.value);
          this._setText(this.tooltipInner, formattedTooltipVal);
          this.tooltip.style[this.stylePos] = (positionPercentages[1] + positionPercentages[0]) / 2 + "%";

          if (this.options.orientation === 'vertical') {
            this._css(this.tooltip, "margin-" + this.stylePos, -this.tooltip.offsetHeight / 2 + "px");
          } else {
            this._css(this.tooltip, "margin-" + this.stylePos, -this.tooltip.offsetWidth / 2 + "px");
          }

          var innerTooltipMinText = this.options.formatter(this._state.value[0]);
          this._setText(this.tooltipInner_min, innerTooltipMinText);

          var innerTooltipMaxText = this.options.formatter(this._state.value[1]);
          this._setText(this.tooltipInner_max, innerTooltipMaxText);

          this.tooltip_min.style[this.stylePos] = positionPercentages[0] + "%";

          if (this.options.orientation === 'vertical') {
            this._css(this.tooltip_min, "margin-" + this.stylePos, -this.tooltip_min.offsetHeight / 2 + "px");
          } else {
            this._css(this.tooltip_min, "margin-" + this.stylePos, -this.tooltip_min.offsetWidth / 2 + "px");
          }

          this.tooltip_max.style[this.stylePos] = positionPercentages[1] + "%";

          if (this.options.orientation === 'vertical') {
            this._css(this.tooltip_max, "margin-" + this.stylePos, -this.tooltip_max.offsetHeight / 2 + "px");
          } else {
            this._css(this.tooltip_max, "margin-" + this.stylePos, -this.tooltip_max.offsetWidth / 2 + "px");
          }
        } else {
          formattedTooltipVal = this.options.formatter(this._state.value[0]);
          this._setText(this.tooltipInner, formattedTooltipVal);

          this.tooltip.style[this.stylePos] = positionPercentages[0] + "%";
          if (this.options.orientation === 'vertical') {
            this._css(this.tooltip, "margin-" + this.stylePos, -this.tooltip.offsetHeight / 2 + "px");
          } else {
            this._css(this.tooltip, "margin-" + this.stylePos, -this.tooltip.offsetWidth / 2 + "px");
          }
        }

        if (this.options.orientation === 'vertical') {
          this.trackLow.style.top = '0';
          this.trackLow.style.height = Math.min(positionPercentages[0], positionPercentages[1]) + '%';

          this.trackSelection.style.top = Math.min(positionPercentages[0], positionPercentages[1]) + '%';
          this.trackSelection.style.height = Math.abs(positionPercentages[0] - positionPercentages[1]) + '%';

          this.trackHigh.style.bottom = '0';
          this.trackHigh.style.height = 100 - Math.min(positionPercentages[0], positionPercentages[1]) - Math.abs(positionPercentages[0] - positionPercentages[1]) + '%';
        } else {
          if (this.stylePos === 'right') {
            this.trackLow.style.right = '0';
          } else {
            this.trackLow.style.left = '0';
          }
          this.trackLow.style.width = Math.min(positionPercentages[0], positionPercentages[1]) + '%';

          if (this.stylePos === 'right') {
            this.trackSelection.style.right = Math.min(positionPercentages[0], positionPercentages[1]) + '%';
          } else {
            this.trackSelection.style.left = Math.min(positionPercentages[0], positionPercentages[1]) + '%';
          }
          this.trackSelection.style.width = Math.abs(positionPercentages[0] - positionPercentages[1]) + '%';

          if (this.stylePos === 'right') {
            this.trackHigh.style.left = '0';
          } else {
            this.trackHigh.style.right = '0';
          }
          this.trackHigh.style.width = 100 - Math.min(positionPercentages[0], positionPercentages[1]) - Math.abs(positionPercentages[0] - positionPercentages[1]) + '%';

          var offset_min = this.tooltip_min.getBoundingClientRect();
          var offset_max = this.tooltip_max.getBoundingClientRect();

          if (this.options.tooltip_position === 'bottom') {
            if (offset_min.right > offset_max.left) {
              this._removeClass(this.tooltip_max, 'bottom');
              this._addClass(this.tooltip_max, 'top');
              this.tooltip_max.style.top = '';
              this.tooltip_max.style.bottom = 22 + 'px';
            } else {
              this._removeClass(this.tooltip_max, 'top');
              this._addClass(this.tooltip_max, 'bottom');
              this.tooltip_max.style.top = this.tooltip_min.style.top;
              this.tooltip_max.style.bottom = '';
            }
          } else {
            if (offset_min.right > offset_max.left) {
              this._removeClass(this.tooltip_max, 'top');
              this._addClass(this.tooltip_max, 'bottom');
              this.tooltip_max.style.top = 18 + 'px';
            } else {
              this._removeClass(this.tooltip_max, 'bottom');
              this._addClass(this.tooltip_max, 'top');
              this.tooltip_max.style.top = this.tooltip_min.style.top;
            }
          }
        }
      },
      _createHighlightRange: function _createHighlightRange(start, end) {
        if (this._isHighlightRange(start, end)) {
          if (start > end) {
            return { 'start': end, 'size': start - end };
          }
          return { 'start': start, 'size': end - start };
        }
        return null;
      },
      _isHighlightRange: function _isHighlightRange(start, end) {
        if (0 <= start && start <= 100 && 0 <= end && end <= 100) {
          return true;
        } else {
          return false;
        }
      },
      _resize: function _resize(ev) {
        /*jshint unused:false*/
        this._state.offset = this._offset(this.sliderElem);
        this._state.size = this.sliderElem[this.sizePos];
        this._layout();
      },
      _removeProperty: function _removeProperty(element, prop) {
        if (element.style.removeProperty) {
          element.style.removeProperty(prop);
        } else {
          element.style.removeAttribute(prop);
        }
      },
      _mousedown: function _mousedown(ev) {
        if (!this._state.enabled) {
          return false;
        }

        this._state.offset = this._offset(this.sliderElem);
        this._state.size = this.sliderElem[this.sizePos];

        var percentage = this._getPercentage(ev);

        if (this.options.range) {
          var diff1 = Math.abs(this._state.percentage[0] - percentage);
          var diff2 = Math.abs(this._state.percentage[1] - percentage);
          this._state.dragged = diff1 < diff2 ? 0 : 1;
          this._adjustPercentageForRangeSliders(percentage);
        } else {
          this._state.dragged = 0;
        }

        this._state.percentage[this._state.dragged] = percentage;
        this._layout();

        if (this.touchCapable) {
          document.removeEventListener("touchmove", this.mousemove, false);
          document.removeEventListener("touchend", this.mouseup, false);
        }

        if (this.mousemove) {
          document.removeEventListener("mousemove", this.mousemove, false);
        }
        if (this.mouseup) {
          document.removeEventListener("mouseup", this.mouseup, false);
        }

        this.mousemove = this._mousemove.bind(this);
        this.mouseup = this._mouseup.bind(this);

        if (this.touchCapable) {
          // Touch: Bind touch events:
          document.addEventListener("touchmove", this.mousemove, false);
          document.addEventListener("touchend", this.mouseup, false);
        }
        // Bind mouse events:
        document.addEventListener("mousemove", this.mousemove, false);
        document.addEventListener("mouseup", this.mouseup, false);

        this._state.inDrag = true;
        var newValue = this._calculateValue();

        this._trigger('slideStart', newValue);

        this._setDataVal(newValue);
        this.setValue(newValue, false, true);

        ev.returnValue = false;

        if (this.options.focus) {
          this._triggerFocusOnHandle(this._state.dragged);
        }

        return true;
      },
      _touchstart: function _touchstart(ev) {
        if (ev.changedTouches === undefined) {
          this._mousedown(ev);
          return;
        }

        var touch = ev.changedTouches[0];
        this.touchX = touch.pageX;
        this.touchY = touch.pageY;
      },
      _triggerFocusOnHandle: function _triggerFocusOnHandle(handleIdx) {
        if (handleIdx === 0) {
          this.handle1.focus();
        }
        if (handleIdx === 1) {
          this.handle2.focus();
        }
      },
      _keydown: function _keydown(handleIdx, ev) {
        if (!this._state.enabled) {
          return false;
        }

        var dir;
        switch (ev.keyCode) {
          case 37: // left
          case 40:
            // down
            dir = -1;
            break;
          case 39: // right
          case 38:
            // up
            dir = 1;
            break;
        }
        if (!dir) {
          return;
        }

        // use natural arrow keys instead of from min to max
        if (this.options.natural_arrow_keys) {
          var ifVerticalAndNotReversed = this.options.orientation === 'vertical' && !this.options.reversed;
          var ifHorizontalAndReversed = this.options.orientation === 'horizontal' && this.options.reversed; // @todo control with rtl

          if (ifVerticalAndNotReversed || ifHorizontalAndReversed) {
            dir = -dir;
          }
        }

        var val = this._state.value[handleIdx] + dir * this.options.step;
        var percentage = val / this.options.max * 100;
        this._state.keyCtrl = handleIdx;
        if (this.options.range) {
          this._adjustPercentageForRangeSliders(percentage);
          var val1 = !this._state.keyCtrl ? val : this._state.value[0];
          var val2 = this._state.keyCtrl ? val : this._state.value[1];
          val = [val1, val2];
        }

        this._trigger('slideStart', val);
        this._setDataVal(val);
        this.setValue(val, true, true);

        this._setDataVal(val);
        this._trigger('slideStop', val);
        this._layout();

        this._pauseEvent(ev);
        delete this._state.keyCtrl;

        return false;
      },
      _pauseEvent: function _pauseEvent(ev) {
        if (ev.stopPropagation) {
          ev.stopPropagation();
        }
        if (ev.preventDefault) {
          ev.preventDefault();
        }
        ev.cancelBubble = true;
        ev.returnValue = false;
      },
      _mousemove: function _mousemove(ev) {
        if (!this._state.enabled) {
          return false;
        }

        var percentage = this._getPercentage(ev);
        this._adjustPercentageForRangeSliders(percentage);
        this._state.percentage[this._state.dragged] = percentage;
        this._layout();

        var val = this._calculateValue(true);
        this.setValue(val, true, true);

        return false;
      },
      _touchmove: function _touchmove(ev) {
        if (ev.changedTouches === undefined) {
          return;
        }

        var touch = ev.changedTouches[0];

        var xDiff = touch.pageX - this.touchX;
        var yDiff = touch.pageY - this.touchY;

        if (!this._state.inDrag) {
          // Vertical Slider
          if (this.options.orientation === 'vertical' && xDiff <= 5 && xDiff >= -5 && (yDiff >= 15 || yDiff <= -15)) {
            this._mousedown(ev);
          }
          // Horizontal slider.
          else if (yDiff <= 5 && yDiff >= -5 && (xDiff >= 15 || xDiff <= -15)) {
              this._mousedown(ev);
            }
        }
      },
      _adjustPercentageForRangeSliders: function _adjustPercentageForRangeSliders(percentage) {
        if (this.options.range) {
          var precision = this._getNumDigitsAfterDecimalPlace(percentage);
          precision = precision ? precision - 1 : 0;
          var percentageWithAdjustedPrecision = this._applyToFixedAndParseFloat(percentage, precision);
          if (this._state.dragged === 0 && this._applyToFixedAndParseFloat(this._state.percentage[1], precision) < percentageWithAdjustedPrecision) {
            this._state.percentage[0] = this._state.percentage[1];
            this._state.dragged = 1;
          } else if (this._state.dragged === 1 && this._applyToFixedAndParseFloat(this._state.percentage[0], precision) > percentageWithAdjustedPrecision) {
            this._state.percentage[1] = this._state.percentage[0];
            this._state.dragged = 0;
          } else if (this._state.keyCtrl === 0 && this._state.value[1] / this.options.max * 100 < percentage) {
            this._state.percentage[0] = this._state.percentage[1];
            this._state.keyCtrl = 1;
            this.handle2.focus();
          } else if (this._state.keyCtrl === 1 && this._state.value[0] / this.options.max * 100 > percentage) {
            this._state.percentage[1] = this._state.percentage[0];
            this._state.keyCtrl = 0;
            this.handle1.focus();
          }
        }
      },
      _mouseup: function _mouseup() {
        if (!this._state.enabled) {
          return false;
        }
        if (this.touchCapable) {
          // Touch: Unbind touch event handlers:
          document.removeEventListener("touchmove", this.mousemove, false);
          document.removeEventListener("touchend", this.mouseup, false);
        }
        // Unbind mouse event handlers:
        document.removeEventListener("mousemove", this.mousemove, false);
        document.removeEventListener("mouseup", this.mouseup, false);

        this._state.inDrag = false;
        if (this._state.over === false) {
          this._hideTooltip();
        }
        var val = this._calculateValue(true);

        this._layout();
        this._setDataVal(val);
        this._trigger('slideStop', val);

        return false;
      },
      _calculateValue: function _calculateValue(snapToClosestTick) {
        var val;
        if (this.options.range) {
          val = [this.options.min, this.options.max];
          if (this._state.percentage[0] !== 0) {
            val[0] = this._toValue(this._state.percentage[0]);
            val[0] = this._applyPrecision(val[0]);
          }
          if (this._state.percentage[1] !== 100) {
            val[1] = this._toValue(this._state.percentage[1]);
            val[1] = this._applyPrecision(val[1]);
          }
        } else {
          val = this._toValue(this._state.percentage[0]);
          val = parseFloat(val);
          val = this._applyPrecision(val);
        }

        if (snapToClosestTick) {
          var min = [val, Infinity];
          for (var i = 0; i < this.options.ticks.length; i++) {
            var diff = Math.abs(this.options.ticks[i] - val);
            if (diff <= min[1]) {
              min = [this.options.ticks[i], diff];
            }
          }
          if (min[1] <= this.options.ticks_snap_bounds) {
            return min[0];
          }
        }

        return val;
      },
      _applyPrecision: function _applyPrecision(val) {
        var precision = this.options.precision || this._getNumDigitsAfterDecimalPlace(this.options.step);
        return this._applyToFixedAndParseFloat(val, precision);
      },
      _getNumDigitsAfterDecimalPlace: function _getNumDigitsAfterDecimalPlace(num) {
        var match = ('' + num).match(/(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/);
        if (!match) {
          return 0;
        }
        return Math.max(0, (match[1] ? match[1].length : 0) - (match[2] ? +match[2] : 0));
      },
      _applyToFixedAndParseFloat: function _applyToFixedAndParseFloat(num, toFixedInput) {
        var truncatedNum = num.toFixed(toFixedInput);
        return parseFloat(truncatedNum);
      },
      /*
    Credits to Mike Samuel for the following method!
    Source: http://stackoverflow.com/questions/10454518/javascript-how-to-retrieve-the-number-of-decimals-of-a-string-number
   */
      _getPercentage: function _getPercentage(ev) {
        if (this.touchCapable && (ev.type === 'touchstart' || ev.type === 'touchmove')) {
          ev = ev.touches[0];
        }

        var eventPosition = ev[this.mousePos];
        var sliderOffset = this._state.offset[this.stylePos];
        var distanceToSlide = eventPosition - sliderOffset;
        if (this.stylePos === 'right') {
          distanceToSlide = -distanceToSlide;
        }
        // Calculate what percent of the length the slider handle has slid
        var percentage = distanceToSlide / this._state.size * 100;
        percentage = Math.round(percentage / this._state.percentage[2]) * this._state.percentage[2];
        if (this.options.reversed) {
          percentage = 100 - percentage;
        }

        // Make sure the percent is within the bounds of the slider.
        // 0% corresponds to the 'min' value of the slide
        // 100% corresponds to the 'max' value of the slide
        return Math.max(0, Math.min(100, percentage));
      },
      _validateInputValue: function _validateInputValue(val) {
        if (!isNaN(+val)) {
          return +val;
        } else if (Array.isArray(val)) {
          this._validateArray(val);
          return val;
        } else {
          throw new Error(ErrorMsgs.formatInvalidInputErrorMsg(val));
        }
      },
      _validateArray: function _validateArray(val) {
        for (var i = 0; i < val.length; i++) {
          var input = val[i];
          if (typeof input !== 'number') {
            throw new Error(ErrorMsgs.formatInvalidInputErrorMsg(input));
          }
        }
      },
      _setDataVal: function _setDataVal(val) {
        this.element.setAttribute('data-value', val);
        this.element.setAttribute('value', val);
        this.element.value = val;
      },
      _trigger: function _trigger(evt, val) {
        val = val || val === 0 ? val : undefined;

        var callbackFnArray = this.eventToCallbackMap[evt];
        if (callbackFnArray && callbackFnArray.length) {
          for (var i = 0; i < callbackFnArray.length; i++) {
            var callbackFn = callbackFnArray[i];
            callbackFn(val);
          }
        }

        /* If JQuery exists, trigger JQuery events */
        if ($) {
          this._triggerJQueryEvent(evt, val);
        }
      },
      _triggerJQueryEvent: function _triggerJQueryEvent(evt, val) {
        var eventData = {
          type: evt,
          value: val
        };
        this.$element.trigger(eventData);
        this.$sliderElem.trigger(eventData);
      },
      _unbindJQueryEventHandlers: function _unbindJQueryEventHandlers() {
        this.$element.off();
        this.$sliderElem.off();
      },
      _setText: function _setText(element, text) {
        if (typeof element.textContent !== "undefined") {
          element.textContent = text;
        } else if (typeof element.innerText !== "undefined") {
          element.innerText = text;
        }
      },
      _removeClass: function _removeClass(element, classString) {
        var classes = classString.split(" ");
        var newClasses = element.className;

        for (var i = 0; i < classes.length; i++) {
          var classTag = classes[i];
          var regex = new RegExp("(?:\\s|^)" + classTag + "(?:\\s|$)");
          newClasses = newClasses.replace(regex, " ");
        }

        element.className = newClasses.trim();
      },
      _addClass: function _addClass(element, classString) {
        var classes = classString.split(" ");
        var newClasses = element.className;

        for (var i = 0; i < classes.length; i++) {
          var classTag = classes[i];
          var regex = new RegExp("(?:\\s|^)" + classTag + "(?:\\s|$)");
          var ifClassExists = regex.test(newClasses);

          if (!ifClassExists) {
            newClasses += " " + classTag;
          }
        }

        element.className = newClasses.trim();
      },
      _offsetLeft: function _offsetLeft(obj) {
        return obj.getBoundingClientRect().left;
      },
      _offsetRight: function _offsetRight(obj) {
        return obj.getBoundingClientRect().right;
      },
      _offsetTop: function _offsetTop(obj) {
        var offsetTop = obj.offsetTop;
        while ((obj = obj.offsetParent) && !isNaN(obj.offsetTop)) {
          offsetTop += obj.offsetTop;
          if (obj.tagName !== 'BODY') {
            offsetTop -= obj.scrollTop;
          }
        }
        return offsetTop;
      },
      _offset: function _offset(obj) {
        return {
          left: this._offsetLeft(obj),
          right: this._offsetRight(obj),
          top: this._offsetTop(obj)
        };
      },
      _css: function _css(elementRef, styleName, value) {
        if ($) {
          $.style(elementRef, styleName, value);
        } else {
          var style = styleName.replace(/^-ms-/, "ms-").replace(/-([\da-z])/gi, function (all, letter) {
            return letter.toUpperCase();
          });
          elementRef.style[style] = value;
        }
      },
      _toValue: function _toValue(percentage) {
        return this.options.scale.toValue.apply(this, [percentage]);
      },
      _toPercentage: function _toPercentage(value) {
        return this.options.scale.toPercentage.apply(this, [value]);
      },
      _setTooltipPosition: function _setTooltipPosition() {
        var tooltips = [this.tooltip, this.tooltip_min, this.tooltip_max];
        if (this.options.orientation === 'vertical') {
          var tooltipPos;
          if (this.options.tooltip_position) {
            tooltipPos = this.options.tooltip_position;
          } else {
            if (this.options.rtl) {
              tooltipPos = 'left';
            } else {
              tooltipPos = 'right';
            }
          }
          var oppositeSide = tooltipPos === 'left' ? 'right' : 'left';
          tooltips.forEach(function (tooltip) {
            this._addClass(tooltip, tooltipPos);
            tooltip.style[oppositeSide] = '100%';
          }.bind(this));
        } else if (this.options.tooltip_position === 'bottom') {
          tooltips.forEach(function (tooltip) {
            this._addClass(tooltip, 'bottom');
            tooltip.style.top = 22 + 'px';
          }.bind(this));
        } else {
          tooltips.forEach(function (tooltip) {
            this._addClass(tooltip, 'top');
            tooltip.style.top = -this.tooltip.outerHeight - 14 + 'px';
          }.bind(this));
        }
      }
    };

    /*********************************
      Attach to global namespace
    *********************************/
    if ($ && $.fn) {
      var autoRegisterNamespace = void 0;

      if (!$.fn.slider) {
        $.bridget(NAMESPACE_MAIN, Slider);
        autoRegisterNamespace = NAMESPACE_MAIN;
      } else {
        if (windowIsDefined) {
          window.console.warn("bootstrap-slider.js - WARNING: $.fn.slider namespace is already bound. Use the $.fn.bootstrapSlider namespace instead.");
        }
        autoRegisterNamespace = NAMESPACE_ALTERNATE;
      }
      $.bridget(NAMESPACE_ALTERNATE, Slider);

      // Auto-Register data-provide="slider" Elements
      $(function () {
        $("input[data-provide=slider]")[autoRegisterNamespace]();
      });
    }
  })($);

  return Slider;
});

 /* ================== Bootstrap-slider JS ends here ============================*/

 /* ========================================================================
  =================== Light Gallery JS starts HERE =========================
 * ======================================================================== */


(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define(['jquery'], function (a0) {
      return (factory(a0));
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory(require('jquery'));
  } else {
    factory(root["jQuery"]);
  }
}(this, function ($) {

(function() {
    'use strict';

    var defaults = {

        mode: 'lg-slide',

        // Ex : 'ease'
        cssEasing: 'ease',

        //'for jquery animation'
        easing: 'linear',
        speed: 600,
        height: '100%',
        width: '100%',
        addClass: '',
        startClass: 'lg-start-zoom',
        backdropDuration: 150,
        hideBarsDelay: 6000,

        useLeft: false,

        closable: true,
        loop: true,
        escKey: true,
        keyPress: true,
        controls: true,
        slideEndAnimatoin: true,
        hideControlOnEnd: false,
        mousewheel: true,

        getCaptionFromTitleOrAlt: true,

        // .lg-item || '.lg-sub-html'
        appendSubHtmlTo: '.lg-sub-html',

        subHtmlSelectorRelative: false,

        preload: 1,
        showAfterLoad: true,
        selector: '',
        selectWithin: '',
        nextHtml: '',
        prevHtml: '',

        // 0, 1
        index: false,

        iframeMaxWidth: '100%',

        download: true,
        counter: true,
        appendCounterTo: '.lg-toolbar',

        swipeThreshold: 50,
        enableSwipe: true,
        enableDrag: true,

        dynamic: false,
        dynamicEl: [],
        galleryId: 1
    };

    function Plugin(element, options) {

        // Current lightGallery element
        this.el = element;

        // Current jquery element
        this.$el = $(element);

        // lightGallery settings
        this.s = $.extend({}, defaults, options);

        // When using dynamic mode, ensure dynamicEl is an array
        if (this.s.dynamic && this.s.dynamicEl !== 'undefined' && this.s.dynamicEl.constructor === Array && !this.s.dynamicEl.length) {
            throw ('When using dynamic mode, you must also define dynamicEl as an Array.');
        }

        // lightGallery modules
        this.modules = {};

        // false when lightgallery complete first slide;
        this.lGalleryOn = false;

        this.lgBusy = false;

        // Timeout function for hiding controls;
        this.hideBartimeout = false;

        // To determine browser supports for touch events;
        this.isTouch = ('ontouchstart' in document.documentElement);

        // Disable hideControlOnEnd if sildeEndAnimation is true
        if (this.s.slideEndAnimatoin) {
            this.s.hideControlOnEnd = false;
        }

        // Gallery items
        if (this.s.dynamic) {
            this.$items = this.s.dynamicEl;
        } else {
            if (this.s.selector === 'this') {
                this.$items = this.$el;
            } else if (this.s.selector !== '') {
                if (this.s.selectWithin) {
                    this.$items = $(this.s.selectWithin).find(this.s.selector);
                } else {
                    this.$items = this.$el.find($(this.s.selector));
                }
            } else {
                this.$items = this.$el.children();
            }
        }

        // .lg-item
        this.$slide = '';

        // .lg-outer
        this.$outer = '';

        this.init();

        return this;
    }

    Plugin.prototype.init = function() {

        var _this = this;

        // s.preload should not be more than $item.length
        if (_this.s.preload > _this.$items.length) {
            _this.s.preload = _this.$items.length;
        }

        // if dynamic option is enabled execute immediately
        var _hash = window.location.hash;
        if (_hash.indexOf('lg=' + this.s.galleryId) > 0) {

            _this.index = parseInt(_hash.split('&slide=')[1], 10);

            $('body').addClass('lg-from-hash');
            if (!$('body').hasClass('lg-on')) {
                setTimeout(function() {
                    _this.build(_this.index);
                });

                $('body').addClass('lg-on');
            }
        }

        if (_this.s.dynamic) {

            _this.$el.trigger('onBeforeOpen.lg');

            _this.index = _this.s.index || 0;

            // prevent accidental double execution
            if (!$('body').hasClass('lg-on')) {
                setTimeout(function() {
                    _this.build(_this.index);
                    $('body').addClass('lg-on');
                });
            }
        } else {

            // Using different namespace for click because click event should not unbind if selector is same object('this')
            _this.$items.on('click.lgcustom', function(event) {

                // For IE8
                try {
                    event.preventDefault();
                    event.preventDefault();
                } catch (er) {
                    event.returnValue = false;
                }

                _this.$el.trigger('onBeforeOpen.lg');

                _this.index = _this.s.index || _this.$items.index(this);

                // prevent accidental double execution
                if (!$('body').hasClass('lg-on')) {
                    _this.build(_this.index);
                    $('body').addClass('lg-on');
                }
            });
        }

    };

    Plugin.prototype.build = function(index) {

        var _this = this;

        _this.structure();

        // module constructor
        $.each($.fn.lightGallery.modules, function(key) {
            _this.modules[key] = new $.fn.lightGallery.modules[key](_this.el);
        });

        // initiate slide function
        _this.slide(index, false, false, false);

        if (_this.s.keyPress) {
            _this.keyPress();
        }

        if (_this.$items.length > 1) {

            _this.arrow();

            setTimeout(function() {
                _this.enableDrag();
                _this.enableSwipe();
            }, 50);

            if (_this.s.mousewheel) {
                _this.mousewheel();
            }
        } else {
            _this.$slide.on('click.lg', function() {
                _this.$el.trigger('onSlideClick.lg');
            });
        }

        _this.counter();

        _this.closeGallery();

        _this.$el.trigger('onAfterOpen.lg');

        // Hide controllers if mouse doesn't move for some period
        _this.$outer.on('mousemove.lg click.lg touchstart.lg', function() {

            _this.$outer.removeClass('lg-hide-items');

            clearTimeout(_this.hideBartimeout);

            // Timeout will be cleared on each slide movement also
            _this.hideBartimeout = setTimeout(function() {
                _this.$outer.addClass('lg-hide-items');
            }, _this.s.hideBarsDelay);

        });

        _this.$outer.trigger('mousemove.lg');

    };

    Plugin.prototype.structure = function() {
        var list = '';
        var controls = '';
        var i = 0;
        var subHtmlCont = '';
        var template;
        var _this = this;

        $('body').append('<div class="lg-backdrop"></div>');
        $('.lg-backdrop').css('transition-duration', this.s.backdropDuration + 'ms');

        // Create gallery items
        for (i = 0; i < this.$items.length; i++) {
            list += '<div class="lg-item"></div>';
        }

        // Create controlls
        if (this.s.controls && this.$items.length > 1) {
            controls = '<div class="lg-actions">' +
                '<button class="lg-prev lg-icon">' + this.s.prevHtml + '</button>' +
                '<button class="lg-next lg-icon">' + this.s.nextHtml + '</button>' +
                '</div>';
        }

        if (this.s.appendSubHtmlTo === '.lg-sub-html') {
            subHtmlCont = '<div class="lg-sub-html"></div>';
        }

        template = '<div class="lg-outer ' + this.s.addClass + ' ' + this.s.startClass + '">' +
            '<div class="lg" style="width:' + this.s.width + '; height:' + this.s.height + '">' +
            '<div class="lg-inner">' + list + '</div>' +
            '<div class="lg-toolbar lg-group">' +
            '<span class="lg-close lg-icon"></span>' +
            '</div>' +
            controls +
            subHtmlCont +
            '</div>' +
            '</div>';

        $('body').append(template);
        this.$outer = $('.lg-outer');
        this.$slide = this.$outer.find('.lg-item');

        if (this.s.useLeft) {
            this.$outer.addClass('lg-use-left');

            // Set mode lg-slide if use left is true;
            this.s.mode = 'lg-slide';
        } else {
            this.$outer.addClass('lg-use-css3');
        }

        // For fixed height gallery
        _this.setTop();
        $(window).on('resize.lg orientationchange.lg', function() {
            setTimeout(function() {
                _this.setTop();
            }, 100);
        });

        // add class lg-current to remove initial transition
        this.$slide.eq(this.index).addClass('lg-current');

        // add Class for css support and transition mode
        if (this.doCss()) {
            this.$outer.addClass('lg-css3');
        } else {
            this.$outer.addClass('lg-css');

            // Set speed 0 because no animation will happen if browser doesn't support css3
            this.s.speed = 0;
        }

        this.$outer.addClass(this.s.mode);

        if (this.s.enableDrag && this.$items.length > 1) {
            this.$outer.addClass('lg-grab');
        }

        if (this.s.showAfterLoad) {
            this.$outer.addClass('lg-show-after-load');
        }

        if (this.doCss()) {
            var $inner = this.$outer.find('.lg-inner');
            $inner.css('transition-timing-function', this.s.cssEasing);
            $inner.css('transition-duration', this.s.speed + 'ms');
        }

        setTimeout(function() {
            $('.lg-backdrop').addClass('in');
        });

        setTimeout(function() {
            _this.$outer.addClass('lg-visible');
        }, this.s.backdropDuration);

        if (this.s.download) {
            this.$outer.find('.lg-toolbar').append('<a id="lg-download" target="_blank" download class="lg-download lg-icon"></a>');
        }

        // Store the current scroll top value to scroll back after closing the gallery..
        this.prevScrollTop = $(window).scrollTop();

    };

    // For fixed height gallery
    Plugin.prototype.setTop = function() {
        if (this.s.height !== '100%') {
            var wH = $(window).height();
            var top = (wH - parseInt(this.s.height, 10)) / 2;
            var $lGallery = this.$outer.find('.lg');
            if (wH >= parseInt(this.s.height, 10)) {
                $lGallery.css('top', top + 'px');
            } else {
                $lGallery.css('top', '0px');
            }
        }
    };

    // Find css3 support
    Plugin.prototype.doCss = function() {
        // check for css animation support
        var support = function() {
            var transition = ['transition', 'MozTransition', 'WebkitTransition', 'OTransition', 'msTransition', 'KhtmlTransition'];
            var root = document.documentElement;
            var i = 0;
            for (i = 0; i < transition.length; i++) {
                if (transition[i] in root.style) {
                    return true;
                }
            }
        };

        if (support()) {
            return true;
        }

        return false;
    };

    /**
     *  @desc Check the given src is video
     *  @param {String} src
     *  @return {Object} video type
     *  Ex:{ youtube  :  ["//www.youtube.com/watch?v=c0asJgSyxcY", "c0asJgSyxcY"] }
     */
    Plugin.prototype.isVideo = function(src, index) {

        var html;
        if (this.s.dynamic) {
            html = this.s.dynamicEl[index].html;
        } else {
            html = this.$items.eq(index).attr('data-html');
        }

        if (!src) {
            if(html) {
                return {
                    html5: true
                };
            } else {
                console.error('lightGallery :- data-src is not pvovided on slide item ' + (index + 1) + '. Please make sure the selector property is properly configured. More info - http://sachinchoolur.github.io/lightGallery/demos/html-markup.html');
                return false;
            }
        }

        var youtube = src.match(/\/\/(?:www\.)?youtu(?:\.be|be\.com)\/(?:watch\?v=|embed\/)?([a-z0-9\-\_\%]+)/i);
        var vimeo = src.match(/\/\/(?:www\.)?vimeo.com\/([0-9a-z\-_]+)/i);
        var dailymotion = src.match(/\/\/(?:www\.)?dai.ly\/([0-9a-z\-_]+)/i);
        var vk = src.match(/\/\/(?:www\.)?(?:vk\.com|vkontakte\.ru)\/(?:video_ext\.php\?)(.*)/i);

        if (youtube) {
            return {
                youtube: youtube
            };
        } else if (vimeo) {
            return {
                vimeo: vimeo
            };
        } else if (dailymotion) {
            return {
                dailymotion: dailymotion
            };
        } else if (vk) {
            return {
                vk: vk
            };
        }
    };

    /**
     *  @desc Create image counter
     *  Ex: 1/10
     */
    Plugin.prototype.counter = function() {
        if (this.s.counter) {
            $(this.s.appendCounterTo).append('<div id="lg-counter"><span id="lg-counter-current">' + (parseInt(this.index, 10) + 1) + '</span> / <span id="lg-counter-all">' + this.$items.length + '</span></div>');
        }
    };

    /**
     *  @desc add sub-html into the slide
     *  @param {Number} index - index of the slide
     */
    Plugin.prototype.addHtml = function(index) {
        var subHtml = null;
        var subHtmlUrl;
        var $currentEle;
        if (this.s.dynamic) {
            if (this.s.dynamicEl[index].subHtmlUrl) {
                subHtmlUrl = this.s.dynamicEl[index].subHtmlUrl;
            } else {
                subHtml = this.s.dynamicEl[index].subHtml;
            }
        } else {
            $currentEle = this.$items.eq(index);
            if ($currentEle.attr('data-sub-html-url')) {
                subHtmlUrl = $currentEle.attr('data-sub-html-url');
            } else {
                subHtml = $currentEle.attr('data-sub-html');
                if (this.s.getCaptionFromTitleOrAlt && !subHtml) {
                    subHtml = $currentEle.attr('title') || $currentEle.find('img').first().attr('alt');
                }
            }
        }

        if (!subHtmlUrl) {
            if (typeof subHtml !== 'undefined' && subHtml !== null) {

                // get first letter of subhtml
                // if first letter starts with . or # get the html form the jQuery object
                var fL = subHtml.substring(0, 1);
                if (fL === '.' || fL === '#') {
                    if (this.s.subHtmlSelectorRelative && !this.s.dynamic) {
                        subHtml = $currentEle.find(subHtml).html();
                    } else {
                        subHtml = $(subHtml).html();
                    }
                }
            } else {
                subHtml = '';
            }
        }

        if (this.s.appendSubHtmlTo === '.lg-sub-html') {

            if (subHtmlUrl) {
                this.$outer.find(this.s.appendSubHtmlTo).load(subHtmlUrl);
            } else {
                this.$outer.find(this.s.appendSubHtmlTo).html(subHtml);
            }

        } else {

            if (subHtmlUrl) {
                this.$slide.eq(index).load(subHtmlUrl);
            } else {
                this.$slide.eq(index).append(subHtml);
            }
        }

        // Add lg-empty-html class if title doesn't exist
        if (typeof subHtml !== 'undefined' && subHtml !== null) {
            if (subHtml === '') {
                this.$outer.find(this.s.appendSubHtmlTo).addClass('lg-empty-html');
            } else {
                this.$outer.find(this.s.appendSubHtmlTo).removeClass('lg-empty-html');
            }
        }

        this.$el.trigger('onAfterAppendSubHtml.lg', [index]);
    };

    /**
     *  @desc Preload slides
     *  @param {Number} index - index of the slide
     */
    Plugin.prototype.preload = function(index) {
        var i = 1;
        var j = 1;
        for (i = 1; i <= this.s.preload; i++) {
            if (i >= this.$items.length - index) {
                break;
            }

            this.loadContent(index + i, false, 0);
        }

        for (j = 1; j <= this.s.preload; j++) {
            if (index - j < 0) {
                break;
            }

            this.loadContent(index - j, false, 0);
        }
    };


    Plugin.prototype.loadContent = function(index, rec, delay) {

        var _this = this;
        var _hasPoster = false;
        var _$img;
        var _src;
        var _poster;
        var _srcset;
        var _sizes;
        var _html;
        var getResponsiveSrc = function(srcItms) {
            var rsWidth = [];
            var rsSrc = [];
            for (var i = 0; i < srcItms.length; i++) {
                var __src = srcItms[i].split(' ');

                // Manage empty space
                if (__src[0] === '') {
                    __src.splice(0, 1);
                }

                rsSrc.push(__src[0]);
                rsWidth.push(__src[1]);
            }

            var wWidth = $(window).width();
            for (var j = 0; j < rsWidth.length; j++) {
                if (parseInt(rsWidth[j], 10) > wWidth) {
                    _src = rsSrc[j];
                    break;
                }
            }
        };

        if (_this.s.dynamic) {

            if (_this.s.dynamicEl[index].poster) {
                _hasPoster = true;
                _poster = _this.s.dynamicEl[index].poster;
            }

            _html = _this.s.dynamicEl[index].html;
            _src = _this.s.dynamicEl[index].src;

            if (_this.s.dynamicEl[index].responsive) {
                var srcDyItms = _this.s.dynamicEl[index].responsive.split(',');
                getResponsiveSrc(srcDyItms);
            }

            _srcset = _this.s.dynamicEl[index].srcset;
            _sizes = _this.s.dynamicEl[index].sizes;

        } else {

            if (_this.$items.eq(index).attr('data-poster')) {
                _hasPoster = true;
                _poster = _this.$items.eq(index).attr('data-poster');
            }

            _html = _this.$items.eq(index).attr('data-html');
            _src = _this.$items.eq(index).attr('href') || _this.$items.eq(index).attr('data-src');

            if (_this.$items.eq(index).attr('data-responsive')) {
                var srcItms = _this.$items.eq(index).attr('data-responsive').split(',');
                getResponsiveSrc(srcItms);
            }

            _srcset = _this.$items.eq(index).attr('data-srcset');
            _sizes = _this.$items.eq(index).attr('data-sizes');

        }

        //if (_src || _srcset || _sizes || _poster) {

        var iframe = false;
        if (_this.s.dynamic) {
            if (_this.s.dynamicEl[index].iframe) {
                iframe = true;
            }
        } else {
            if (_this.$items.eq(index).attr('data-iframe') === 'true') {
                iframe = true;
            }
        }

        var _isVideo = _this.isVideo(_src, index);
        if (!_this.$slide.eq(index).hasClass('lg-loaded')) {
            if (iframe) {
                _this.$slide.eq(index).prepend('<div class="lg-video-cont lg-has-iframe" style="max-width:' + _this.s.iframeMaxWidth + '"><div class="lg-video"><iframe class="lg-object" frameborder="0" src="' + _src + '"  allowfullscreen="true"></iframe></div></div>');
            } else if (_hasPoster) {
                var videoClass = '';
                if (_isVideo && _isVideo.youtube) {
                    videoClass = 'lg-has-youtube';
                } else if (_isVideo && _isVideo.vimeo) {
                    videoClass = 'lg-has-vimeo';
                } else {
                    videoClass = 'lg-has-html5';
                }

                _this.$slide.eq(index).prepend('<div class="lg-video-cont ' + videoClass + ' "><div class="lg-video"><span class="lg-video-play"></span><img class="lg-object lg-has-poster" src="' + _poster + '" /></div></div>');

            } else if (_isVideo) {
                _this.$slide.eq(index).prepend('<div class="lg-video-cont "><div class="lg-video"></div></div>');
                _this.$el.trigger('hasVideo.lg', [index, _src, _html]);
            } else {
                _this.$slide.eq(index).prepend('<div class="lg-img-wrap"><img class="lg-object lg-image" src="' + _src + '" /></div>');
            }

            _this.$el.trigger('onAferAppendSlide.lg', [index]);

            _$img = _this.$slide.eq(index).find('.lg-object');
            if (_sizes) {
                _$img.attr('sizes', _sizes);
            }

            if (_srcset) {
                _$img.attr('srcset', _srcset);
                try {
                    picturefill({
                        elements: [_$img[0]]
                    });
                } catch (e) {
                    console.warn('lightGallery :- If you want srcset to be supported for older browser please include picturefil version 2 javascript library in your document.');
                }
            }

            if (this.s.appendSubHtmlTo !== '.lg-sub-html') {
                _this.addHtml(index);
            }

            _this.$slide.eq(index).addClass('lg-loaded');
        }

        _this.$slide.eq(index).find('.lg-object').on('load.lg error.lg', function() {

            // For first time add some delay for displaying the start animation.
            var _speed = 0;

            // Do not change the delay value because it is required for zoom plugin.
            // If gallery opened from direct url (hash) speed value should be 0
            if (delay && !$('body').hasClass('lg-from-hash')) {
                _speed = delay;
            }

            setTimeout(function() {
                _this.$slide.eq(index).addClass('lg-complete');
                _this.$el.trigger('onSlideItemLoad.lg', [index, delay || 0]);
            }, _speed);

        });

        // @todo check load state for html5 videos
        if (_isVideo && _isVideo.html5 && !_hasPoster) {
            _this.$slide.eq(index).addClass('lg-complete');
        }

        if (rec === true) {
            if (!_this.$slide.eq(index).hasClass('lg-complete')) {
                _this.$slide.eq(index).find('.lg-object').on('load.lg error.lg', function() {
                    _this.preload(index);
                });
            } else {
                _this.preload(index);
            }
        }

        //}
    };

    Plugin.prototype.slide = function(index, fromTouch, fromThumb, direction) {

        var _prevIndex = this.$outer.find('.lg-current').index();
        var _this = this;

        // Prevent if multiple call
        // Required for hsh plugin
        if (_this.lGalleryOn && (_prevIndex === index)) {
            return;
        }

        var _length = this.$slide.length;
        var _time = _this.lGalleryOn ? this.s.speed : 0;

        if (!_this.lgBusy) {

            if (this.s.download) {
                var _src;
                if (_this.s.dynamic) {
                    _src = _this.s.dynamicEl[index].downloadUrl !== false && (_this.s.dynamicEl[index].downloadUrl || _this.s.dynamicEl[index].src);
                } else {
                    _src = _this.$items.eq(index).attr('data-download-url') !== 'false' && (_this.$items.eq(index).attr('data-download-url') || _this.$items.eq(index).attr('href') || _this.$items.eq(index).attr('data-src'));

                }

                if (_src) {
                    $('#lg-download').attr('href', _src);
                    _this.$outer.removeClass('lg-hide-download');
                } else {
                    _this.$outer.addClass('lg-hide-download');
                }
            }

            this.$el.trigger('onBeforeSlide.lg', [_prevIndex, index, fromTouch, fromThumb]);

            _this.lgBusy = true;

            clearTimeout(_this.hideBartimeout);

            // Add title if this.s.appendSubHtmlTo === lg-sub-html
            if (this.s.appendSubHtmlTo === '.lg-sub-html') {

                // wait for slide animation to complete
                setTimeout(function() {
                    _this.addHtml(index);
                }, _time);
            }

            this.arrowDisable(index);

            if (!direction) {
                if (index < _prevIndex) {
                    direction = 'prev';
                } else if (index > _prevIndex) {
                    direction = 'next';
                }
            }

            if (!fromTouch) {

                // remove all transitions
                _this.$outer.addClass('lg-no-trans');

                this.$slide.removeClass('lg-prev-slide lg-next-slide');

                if (direction === 'prev') {

                    //prevslide
                    this.$slide.eq(index).addClass('lg-prev-slide');
                    this.$slide.eq(_prevIndex).addClass('lg-next-slide');
                } else {

                    // next slide
                    this.$slide.eq(index).addClass('lg-next-slide');
                    this.$slide.eq(_prevIndex).addClass('lg-prev-slide');
                }

                // give 50 ms for browser to add/remove class
                setTimeout(function() {
                    _this.$slide.removeClass('lg-current');

                    //_this.$slide.eq(_prevIndex).removeClass('lg-current');
                    _this.$slide.eq(index).addClass('lg-current');

                    // reset all transitions
                    _this.$outer.removeClass('lg-no-trans');
                }, 50);
            } else {

                this.$slide.removeClass('lg-prev-slide lg-current lg-next-slide');
                var touchPrev;
                var touchNext;
                if (_length > 2) {
                    touchPrev = index - 1;
                    touchNext = index + 1;

                    if ((index === 0) && (_prevIndex === _length - 1)) {

                        // next slide
                        touchNext = 0;
                        touchPrev = _length - 1;
                    } else if ((index === _length - 1) && (_prevIndex === 0)) {

                        // prev slide
                        touchNext = 0;
                        touchPrev = _length - 1;
                    }

                } else {
                    touchPrev = 0;
                    touchNext = 1;
                }

                if (direction === 'prev') {
                    _this.$slide.eq(touchNext).addClass('lg-next-slide');
                } else {
                    _this.$slide.eq(touchPrev).addClass('lg-prev-slide');
                }

                _this.$slide.eq(index).addClass('lg-current');
            }

            if (_this.lGalleryOn) {
                setTimeout(function() {
                    _this.loadContent(index, true, 0);
                }, this.s.speed + 50);

                setTimeout(function() {
                    _this.lgBusy = false;
                    _this.$el.trigger('onAfterSlide.lg', [_prevIndex, index, fromTouch, fromThumb]);
                }, this.s.speed);

            } else {
                _this.loadContent(index, true, _this.s.backdropDuration);

                _this.lgBusy = false;
                _this.$el.trigger('onAfterSlide.lg', [_prevIndex, index, fromTouch, fromThumb]);
            }

            _this.lGalleryOn = true;

            if (this.s.counter) {
                $('#lg-counter-current').text(index + 1);
            }

        }

    };

    /**
     *  @desc Go to next slide
     *  @param {Boolean} fromTouch - true if slide function called via touch event
     */
    Plugin.prototype.goToNextSlide = function(fromTouch) {
        var _this = this;
        var _loop = _this.s.loop;
        if (fromTouch && _this.$slide.length < 3) {
            _loop = false;
        }

        if (!_this.lgBusy) {
            if ((_this.index + 1) < _this.$slide.length) {
                _this.index++;
                _this.$el.trigger('onBeforeNextSlide.lg', [_this.index]);
                _this.slide(_this.index, fromTouch, false, 'next');
            } else {
                if (_loop) {
                    _this.index = 0;
                    _this.$el.trigger('onBeforeNextSlide.lg', [_this.index]);
                    _this.slide(_this.index, fromTouch, false, 'next');
                } else if (_this.s.slideEndAnimatoin && !fromTouch) {
                    _this.$outer.addClass('lg-right-end');
                    setTimeout(function() {
                        _this.$outer.removeClass('lg-right-end');
                    }, 400);
                }
            }
        }
    };

    /**
     *  @desc Go to previous slide
     *  @param {Boolean} fromTouch - true if slide function called via touch event
     */
    Plugin.prototype.goToPrevSlide = function(fromTouch) {
        var _this = this;
        var _loop = _this.s.loop;
        if (fromTouch && _this.$slide.length < 3) {
            _loop = false;
        }

        if (!_this.lgBusy) {
            if (_this.index > 0) {
                _this.index--;
                _this.$el.trigger('onBeforePrevSlide.lg', [_this.index, fromTouch]);
                _this.slide(_this.index, fromTouch, false, 'prev');
            } else {
                if (_loop) {
                    _this.index = _this.$items.length - 1;
                    _this.$el.trigger('onBeforePrevSlide.lg', [_this.index, fromTouch]);
                    _this.slide(_this.index, fromTouch, false, 'prev');
                } else if (_this.s.slideEndAnimatoin && !fromTouch) {
                    _this.$outer.addClass('lg-left-end');
                    setTimeout(function() {
                        _this.$outer.removeClass('lg-left-end');
                    }, 400);
                }
            }
        }
    };

    Plugin.prototype.keyPress = function() {
        var _this = this;
        if (this.$items.length > 1) {
            $(window).on('keyup.lg', function(e) {
                if (_this.$items.length > 1) {
                    if (e.keyCode === 37) {
                        e.preventDefault();
                        _this.goToPrevSlide();
                    }

                    if (e.keyCode === 39) {
                        e.preventDefault();
                        _this.goToNextSlide();
                    }
                }
            });
        }

        $(window).on('keydown.lg', function(e) {
            if (_this.s.escKey === true && e.keyCode === 27) {
                e.preventDefault();
                if (!_this.$outer.hasClass('lg-thumb-open')) {
                    _this.destroy();
                } else {
                    _this.$outer.removeClass('lg-thumb-open');
                }
            }
        });
    };

    Plugin.prototype.arrow = function() {
        var _this = this;
        this.$outer.find('.lg-prev').on('click.lg', function() {
            _this.goToPrevSlide();
        });

        this.$outer.find('.lg-next').on('click.lg', function() {
            _this.goToNextSlide();
        });
    };

    Plugin.prototype.arrowDisable = function(index) {

        // Disable arrows if s.hideControlOnEnd is true
        if (!this.s.loop && this.s.hideControlOnEnd) {
            if ((index + 1) < this.$slide.length) {
                this.$outer.find('.lg-next').removeAttr('disabled').removeClass('disabled');
            } else {
                this.$outer.find('.lg-next').attr('disabled', 'disabled').addClass('disabled');
            }

            if (index > 0) {
                this.$outer.find('.lg-prev').removeAttr('disabled').removeClass('disabled');
            } else {
                this.$outer.find('.lg-prev').attr('disabled', 'disabled').addClass('disabled');
            }
        }
    };

    Plugin.prototype.setTranslate = function($el, xValue, yValue) {
        // jQuery supports Automatic CSS prefixing since jQuery 1.8.0
        if (this.s.useLeft) {
            $el.css('left', xValue);
        } else {
            $el.css({
                transform: 'translate3d(' + (xValue) + 'px, ' + yValue + 'px, 0px)'
            });
        }
    };

    Plugin.prototype.touchMove = function(startCoords, endCoords) {

        var distance = endCoords - startCoords;

        if (Math.abs(distance) > 15) {
            // reset opacity and transition duration
            this.$outer.addClass('lg-dragging');

            // move current slide
            this.setTranslate(this.$slide.eq(this.index), distance, 0);

            // move next and prev slide with current slide
            this.setTranslate($('.lg-prev-slide'), -this.$slide.eq(this.index).width() + distance, 0);
            this.setTranslate($('.lg-next-slide'), this.$slide.eq(this.index).width() + distance, 0);
        }
    };

    Plugin.prototype.touchEnd = function(distance) {
        var _this = this;

        // keep slide animation for any mode while dragg/swipe
        if (_this.s.mode !== 'lg-slide') {
            _this.$outer.addClass('lg-slide');
        }

        this.$slide.not('.lg-current, .lg-prev-slide, .lg-next-slide').css('opacity', '0');

        // set transition duration
        setTimeout(function() {
            _this.$outer.removeClass('lg-dragging');
            if ((distance < 0) && (Math.abs(distance) > _this.s.swipeThreshold)) {
                _this.goToNextSlide(true);
            } else if ((distance > 0) && (Math.abs(distance) > _this.s.swipeThreshold)) {
                _this.goToPrevSlide(true);
            } else if (Math.abs(distance) < 5) {

                // Trigger click if distance is less than 5 pix
                _this.$el.trigger('onSlideClick.lg');
            }

            _this.$slide.removeAttr('style');
        });

        // remove slide class once drag/swipe is completed if mode is not slide
        setTimeout(function() {
            if (!_this.$outer.hasClass('lg-dragging') && _this.s.mode !== 'lg-slide') {
                _this.$outer.removeClass('lg-slide');
            }
        }, _this.s.speed + 100);

    };

    Plugin.prototype.enableSwipe = function() {
        var _this = this;
        var startCoords = 0;
        var endCoords = 0;
        var isMoved = false;

        if (_this.s.enableSwipe && _this.doCss()) {

            _this.$slide.on('touchstart.lg', function(e) {
                if (!_this.$outer.hasClass('lg-zoomed') && !_this.lgBusy) {
                    e.preventDefault();
                    _this.manageSwipeClass();
                    startCoords = e.originalEvent.targetTouches[0].pageX;
                }
            });

            _this.$slide.on('touchmove.lg', function(e) {
                if (!_this.$outer.hasClass('lg-zoomed')) {
                    e.preventDefault();
                    endCoords = e.originalEvent.targetTouches[0].pageX;
                    _this.touchMove(startCoords, endCoords);
                    isMoved = true;
                }
            });

            _this.$slide.on('touchend.lg', function() {
                if (!_this.$outer.hasClass('lg-zoomed')) {
                    if (isMoved) {
                        isMoved = false;
                        _this.touchEnd(endCoords - startCoords);
                    } else {
                        _this.$el.trigger('onSlideClick.lg');
                    }
                }
            });
        }

    };

    Plugin.prototype.enableDrag = function() {
        var _this = this;
        var startCoords = 0;
        var endCoords = 0;
        var isDraging = false;
        var isMoved = false;
        if (_this.s.enableDrag && _this.doCss()) {
            _this.$slide.on('mousedown.lg', function(e) {
                // execute only on .lg-object
                if (!_this.$outer.hasClass('lg-zoomed')) {
                    if ($(e.target).hasClass('lg-object') || $(e.target).hasClass('lg-video-play')) {
                        e.preventDefault();

                        if (!_this.lgBusy) {
                            _this.manageSwipeClass();
                            startCoords = e.pageX;
                            isDraging = true;

                            _this.$outer.scrollLeft += 1;
                            _this.$outer.scrollLeft -= 1;

                            // *

                            _this.$outer.removeClass('lg-grab').addClass('lg-grabbing');

                            _this.$el.trigger('onDragstart.lg');
                        }

                    }
                }
            });

            $(window).on('mousemove.lg', function(e) {
                if (isDraging) {
                    isMoved = true;
                    endCoords = e.pageX;
                    _this.touchMove(startCoords, endCoords);
                    _this.$el.trigger('onDragmove.lg');
                }
            });

            $(window).on('mouseup.lg', function(e) {
                if (isMoved) {
                    isMoved = false;
                    _this.touchEnd(endCoords - startCoords);
                    _this.$el.trigger('onDragend.lg');
                } else if ($(e.target).hasClass('lg-object') || $(e.target).hasClass('lg-video-play')) {
                    _this.$el.trigger('onSlideClick.lg');
                }

                // Prevent execution on click
                if (isDraging) {
                    isDraging = false;
                    _this.$outer.removeClass('lg-grabbing').addClass('lg-grab');
                }
            });

        }
    };

    Plugin.prototype.manageSwipeClass = function() {
        var _touchNext = this.index + 1;
        var _touchPrev = this.index - 1;
        if (this.s.loop && this.$slide.length > 2) {
            if (this.index === 0) {
                _touchPrev = this.$slide.length - 1;
            } else if (this.index === this.$slide.length - 1) {
                _touchNext = 0;
            }
        }

        this.$slide.removeClass('lg-next-slide lg-prev-slide');
        if (_touchPrev > -1) {
            this.$slide.eq(_touchPrev).addClass('lg-prev-slide');
        }

        this.$slide.eq(_touchNext).addClass('lg-next-slide');
    };

    Plugin.prototype.mousewheel = function() {
        var _this = this;
        _this.$outer.on('mousewheel.lg', function(e) {

            if (!e.deltaY) {
                return;
            }

            if (e.deltaY > 0) {
                _this.goToPrevSlide();
            } else {
                _this.goToNextSlide();
            }

            e.preventDefault();
        });

    };

    Plugin.prototype.closeGallery = function() {

        var _this = this;
        var mousedown = false;
        this.$outer.find('.lg-close').on('click.lg', function() {
            _this.destroy();
        });

        if (_this.s.closable) {

            // If you drag the slide and release outside gallery gets close on chrome
            // for preventing this check mousedown and mouseup happened on .lg-item or lg-outer
            _this.$outer.on('mousedown.lg', function(e) {

                if ($(e.target).is('.lg-outer') || $(e.target).is('.lg-item ') || $(e.target).is('.lg-img-wrap')) {
                    mousedown = true;
                } else {
                    mousedown = false;
                }

            });

            _this.$outer.on('mouseup.lg', function(e) {

                if ($(e.target).is('.lg-outer') || $(e.target).is('.lg-item ') || $(e.target).is('.lg-img-wrap') && mousedown) {
                    if (!_this.$outer.hasClass('lg-dragging')) {
                        _this.destroy();
                    }
                }

            });

        }

    };

    Plugin.prototype.destroy = function(d) {

        var _this = this;

        if (!d) {
            _this.$el.trigger('onBeforeClose.lg');
            $(window).scrollTop(_this.prevScrollTop);
        }


        /**
         * if d is false or undefined destroy will only close the gallery
         * plugins instance remains with the element
         *
         * if d is true destroy will completely remove the plugin
         */

        if (d) {
            if (!_this.s.dynamic) {
                // only when not using dynamic mode is $items a jquery collection
                this.$items.off('click.lg click.lgcustom');
            }

            $.removeData(_this.el, 'lightGallery');
        }

        // Unbind all events added by lightGallery
        this.$el.off('.lg.tm');

        // Distroy all lightGallery modules
        $.each($.fn.lightGallery.modules, function(key) {
            if (_this.modules[key]) {
                _this.modules[key].destroy();
            }
        });

        this.lGalleryOn = false;

        clearTimeout(_this.hideBartimeout);
        this.hideBartimeout = false;
        $(window).off('.lg');
        $('body').removeClass('lg-on lg-from-hash');

        if (_this.$outer) {
            _this.$outer.removeClass('lg-visible');
        }

        $('.lg-backdrop').removeClass('in');

        setTimeout(function() {
            if (_this.$outer) {
                _this.$outer.remove();
            }

            $('.lg-backdrop').remove();

            if (!d) {
                _this.$el.trigger('onCloseAfter.lg');
            }

        }, _this.s.backdropDuration + 50);
    };

    $.fn.lightGallery = function(options) {
        return this.each(function() {
            if (!$.data(this, 'lightGallery')) {
                $.data(this, 'lightGallery', new Plugin(this, options));
            } else {
                try {
                    $(this).data('lightGallery').init();
                } catch (err) {
                    console.error('lightGallery has not initiated properly');
                }
            }
        });
    };

    $.fn.lightGallery.modules = {};

})();


}));

/*! lg-autoplay - v1.0.4 - 2017-03-28 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define(['jquery'], function (a0) {
      return (factory(a0));
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory(require('jquery'));
  } else {
    factory(jQuery);
  }
}(this, function ($) {


(function() {

    'use strict';

    var defaults = {
        autoplay: false,
        pause: 5000,
        progressBar: true,
        fourceAutoplay: false,
        autoplayControls: true,
        appendAutoplayControlsTo: '.lg-toolbar'
    };

    /**
     * Creates the autoplay plugin.
     * @param {object} element - lightGallery element
     */
    var Autoplay = function(element) {

        this.core = $(element).data('lightGallery');

        this.$el = $(element);

        // Execute only if items are above 1
        if (this.core.$items.length < 2) {
            return false;
        }

        this.core.s = $.extend({}, defaults, this.core.s);
        this.interval = false;

        // Identify if slide happened from autoplay
        this.fromAuto = true;

        // Identify if autoplay canceled from touch/drag
        this.canceledOnTouch = false;

        // save fourceautoplay value
        this.fourceAutoplayTemp = this.core.s.fourceAutoplay;

        // do not allow progress bar if browser does not support css3 transitions
        if (!this.core.doCss()) {
            this.core.s.progressBar = false;
        }

        this.init();

        return this;
    };

    Autoplay.prototype.init = function() {
        var _this = this;

        // append autoplay controls
        if (_this.core.s.autoplayControls) {
            _this.controls();
        }

        // Create progress bar
        if (_this.core.s.progressBar) {
            _this.core.$outer.find('.lg').append('<div class="lg-progress-bar"><div class="lg-progress"></div></div>');
        }

        // set progress
        _this.progress();

        // Start autoplay
        if (_this.core.s.autoplay) {
            _this.$el.one('onSlideItemLoad.lg.tm', function() {
                _this.startlAuto();
            });
        }

        // cancel interval on touchstart and dragstart
        _this.$el.on('onDragstart.lg.tm touchstart.lg.tm', function() {
            if (_this.interval) {
                _this.cancelAuto();
                _this.canceledOnTouch = true;
            }
        });

        // restore autoplay if autoplay canceled from touchstart / dragstart
        _this.$el.on('onDragend.lg.tm touchend.lg.tm onSlideClick.lg.tm', function() {
            if (!_this.interval && _this.canceledOnTouch) {
                _this.startlAuto();
                _this.canceledOnTouch = false;
            }
        });

    };

    Autoplay.prototype.progress = function() {

        var _this = this;
        var _$progressBar;
        var _$progress;

        _this.$el.on('onBeforeSlide.lg.tm', function() {

            // start progress bar animation
            if (_this.core.s.progressBar && _this.fromAuto) {
                _$progressBar = _this.core.$outer.find('.lg-progress-bar');
                _$progress = _this.core.$outer.find('.lg-progress');
                if (_this.interval) {
                    _$progress.removeAttr('style');
                    _$progressBar.removeClass('lg-start');
                    setTimeout(function() {
                        _$progress.css('transition', 'width ' + (_this.core.s.speed + _this.core.s.pause) + 'ms ease 0s');
                        _$progressBar.addClass('lg-start');
                    }, 20);
                }
            }

            // Remove setinterval if slide is triggered manually and fourceautoplay is false
            if (!_this.fromAuto && !_this.core.s.fourceAutoplay) {
                _this.cancelAuto();
            }

            _this.fromAuto = false;

        });
    };

    // Manage autoplay via play/stop buttons
    Autoplay.prototype.controls = function() {
        var _this = this;
        var _html = '<span class="lg-autoplay-button lg-icon"></span>';

        // Append autoplay controls
        $(this.core.s.appendAutoplayControlsTo).append(_html);

        _this.core.$outer.find('.lg-autoplay-button').on('click.lg', function() {
            if ($(_this.core.$outer).hasClass('lg-show-autoplay')) {
                _this.cancelAuto();
                _this.core.s.fourceAutoplay = false;
            } else {
                if (!_this.interval) {
                    _this.startlAuto();
                    _this.core.s.fourceAutoplay = _this.fourceAutoplayTemp;
                }
            }
        });
    };

    // Autostart gallery
    Autoplay.prototype.startlAuto = function() {
        var _this = this;

        _this.core.$outer.find('.lg-progress').css('transition', 'width ' + (_this.core.s.speed + _this.core.s.pause) + 'ms ease 0s');
        _this.core.$outer.addClass('lg-show-autoplay');
        _this.core.$outer.find('.lg-progress-bar').addClass('lg-start');

        _this.interval = setInterval(function() {
            if (_this.core.index + 1 < _this.core.$items.length) {
                _this.core.index++;
            } else {
                _this.core.index = 0;
            }

            _this.fromAuto = true;
            _this.core.slide(_this.core.index, false, false, 'next');
        }, _this.core.s.speed + _this.core.s.pause);
    };

    // cancel Autostart
    Autoplay.prototype.cancelAuto = function() {
        clearInterval(this.interval);
        this.interval = false;
        this.core.$outer.find('.lg-progress').removeAttr('style');
        this.core.$outer.removeClass('lg-show-autoplay');
        this.core.$outer.find('.lg-progress-bar').removeClass('lg-start');
    };

    Autoplay.prototype.destroy = function() {

        this.cancelAuto();
        this.core.$outer.find('.lg-progress-bar').remove();
    };

    $.fn.lightGallery.modules.autoplay = Autoplay;

})();


}));



/*! lg-pager - v1.0.2 - 2017-01-22*/

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define(['jquery'], function (a0) {
      return (factory(a0));
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory(require('jquery'));
  } else {
    factory(jQuery);
  }
}(this, function ($) {

(function() {

    'use strict';

    var defaults = {
        pager: false
    };

    var Pager = function(element) {

        this.core = $(element).data('lightGallery');

        this.$el = $(element);
        this.core.s = $.extend({}, defaults, this.core.s);
        if (this.core.s.pager && this.core.$items.length > 1) {
            this.init();
        }

        return this;
    };

    Pager.prototype.init = function() {
        var _this = this;
        var pagerList = '';
        var $pagerCont;
        var $pagerOuter;
        var timeout;

        _this.core.$outer.find('.lg').append('<div class="lg-pager-outer"></div>');

        if (_this.core.s.dynamic) {
            for (var i = 0; i < _this.core.s.dynamicEl.length; i++) {
                pagerList += '<span class="lg-pager-cont"> <span class="lg-pager"></span><div class="lg-pager-thumb-cont"><span class="lg-caret"></span> <img src="' + _this.core.s.dynamicEl[i].thumb + '" /></div></span>';
            }
        } else {
            _this.core.$items.each(function() {

                if (!_this.core.s.exThumbImage) {
                    pagerList += '<span class="lg-pager-cont"> <span class="lg-pager"></span><div class="lg-pager-thumb-cont"><span class="lg-caret"></span> <img src="' + $(this).find('img').attr('src') + '" /></div></span>';
                } else {
                    pagerList += '<span class="lg-pager-cont"> <span class="lg-pager"></span><div class="lg-pager-thumb-cont"><span class="lg-caret"></span> <img src="' + $(this).attr(_this.core.s.exThumbImage) + '" /></div></span>';
                }

            });
        }

        $pagerOuter = _this.core.$outer.find('.lg-pager-outer');

        $pagerOuter.html(pagerList);

        $pagerCont = _this.core.$outer.find('.lg-pager-cont');
        $pagerCont.on('click.lg touchend.lg', function() {
            var _$this = $(this);
            _this.core.index = _$this.index();
            _this.core.slide(_this.core.index, false, true, false);
        });

        $pagerOuter.on('mouseover.lg', function() {
            clearTimeout(timeout);
            $pagerOuter.addClass('lg-pager-hover');
        });

        $pagerOuter.on('mouseout.lg', function() {
            timeout = setTimeout(function() {
                $pagerOuter.removeClass('lg-pager-hover');
            });
        });

        _this.core.$el.on('onBeforeSlide.lg.tm', function(e, prevIndex, index) {
            $pagerCont.removeClass('lg-pager-active');
            $pagerCont.eq(index).addClass('lg-pager-active');
        });

    };

    Pager.prototype.destroy = function() {

    };

    $.fn.lightGallery.modules.pager = Pager;

})();


}));


/*! lg-video - v1.1.0 - 2017-08-08 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define(['jquery'], function (a0) {
      return (factory(a0));
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory(require('jquery'));
  } else {
    factory(jQuery);
  }
}(this, function ($) {

(function() {

    'use strict';

    var defaults = {
        videoMaxWidth: '855px',
        youtubePlayerParams: false,
        vimeoPlayerParams: false,
        dailymotionPlayerParams: false,
        vkPlayerParams: false,
        videojs: false,
        videojsOptions: {}
    };

    var Video = function(element) {

        this.core = $(element).data('lightGallery');

        this.$el = $(element);
        this.core.s = $.extend({}, defaults, this.core.s);
        this.videoLoaded = false;

        this.init();

        return this;
    };

    Video.prototype.init = function() {
        var _this = this;

        // Event triggered when video url found without poster
        _this.core.$el.on('hasVideo.lg.tm', function(event, index, src, html) {
            _this.core.$slide.eq(index).find('.lg-video').append(_this.loadVideo(src, 'lg-object', true, index, html));
            if (html) {
                if (_this.core.s.videojs) {
                    try {
                        videojs(_this.core.$slide.eq(index).find('.lg-html5').get(0), _this.core.s.videojsOptions, function() {
                            if (!_this.videoLoaded) {
                                this.play();
                            }
                        });
                    } catch (e) {
                        console.error('Make sure you have included videojs');
                    }
                } else {
                    if(!_this.videoLoaded) {
                        _this.core.$slide.eq(index).find('.lg-html5').get(0).play();
                    }
                }
            }
        });

        // Set max width for video
        _this.core.$el.on('onAferAppendSlide.lg.tm', function(event, index) {
            var $videoCont = _this.core.$slide.eq(index).find('.lg-video-cont');
            if (!$videoCont.hasClass('lg-has-iframe')) {
                $videoCont.css('max-width', _this.core.s.videoMaxWidth);
                _this.videoLoaded = true;
            }
        });

        var loadOnClick = function($el) {
            // check slide has poster
            if ($el.find('.lg-object').hasClass('lg-has-poster') && $el.find('.lg-object').is(':visible')) {

                // check already video element present
                if (!$el.hasClass('lg-has-video')) {

                    $el.addClass('lg-video-playing lg-has-video');

                    var _src;
                    var _html;
                    var _loadVideo = function(_src, _html) {

                        $el.find('.lg-video').append(_this.loadVideo(_src, '', false, _this.core.index, _html));

                        if (_html) {
                            if (_this.core.s.videojs) {
                                try {
                                    videojs(_this.core.$slide.eq(_this.core.index).find('.lg-html5').get(0), _this.core.s.videojsOptions, function() {
                                        this.play();
                                    });
                                } catch (e) {
                                    console.error('Make sure you have included videojs');
                                }
                            } else {
                                _this.core.$slide.eq(_this.core.index).find('.lg-html5').get(0).play();
                            }
                        }

                    };

                    if (_this.core.s.dynamic) {

                        _src = _this.core.s.dynamicEl[_this.core.index].src;
                        _html = _this.core.s.dynamicEl[_this.core.index].html;

                        _loadVideo(_src, _html);

                    } else {

                        _src = _this.core.$items.eq(_this.core.index).attr('href') || _this.core.$items.eq(_this.core.index).attr('data-src');
                        _html = _this.core.$items.eq(_this.core.index).attr('data-html');

                        _loadVideo(_src, _html);

                    }

                    var $tempImg = $el.find('.lg-object');
                    $el.find('.lg-video').append($tempImg);

                    // @todo loading icon for html5 videos also
                    // for showing the loading indicator while loading video
                    if (!$el.find('.lg-video-object').hasClass('lg-html5')) {
                        $el.removeClass('lg-complete');
                        $el.find('.lg-video-object').on('load.lg error.lg', function() {
                            $el.addClass('lg-complete');
                        });
                    }

                } else {

                    var youtubePlayer = $el.find('.lg-youtube').get(0);
                    var vimeoPlayer = $el.find('.lg-vimeo').get(0);
                    var dailymotionPlayer = $el.find('.lg-dailymotion').get(0);
                    var html5Player = $el.find('.lg-html5').get(0);
                    if (youtubePlayer) {
                        youtubePlayer.contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
                    } else if (vimeoPlayer) {
                        try {
                            $f(vimeoPlayer).api('play');
                        } catch (e) {
                            console.error('Make sure you have included froogaloop2 js');
                        }
                    } else if (dailymotionPlayer) {
                        dailymotionPlayer.contentWindow.postMessage('play', '*');

                    } else if (html5Player) {
                        if (_this.core.s.videojs) {
                            try {
                                videojs(html5Player).play();
                            } catch (e) {
                                console.error('Make sure you have included videojs');
                            }
                        } else {
                            html5Player.play();
                        }
                    }

                    $el.addClass('lg-video-playing');

                }
            }
        };

        if (_this.core.doCss() && (_this.core.$items.length > 1) && (_this.core.s.enableSwipe || _this.core.s.enableDrag)) {
            _this.core.$el.on('onSlideClick.lg.tm', function() {
                var $el = _this.core.$slide.eq(_this.core.index);
                loadOnClick($el);
            });
        } else {

            // For IE 9 and bellow
            _this.core.$slide.on('click.lg', function() {
                loadOnClick($(this));
            });
        }

        _this.core.$el.on('onBeforeSlide.lg.tm', function(event, prevIndex, index) {

            var $videoSlide = _this.core.$slide.eq(prevIndex);
            var youtubePlayer = $videoSlide.find('.lg-youtube').get(0);
            var vimeoPlayer = $videoSlide.find('.lg-vimeo').get(0);
            var dailymotionPlayer = $videoSlide.find('.lg-dailymotion').get(0);
            var vkPlayer = $videoSlide.find('.lg-vk').get(0);
            var html5Player = $videoSlide.find('.lg-html5').get(0);
            if (youtubePlayer) {
                youtubePlayer.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
            } else if (vimeoPlayer) {
                try {
                    $f(vimeoPlayer).api('pause');
                } catch (e) {
                    console.error('Make sure you have included froogaloop2 js');
                }
            } else if (dailymotionPlayer) {
                dailymotionPlayer.contentWindow.postMessage('pause', '*');

            } else if (html5Player) {
                if (_this.core.s.videojs) {
                    try {
                        videojs(html5Player).pause();
                    } catch (e) {
                        console.error('Make sure you have included videojs');
                    }
                } else {
                    html5Player.pause();
                }
            } if (vkPlayer) {
                $(vkPlayer).attr('src', $(vkPlayer).attr('src').replace('&autoplay', '&noplay'));
            }

            var _src;
            if (_this.core.s.dynamic) {
                _src = _this.core.s.dynamicEl[index].src;
            } else {
                _src = _this.core.$items.eq(index).attr('href') || _this.core.$items.eq(index).attr('data-src');

            }

            var _isVideo = _this.core.isVideo(_src, index) || {};
            if (_isVideo.youtube || _isVideo.vimeo || _isVideo.dailymotion || _isVideo.vk) {
                _this.core.$outer.addClass('lg-hide-download');
            }

            //$videoSlide.addClass('lg-complete');

        });

        _this.core.$el.on('onAfterSlide.lg.tm', function(event, prevIndex) {
            _this.core.$slide.eq(prevIndex).removeClass('lg-video-playing');
        });
    };

    Video.prototype.loadVideo = function(src, addClass, noposter, index, html) {
        var video = '';
        var autoplay = 1;
        var a = '';
        var isVideo = this.core.isVideo(src, index) || {};

        // Enable autoplay for first video if poster doesn't exist
        if (noposter) {
            if (this.videoLoaded) {
                autoplay = 0;
            } else {
                autoplay = 1;
            }
        }

        if (isVideo.youtube) {

            a = '?wmode=opaque&autoplay=' + autoplay + '&enablejsapi=1';
            if (this.core.s.youtubePlayerParams) {
                a = a + '&' + $.param(this.core.s.youtubePlayerParams);
            }

            video = '<iframe class="lg-video-object lg-youtube ' + addClass + '" width="560" height="315" src="//www.youtube.com/embed/' + isVideo.youtube[1] + a + '" frameborder="0" allowfullscreen></iframe>';

        } else if (isVideo.vimeo) {

            a = '?autoplay=' + autoplay + '&api=1';
            if (this.core.s.vimeoPlayerParams) {
                a = a + '&' + $.param(this.core.s.vimeoPlayerParams);
            }

            video = '<iframe class="lg-video-object lg-vimeo ' + addClass + '" width="560" height="315"  src="//player.vimeo.com/video/' + isVideo.vimeo[1] + a + '" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>';

        } else if (isVideo.dailymotion) {

            a = '?wmode=opaque&autoplay=' + autoplay + '&api=postMessage';
            if (this.core.s.dailymotionPlayerParams) {
                a = a + '&' + $.param(this.core.s.dailymotionPlayerParams);
            }

            video = '<iframe class="lg-video-object lg-dailymotion ' + addClass + '" width="560" height="315" src="//www.dailymotion.com/embed/video/' + isVideo.dailymotion[1] + a + '" frameborder="0" allowfullscreen></iframe>';

        } else if (isVideo.html5) {
            var fL = html.substring(0, 1);
            if (fL === '.' || fL === '#') {
                html = $(html).html();
            }

            video = html;

        } else if (isVideo.vk) {

            a = '&autoplay=' + autoplay;
            if (this.core.s.vkPlayerParams) {
                a = a + '&' + $.param(this.core.s.vkPlayerParams);
            }

            video = '<iframe class="lg-video-object lg-vk ' + addClass + '" width="560" height="315" src="http://vk.com/video_ext.php?' + isVideo.vk[1] + a + '" frameborder="0" allowfullscreen></iframe>';

        }

        return video;
    };

    Video.prototype.destroy = function() {
        this.videoLoaded = false;
    };

    $.fn.lightGallery.modules.video = Video;

})();


}));


/*! lg-hash - v1.0.2 - 2017-06-03 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define(['jquery'], function (a0) {
      return (factory(a0));
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory(require('jquery'));
  } else {
    factory(jQuery);
  }
}(this, function ($) {

(function() {

    'use strict';

    var defaults = {
        hash: true
    };

    var Hash = function(element) {

        this.core = $(element).data('lightGallery');

        this.core.s = $.extend({}, defaults, this.core.s);

        if (this.core.s.hash) {
            this.oldHash = window.location.hash;
            this.init();
        }

        return this;
    };

    Hash.prototype.init = function() {
        var _this = this;
        var _hash;

        // Change hash value on after each slide transition
        _this.core.$el.on('onAfterSlide.lg.tm', function(event, prevIndex, index) {
            if (history.replaceState) {
                history.replaceState(null, null, '#lg=' + _this.core.s.galleryId + '&slide=' + index);
            } else {
                window.location.hash = 'lg=' + _this.core.s.galleryId + '&slide=' + index;
            }
        });

        // Listen hash change and change the slide according to slide value
        $(window).on('hashchange.lg.hash', function() {
            _hash = window.location.hash;
            var _idx = parseInt(_hash.split('&slide=')[1], 10);

            // it galleryId doesn't exist in the url close the gallery
            if ((_hash.indexOf('lg=' + _this.core.s.galleryId) > -1)) {
                _this.core.slide(_idx, false, false);
            } else if (_this.core.lGalleryOn) {
                _this.core.destroy();
            }

        });
    };

    Hash.prototype.destroy = function() {

        if (!this.core.s.hash) {
            return;
        }

        // Reset to old hash value
        if (this.oldHash && this.oldHash.indexOf('lg=' + this.core.s.galleryId) < 0) {
            if (history.replaceState) {
                history.replaceState(null, null, this.oldHash);
            } else {
                window.location.hash = this.oldHash;
            }
        } else {
            if (history.replaceState) {
                history.replaceState(null, document.title, window.location.pathname + window.location.search);
            } else {
                window.location.hash = '';
            }
        }

        this.core.$el.off('.lg.hash');

    };

    $.fn.lightGallery.modules.hash = Hash;

})();

}));

/*! lg-share - v1.0.2 - 2016-11-26 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define(['jquery'], function (a0) {
      return (factory(a0));
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory(require('jquery'));
  } else {
    factory(jQuery);
  }
}(this, function ($) {

(function() {

    'use strict';

    var defaults = {
        share: true,
        facebook: true,
        facebookDropdownText: 'Facebook',
        twitter: true,
        twitterDropdownText: 'Twitter',
        googlePlus: true,
        googlePlusDropdownText: 'GooglePlus',
        pinterest: true,
        pinterestDropdownText: 'Pinterest'
    };

    var Share = function(element) {

        this.core = $(element).data('lightGallery');

        this.core.s = $.extend({}, defaults, this.core.s);
        if (this.core.s.share) {
            this.init();
        }

        return this;
    };

    Share.prototype.init = function() {
        var _this = this;
        var shareHtml = '<span id="lg-share" class="lg-icon">' +
            '<ul class="lg-dropdown" style="position: absolute;">';
        shareHtml += _this.core.s.facebook ? '<li><a id="lg-share-facebook" target="_blank"><span class="lg-icon"></span><span class="lg-dropdown-text">' + this.core.s.facebookDropdownText + '</span></a></li>' : '';
        shareHtml += _this.core.s.twitter ? '<li><a id="lg-share-twitter" target="_blank"><span class="lg-icon"></span><span class="lg-dropdown-text">' + this.core.s.twitterDropdownText + '</span></a></li>' : '';
        shareHtml += _this.core.s.googlePlus ? '<li><a id="lg-share-googleplus" target="_blank"><span class="lg-icon"></span><span class="lg-dropdown-text">' + this.core.s.googlePlusDropdownText + '</span></a></li>' : '';
        shareHtml += _this.core.s.pinterest ? '<li><a id="lg-share-pinterest" target="_blank"><span class="lg-icon"></span><span class="lg-dropdown-text">' + this.core.s.pinterestDropdownText + '</span></a></li>' : '';
        shareHtml += '</ul></span>';

        this.core.$outer.find('.lg-toolbar').append(shareHtml);
        this.core.$outer.find('.lg').append('<div id="lg-dropdown-overlay"></div>');
        $('#lg-share').on('click.lg', function(){
            _this.core.$outer.toggleClass('lg-dropdown-active');
        });

        $('#lg-dropdown-overlay').on('click.lg', function(){
            _this.core.$outer.removeClass('lg-dropdown-active');
        });

        _this.core.$el.on('onAfterSlide.lg.tm', function(event, prevIndex, index) {

            setTimeout(function() { 
                $('#lg-share-facebook').attr('href', 'https://www.facebook.com/sharer/sharer.php?u=' + (encodeURIComponent(_this.core.$items.eq(index).attr('data-facebook-share-url') || window.location.href)));

                $('#lg-share-twitter').attr('href', 'https://twitter.com/intent/tweet?text=' + _this.core.$items.eq(index).attr('data-tweet-text') + '&url=' + (encodeURIComponent(_this.core.$items.eq(index).attr('data-twitter-share-url') || window.location.href)));

                $('#lg-share-googleplus').attr('href', 'https://plus.google.com/share?url=' + (encodeURIComponent(_this.core.$items.eq(index).attr('data-googleplus-share-url') || window.location.href)));

                $('#lg-share-pinterest').attr('href', 'http://www.pinterest.com/pin/create/button/?url=' + (encodeURIComponent(_this.core.$items.eq(index).attr('data-pinterest-share-url') || window.location.href)) + '&media=' + encodeURIComponent(_this.core.$items.eq(index).attr('href') || _this.core.$items.eq(index).attr('data-src')) + '&description=' + _this.core.$items.eq(index).attr('data-pinterest-text'));

            }, 100);
        });
    };

    Share.prototype.destroy = function() {

    };

    $.fn.lightGallery.modules.share = Share;

})();

}));


 /* ================== Light Gallery JS ends HERE ============================*/






/* ========================================================================
  =================== STARTS OF COMMON JS HERE ============================
 * ======================================================================== */
jQuery(document).ready(function($) {

  // Fix navbar on top JS Starts here 
  var scrollStart = $("nav").offset().top;
    var navHeight = $("nav").height();
    var grayBody = $("body").hasClass("fixed-navigation");
    var bannerSticky = $("body").hasClass('banner-sticky-head');

    $(window).on('scroll', function() {
        var scroll = $(window).scrollTop();

        if(!bannerSticky) {
            if (scroll > scrollStart) {
                $("nav").addClass("sticky-nav").css('position', 'fixed');
                $(".navbar-toggle").addClass("push-290");
            } else {
                $("nav").removeClass("sticky-nav").css('position', '');
                $(".navbar-toggle").removeClass("push-290");
            }
        } 
    });// Fix navbar on top JS Ends here 

    // Mobile silde menu JS Starts here 
    var sideslider = $('[data-toggle=collapse-side]');
    var sel = sideslider.attr('data-target');
    var sel2 = sideslider.attr('data-target-2');

    sideslider.click(function(event){
        $(sel).toggleClass('in');
        $(sel2).toggleClass('out');
    });// Mobile silde menu JS Ends here

    $('.mask').click(function(event){
        $(sel).toggleClass('in');
        $(sel2).toggleClass('out');
    });// Mobile silde menu JS Ends here


    // Filter silde menu JS Starts here 
    var filter = $('[data-toggle=collapse-fil]');
    var fil = filter.attr('fil-target');
    var fil2 = filter.attr('fil-target-3');

    filter.click(function(event){
        $(fil).toggleClass('in');
        $(fil2).toggleClass('out-fil');
    });// Filter silde menu JS Ends here

    $('.mask-fil').click(function(event){
        $(fil).toggleClass('in');
        $(fil2).toggleClass('out-fil');
    });// Filter silde menu JS Ends here



    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      $('.certificate').slick('setPosition', 0);
    });

    // certificate and courses slider function Starts here 
    $('.certificate').slick({
      dots: false,
      infinite: false,
      arrows: true,
      speed: 300,
      slidesToShow: 4,
      slidesToScroll: 4,
      responsive: [
        {
          breakpoint: 1025,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
            infinite: false,
            dots: false
          }
        },
        {
          breakpoint: 769,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2,
            arrows: false
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            dots: true
          }
        }
      ]
    });// certificate and courses slider function ends here

    // Events slider function ends here
    $('.event-slider').slick({
      dots: false,
      infinite: false,
      arrows: true,
      speed: 300,
      slidesToShow: 3,
      slidesToScroll: 3,
      responsive: [
        {
          breakpoint: 1025,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2,
            infinite: false,
            dots: false
          }
        },
        {
          breakpoint: 769,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2,
            arrows: false
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            dots: true
          }
        }
      ]
    });// Events slider function ends here




  // Client logo function ends here
  $('.client-logo').slick({
    dots: false,
    infinite: false,
    arrows: true,
    speed: 300,
    slidesToShow: 4,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 1025,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          infinite: false,
          dots: false
        }
      },
      {
        breakpoint: 769,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          arrows: false
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          arrows: false,
          dots: true
        }
      }
    ]
  });// Client logo function ends here
  
  // Client logo function ends here
  $('.team').slick({
    dots: false,
    infinite: false,
    arrows: true,
    speed: 300,
    slidesToShow: 3,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 1025,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          infinite: false,
          dots: false
        }
      },
      {
        breakpoint: 769,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          arrows: false
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          arrows: false,
          dots: true
        }
      }
    ]
  });// Client logo function ends here



    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      $('.testimonials').slick('setPosition', 0);
    });

    $('.testimonials').slick({
      dots: true,
      responsive: [
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            dots: true
          }
        }
      ]
    }); 


    $('.main-banner').slick({
      arrows: false,
      dots: true
    }); 

    $('.rhs-testimonials').slick({
      dots: true,
    }); 



// With JQuery
$("#ex2").slider({});

// Modal Auto load 
// $(window).load(function(){
//    setTimeout(function(){
//        $('#rac').modal('show');
//    }, 2000);
// });

  // LightGallery function
  $('#lightgallery').lightGallery({
    thumbnail:false,
    download:false,
    counter:false,
    fullScreen:false,
    zoom:false
  });
});


$(document).ready(function() { 
    if ($(window).width() >767 ) {
      $(".dropdown").hover(function() {
            $('.multi-level', this).stop( true, true ).fadeIn("fast");
            $(this).toggleClass('open');              
          },

          function() {
            $('.multi-level', this).stop( true, true ).fadeOut("fast");
            $(this).toggleClass('open');               
      });

      $(".dropdown-submenu").hover (function() {
        $('.multi-level', this).stop( true, true ).fadeOut("fast");
        $(this).toggleClass('open');
        $(this).toggleClass('active');

      });
    }
});



    if ($(window).width() <767 ) {

    (function menu() {
        var parentMenu = $('.js-dropdown'),
        firstLevel = $('.js-multi-level'),
        secondLevel = $('.js-level-one'),
        thirdLevel = $('.js-level-two');


        var jsDropdownClick = function() {
            $('.js-dropdown').on('click',function(e){
                e.stopPropagation();
                e.preventDefault();
                menuShow.call(this,'.js-multi-level');

            });
        };

        var jsLevelOne = function() {
            $('.js-level-one').on('click',function(e){
                e.stopPropagation();
                menuShow.call(this,'.js-level-two');
            });
        };

        var menuShow = function(childElementClass) {
            var childElement = $(this).closest('li').find(childElementClass);
            if(childElement.css('display') == 'none') {
                childElement.show();
                if(childElementClass == '.js-multi-level') {
                    $(this).closest('li').find('.js-level-one').show();
                }
                if(childElementClass == '.js-level-one') {
                    $(this).closest('li').find('.js-level-two').show();
                }
            } else {
                childElement.hide();
            }
        };

        var blackArrowClick = function(){
            $('.js-menu-back').on('click',function(e){
                e.stopPropagation();
                $(this).closest('ul').hide();
            })
        };

        var maskClick = function() {
            $('.mask').on('click',function(e){
                e.stopPropagation();
                firstLevel.hide();
                secondLevel.hide();
                thirdLevel.hide();
            });
        }


        var init = function(){
            jsDropdownClick();
            jsLevelOne();
            blackArrowClick();
            maskClick();
        };

        init();
    })();
    }
