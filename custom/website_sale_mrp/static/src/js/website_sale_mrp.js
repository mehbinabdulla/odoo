/*odoo module*/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { Component } from "@odoo/owl";
import wSaleUtils from "@website_sale/js/website_sale_utils";


const WebsiteSaleBom = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'click [name="add_bom_to_cart"]': '_onClickAddBomToCart',
    },

    start: function () {
        return this._super(...arguments);
    },

    _onClickAddBomToCart: function (ev) {
        ev.preventDefault();
        const $el = $(ev.currentTarget);
        const productId = parseInt($el.data('product-id'));
        const addQty = parseFloat($el.data('add-qty'));

        rpc("/shop/cart/update_json", {
            product_id: productId,
            add_qty: addQty,
        }).then((data) => {
            $('.js_cart_lines').load("/shop/cart .js_cart_lines > *", () => {
                new WebsiteSaleBom(null, $('.oe_website_sale')).start();
            });
            wSaleUtils.updateCartNavBar(data);
            wSaleUtils.showWarning(data.notification_info.warning);
            Component.env.bus.trigger('cart_amount_changed', [data.amount, data.minor_amount]);
        });
    },
});

publicWidget.registry.WebsiteSaleBom = WebsiteSaleBom;

