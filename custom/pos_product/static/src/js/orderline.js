/** @odoo-module */
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

let currentOrderLimit = [];
let productDiscountMap = {};

patch(PosOrder.prototype, {
    setup() {
        currentOrderLimit = this.models["pos.category"].getAll().map(cat => ({
            id: cat.id,
            name: cat.name,
            discount_limit: (cat.discount_limit || 0) * 100,
        }));
        productDiscountMap = {};
        console.log("Initial Discount Limits:", currentOrderLimit);
        return super.setup(...arguments);
    }
});

patch(PosOrderline.prototype, {
    setup(vals) {
        return super.setup(...arguments);
    },

    getDisplayData() {
        return {
            ...super.getDisplayData(),
            rating: this.get_product().rating,
            discount_limit: this.get_product().discount_limit,
        };
    },

    set_discount(new_discount) {
        const product = this.get_product();
        const productId = product.id;
        const categoryIds = product.pos_categ_ids || [];

        if (!categoryIds.length) {
            return super.set_discount(...arguments);
        }

        const categoryId = categoryIds[0].id;

        const category = currentOrderLimit.find(cat => cat.id === categoryId);
        if (!category) return super.set_discount(...arguments);

        const prev_discount = productDiscountMap[productId] || 0;
        const difference = new_discount - prev_discount;

        if (category.discount_limit - difference < 0) {
            alert(`Maximum discount limit of category '${category.name}' exceeded.`);
            return;
        }

        category.discount_limit -= difference;
        productDiscountMap[productId] = new_discount;

        console.log(`Category ${category.name} remaining discount: ${category.discount_limit}%`);

        return super.set_discount(...arguments);
    }
});

patch(Orderline.prototype, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                rating: { type: [String, Boolean], optional: true },
                discount_limit: { type: Number, optional: true },
            },
        },
    },
});
