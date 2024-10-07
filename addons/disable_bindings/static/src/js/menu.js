/** @odoo-module **/

import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";

const userMenuRegistry = registry.category("user_menuitems");

// For removing the menu:
patch(UserMenu.prototype,  {
    setup() {
        super.setup(...arguments);
        userMenuRegistry.remove("documentation");
    },
});

patch(UserMenu.prototype,  {
    setup() {
        super.setup(...arguments);
        userMenuRegistry.remove("odoo_account");
    },
});

patch(UserMenu.prototype,  {
    setup() {
        super.setup(...arguments);
        userMenuRegistry.remove("support");
    },
});
// For adding the menu:
// function documentationItemNew(env) {
//     const documentationURL = "https://www.odoo.com/documentation/17.0"; // Updated to Odoo 17
//     return {
//         type: "item",
//         id: "documentation",
//         description: env._t("New Documentation"),
//         href: documentationURL,
//         callback: () => {
//             browser.open(documentationURL, "_blank");
//         },
//         sequence: 10,
//     };
// }

// userMenuRegistry.add("documentation", documentationItemNew);