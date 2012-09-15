class HomeController < ApplicationController
	def index
    Politician.create ({:name => 'Mitt Romney', :party => 'Republican', 
      :type => 'president'})
	end
end