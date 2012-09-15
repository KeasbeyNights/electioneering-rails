class PoliticianController < ApplicationController
  def create
    @politician = Politician.new(params[:politician])
    @politician.save
  end
end