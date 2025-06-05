//$(document).ready(function () {
//    $(document).on("click", '[name="add_bom_to_cart"]', function (e) {
//        console.log($(this).data('product-id'))
//        try {
//            const productId = parseInt($(this).data('product-id'));
//            const addQty = parseFloat($(this).data('add-qty'));
//            fetch('/shop/cart/update_json', {
//                method: 'POST',
//                headers: {
//                    'Content-Type': 'application/json',
//                    'X-Requested-With': 'XMLHttpRequest',
//                },
//                body: JSON.stringify({
//                    params: {
//                        product_id: productId,
//                        add_qty: addQty
//                    }
//                })
//            })
//                .then(response => response.json())
//                .then(data => {
//                    window.location.reload(true)
//                })
//        } catch(e) {
//            console.log(`${e} Haaaai`)
//        }
//    });
//});

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


export const WebsiteSaleBom = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: Object.assign({}, VariantMixin.events || {}, {
        'click [name="add_bom_to_cart"]': '_onClickAddBomToCart',
    }),

    _onClickAddBomToCart: function() {
         const productId = parseInt($(this).data('product-id'));
         const addQty = parseFloat($(this).data('add-qty'));
        rpc("/shop/cart/update_json", {
            product_id: productId,
            add_qty: addQty
        }).then((data) => {
            console.log(data)
        });
    }
})

