;(function ( $ ) {

    var pluginName = 'validate',
        defaults = {

        };

    function Plugin( element, options ) {
        this.element = element;
        this.$element = $(element);

        this.options = $.extend( {}, defaults, options) ;

        this._defaults = defaults;
        this._name = pluginName;

        this.init();
    };

    Plugin.prototype.init = function () {
        this.initEvents();
    };

    Plugin.prototype.initEvents = function() {
        var self = this;
        var $email = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/;
        var $validateEmail = false;

        self.$element.change(function() {
            var $val = self.$element.val();
            if (self.$element.attr('id') == 'email') {
                var $apply = $email.test($val);
                if ($apply)
                    $validateEmail = true;
            }
        });

        $('.b-button').on('click', function(e){
            if (!$validateEmail)
                e.preventDefault();
        });
    };

    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, 'plugin_' + pluginName)) {
                $.data(this, 'plugin_' + pluginName,
                    new Plugin( this, options ));
            }
        });
    };

})( jQuery );

