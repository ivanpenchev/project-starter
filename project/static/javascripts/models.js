Backbone.emulateHTTP = true; // Use _method parameter rather than using DELETE and PUT methods
Backbone.emulateJSON = true; // Send data to server via parameter rather than via request content
 
var BuilderPage = Backbone.Model.extend({
    initialize: function() {
        this.on('change:builder_content', function(e) {
            $('#builder_content').html(this.get('builder_content'));
        });
    },

    defaults: {
        builder_content: 'undefined',
        page_id: 'undefined',
    },

    urlRoot: "/builder/",

    url: function() {
        var base = this.urlRoot || (this.collection && this.collection.url) || "/";
        if (this.isNew()) return base;
 
        return base + this.id + '/json';
    }
});