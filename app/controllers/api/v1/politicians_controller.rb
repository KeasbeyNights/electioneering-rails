module Api
  module V1
    class PoliticiansController < ApplicationController
      respond_to :json

      def index
        respond_with Politician.all
      end

      def compare
        respond_with Politician.find([params[:white].politician_id, 
          params[:black].politician_id])
      end

    end
  end
end