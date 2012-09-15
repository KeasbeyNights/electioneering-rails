class HomeController < ApplicationController
	def index
    @politician = Politician.new
	end

  def compare
    @white = Politician.first(:name => params[:white])
    @black = Politician.first(:name => params[:black])
  end
end