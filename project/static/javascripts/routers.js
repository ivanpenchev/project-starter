var BuilderRouter = Backbone.Router.extend({
    routes: {
        'builder/:id/landing-page/' : 'landing_page',
        'builder/:id/sharing-page/' : 'sharing_page',
        'builder/:id/confirmation-email/' : 'confirmation_email',
        'builder/:id/site-settings/' : 'site_settings',
        'builder/:id/review-page/' : 'review_page',
    },

    landing_page: function(id) {
        var builderPage = new BuilderPage({id: id+'/landing-page'});
        builderPage.fetch();
    },
    sharing_page: function(id) {
        var builderPage = new BuilderPage({id: id+'/sharing-page'});
        builderPage.fetch();
    },
    confirmation_email: function(id) {
        var builderPage = new BuilderPage({id: id+'/confirmation-email'});
        builderPage.fetch();
    },
    site_settings: function(id) {
        var builderPage = new BuilderPage({id: id+'/site-settings'});
        builderPage.fetch();
    },
    review_page: function(id) {
        var builderPage = new BuilderPage({id: id+'/review-page'});
        builderPage.fetch();
    },
})