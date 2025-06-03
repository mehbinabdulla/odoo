/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
publicWidget.registry.get_latest_event = publicWidget.Widget.extend({
    selector : '.school_event_snippet',
    async willStart() {
        const result = await rpc('/event/widget/latest', {'limit': 4});
        console.log(result)
        if(result){
            this.$target.empty().html(renderToElement('school_management.latest_event', {result: result.events}))
        }
    },
});

publicWidget.registry.get_carousal_event = publicWidget.Widget.extend({
    selector : '.school_event_snippet',
    async willStart() {
        const result = await rpc('/event/widget/latest', {'limit': 10});
        console.log(result)
        if(result){
            this.$target.empty().html(renderToElement('school_management.latest_event', {result: result.events}))
        }
    },
});