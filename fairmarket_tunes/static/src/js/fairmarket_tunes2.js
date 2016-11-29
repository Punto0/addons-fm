openerp.fairmarket_tunes = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    alert('JOLL');
    local.TwoDecimals = instance.Widget.extend({
        className: 'oe_fairmarket_tunes_2decimals',
        start: function() {
	    alert('helow');
            this.$el.append("<div>Hello dear Odoo user!</div>");
	    this.alert('JELOW');
            //console.log("pet store home page loaded");
        },

    });


    instance.web.client_actions.add('fairmarket_tunes.TwoDecimals', 'instance.fairmarket_tunes.TwoDecimals');
}
