/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
console.log("Dynamic")
publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector : '.school_event_snippet',
    async willStart() {
        const result = await rpc('/event/widget/latest', {});
        console.log(result)
        if(result){
            this.$target.empty().html(renderToElement('school_management.latest_event_snippet', {result: result}))
        } else {
            console.log("Hehhe")
        }

    },
});