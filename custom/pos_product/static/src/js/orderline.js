/** @odoo-module */
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { DiscountLimit } from "./modal";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

let currentOrderLimit = [];
let productDiscountMap = {};
let dialogTimeout;

patch(PosOrder.prototype, {
    setup() {
        currentOrderLimit = this.models["pos.category"].getAll().map(cat => ({
            id: cat.id,
            name: cat.name,
            discount_limit: (cat.discount_limit || 0) * 100,
        }));
        productDiscountMap = {};
        console.log("Setup Discount:", currentOrderLimit);
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
        if (!categoryIds.length) return super.set_discount(...arguments);

        const categoryId = categoryIds[0];
        const category = currentOrderLimit.find(cat => cat.id === categoryId.id);
        if (!category) return super.set_discount(...arguments);

        const prev_discount = productDiscountMap[productId] || 0;
        const difference = new_discount - prev_discount;

        if (category.discount_limit - difference < 0) {
            window.dispatchEvent(new CustomEvent("discount_limit_exceeded", {
               detail: { category: categoryId.name, limit: categoryId.discount_limit * 100 }
            }));
            console.log('Discount limit exceeded');
            return;
        }

        category.discount_limit -= difference;
        productDiscountMap[productId] = new_discount;
        console.log(`${category.name} remaining : ${category.discount_limit}%`);
        return super.set_discount(...arguments);
    }
});


patch(Orderline.prototype, {

    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this._onLimitExceeded = this._onLimitExceeded.bind(this);
        window.addEventListener("discount_limit_exceeded", this._onLimitExceeded);
    },

    willUnmount() {
        window.removeEventListener("discount_limit_exceeded", this._onLimitExceeded);
    },

    async _onLimitExceeded(event) {
        if (dialogTimeout) return;
        dialogTimeout = setTimeout(() => {
            dialogTimeout = null;
        }, 500);
        await this.dialog.add(DiscountLimit, {
           title: "Discount Limit Exceeded",
           body: `Maximum discount limit (${event.detail.limit}%) of category ${event.detail.category} exceeded.`,
        });
    },

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
