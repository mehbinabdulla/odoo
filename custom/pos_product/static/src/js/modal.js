import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@odoo/owl";

export class DiscountLimit extends Component {
    static components = { Dialog };
    static template = "pos_product.DiscountLimit";
    static props = ["close", "title", "body"];

    setup() {}

    confirm() {
        this.props.close();
    }
}
