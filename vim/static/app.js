var app = app || {};
app.collection = app.collection || {};

app.model = Backbone.Model.extend({});

app.collection.usrList = Backbone.Collection.extend({
	model:app.model,
	initialize: function(){
		this.count = 0;
		this.id = $('#searchResults').children(".searchDisplay");
	},
	 url : function(){
      		return '/api/search/';
    	},
    	parse : function(response){
	      this.count = response.count;
	      return response.results;  
    	},
    	retrieve: function(){
    		self = this;

    		this.fetch({success:function(){   
                                                                            $('#count').html(self.count+" Results");
    						self.id.children().remove();
			    			self.each(function(u){
			    				self.id.append(new app.collection.usrListItemView({model:u}).render().el);
			    			});
    		              }
    	   });
    	}//end retrieve
});

app.collection.usrListItemView = Backbone.View.extend({
 
     tagName:"li",
 
    template:_.template($("#usrTemplate").html()),
 
    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }
 
});