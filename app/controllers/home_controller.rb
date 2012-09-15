class HomeController < ApplicationController
	def index
    @politician = Politician.new
	end

  def compare
    @white = Politician.first(:name => params[:candidate1])
    @black = Politician.first(:name => params[:candidate2])
  end
end