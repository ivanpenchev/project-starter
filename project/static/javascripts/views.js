var BuilderView = Backbone.View.extend({

    el: '#builder_view',

    events: {
        "click #builder_menu a" : "navigate",
    },

    render: function() {
        return true;
    },

    navigate: function(e) {
        e.preventDefault();
        
        var element = e.currentTarget;
        $(element).parents('ul').find('.current').removeClass('current');
        $(element).addClass('current');
        var href = $(element).attr('href');
        builderRouter.navigate(href, {trigger: true});
    },

});