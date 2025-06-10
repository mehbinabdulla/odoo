/** @odoo-module */
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    setup(vals) {
        return super.setup(...arguments);
    },
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            rating: this.get_product().rating,
        };
    },
    set_discount(discount){
        console.log(this.get_product().pos_categ_ids[0].discount_limit)
        return super.set_discount(...arguments)
    }
});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                rating: { type: [String, Boolean], optional: true },
            },
        },
    },
});