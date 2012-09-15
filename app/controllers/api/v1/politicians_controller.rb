module Api
  module V1
    class PoliticiansController < ApplicationController
      respond_to :json

      def index
        if !params["names"]["auth"].eql?('lZvqvJZgXVsYVB43siOl0jsAYNhJXR3Qhnyh4tQlEgSxRi1qxuG7qtXDqjOTk4KN')
          respond_with ''
        elsif params["names"]["white"].nil? || 
          params["names"]["black"].nil?
          respond_with Politician.all
        else
          @white = Politician.where(:name => params["names"]["white"])
          @black = Politician.where(:name => params["names"]["black"])
          respond_with [@white, @black].to_json
        end
      end
    end
  end
end