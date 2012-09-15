class HomeController < ApplicationController
	def index
    @politician = Politician.new
	end

  def compare
    @white = Politician.first(:name => params[:white])
    #Issue.create(:politician_id => @white._id, :name => "Abortion", 
     # :stance => "pro-choice")
    #Issue.create(:politician_id => @white._id, :name => "Gay Marriage", 
     # :stance => "support")
    #Issue.create(:politician_id => @white._id, :name => "Gun Control", 
     # :stance => "regulate")
    @black = Politician.first(:name => params[:black])
    #Issue.create(:politician_id => @black._id, :name => "Abortion", 
     # :stance => "pro-life")
    #Issue.create(:politician_id => @black._id, :name => "Gay Marriage", 
     # :stance => "oppose")
    #Issue.create(:politician_id => @black._id, :name => "Gun Control", 
     # :stance => "deregulate")
  end
end