/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Modal extends Component {
  static template = "pos_custom_popup.Modal";

  confirm() {
    this.props.resolve({ confirmed: true });
  }

  cancel() {
    this.props.resolve({ confirmed: false });
  }
}
