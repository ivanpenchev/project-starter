Backbone.emulateHTTP = true; // Use _method parameter rather than using DELETE and PUT methods
Backbone.emulateJSON = true; // Send data to server via parameter rather than via request content
 
var BuilderPage = Backbone.Model.extend({
    initialize: function() {
        this.on('change:builder_content', function(e) {
            $('#builder_content').html(this.get('builder_content'));

            Aloha.ready( function() {
                var $ = Aloha.jQuery;
                $('.editable').aloha();
            });
            Aloha.bind('aloha-editable-deactivated', function(a, b) {
                var element = $(b.editable.obj);
                var originalElementText = b.editable.originalContent.trim();
                var elementText = element.html();
                var isCustom = element.hasClass('custom');

                var splitedId = element.attr('id').split('_');
                var elementId = splitedId[1];
                var pageId = splitedId[2];

                var deleteElement = false;
                var newElement = false;

                if (elementId == 0) newElement = true;
                if (element.text().trim() == '')
                {
                    if (isCustom) deleteElement = true;
                    else
                    {
                        if (newElement)
                        {
                            originalElementText = element.data('elementText');
                            element.attr('style', 'color: #ccc;');
                        }
                        element.html(originalElementText);

                        return;
                    }
                }
                else
                {
                    if (element.html().trim() == originalElementText) return;
                }

                $.post('/builder/ajax/save_element/', {
                    'content' : elementText,
                    'position' : elementId,
                    'page_id' : pageId,
                    'delete' : deleteElement,
                    'new' : newElement
                }, function(data) {
                    if (!data.success)
                    {
                        element.html(originalElementText);
                    }
                    else
                    {
                        if (splitedId[1] == 0)
                        {
                            splitedId[1] = data.element_id;
                            var newElement = $('<div></div>')
                                .addClass('editable')
                                .addClass('custom')
                                .attr('id', splitedId.join('_'))
                                .attr('style', 'margin-bottom: 5px;')
                                .html(elementText);
                            $('.elements').append(newElement);

                            Aloha.ready( function() {
                                var $ = Aloha.jQuery;
                                $('.editable').aloha();
                            });

                            element.attr('style', 'color: #ccc;');
                            element.html(element.data('elementText'));
                        }
                        
                        if (deleteElement)
                        {
                            element.remove();
                        }
                    }
                });
            });
        });
        Aloha.bind('aloha-editable-activated', function(a, b) {
            var element = $(b.editable.obj);
            var isCustom = element.hasClass('custom');

            var elementId = element.attr('id').split('_')[1];

            if (elementId == 0)
            {
                var elementText = element.html();
                element.data('elementText', elementText);
                element.attr('style', '');
                element.html('');
            }
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