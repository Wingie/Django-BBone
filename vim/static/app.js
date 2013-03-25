var app = app || {};
app.collection = app.collection || {};

app.model = Backbone.Model.extend({});

app.collection.usrList = Backbone.Collection.extend({
	model:app.model,
	initialize: function(){
		this.count = 0;
		this.id = $('#searchResults').children(".searchDisplay");
                          this.qry = "";
	},
	 url : function(){
      		return '/api/search/'+this.qry;
    	},
    	parse : function(response){
	      this.count = response.count;
	      return response.results;  
    	},
    	retrieve: function(q){
    		
                          this.qry = "?";
                          self = this; 

                          _.each(q,function(val,key){
                                if(val){
                                    self.qry=self.qry+"&"+key+"=1";
                                    console.log(self.qry);
                                }
                          });
                          
                         self.id.children().remove();
                         $('#count').html("Loading...");
    		this.fetch({success:function(){   
                                                                            $('#count').html(self.count+" Results");	
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