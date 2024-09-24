odoo.define('bill_of_quantity_prasetia.custom_scrollable_tree_view', function(require) {
    "use strict";
    var core = require('web.core');
    var ListView = require('web.ListView');

    // Inject custom CSS after the DOM is ready
    $(document).ready(function() {
        // Add custom styles to the tree view
        $("<style>")
            .prop("type", "text/css")
            .html("\
                .o_list_view { overflow-x: auto; white-space: nowrap; }\
                .o_list_view th, .o_list_view td { min-width: 150px; }\
                th { white-space: nowrap; }\
            ")
            .appendTo("head");
    });
});
